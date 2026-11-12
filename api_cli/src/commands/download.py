from api.exceptions import ApiError, NetworkError
from commands.base import BaseCommand
from commands.utils.download_storage import DownloadStorage
from requests.exceptions import HTTPError, RequestException, Timeout


class DownloadCommand(BaseCommand):
    def __init__(self, api, console, storage: DownloadStorage | None = None):
        super().__init__(api, console)

        if storage is None:
            storage = DownloadStorage()

        self._storage = storage

    def execute(self, args):
        session = self._storage.prepare(
            args.task_uid,
            args.filename,
            args.output,
            reset=args.reset,
            force=args.force,
        )

        mode, offset = "ab", session.offset

        if offset > 0:
            self.console.info(
                f"Resuming '{args.filename}' from {offset} bytes into {session.target}..."
            )
        else:
            self.console.info(f"Downloading '{args.filename}' into {session.target}...")

        resp = None
        try:
            resp = self.api.get_download_stream(args.task_uid, args.filename, offset)

            if offset > 0 and resp.status_code == 200:
                self.console.warning(
                    "Server ignored 'Range' header. Restarting download..."
                )
                mode, offset = "wb", 0

            elif offset > 0 and resp.status_code == 416:
                self.console.info("File already fully downloaded.")
                return

            elif resp.status_code >= 400:
                resp.raise_for_status()

            remaining_size = int(resp.headers.get("content-length", 0))
            total_size = offset + remaining_size

            with (
                open(session.part, mode) as f,
                self.console.progress_bar(args.filename, total_size, offset) as bar,
            ):
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

            final = self._storage.complete(session)
            self.console.info(f"Saved to: {final.resolve()}")

        except HTTPError as e:
            if resp is None:
                raise ApiError(
                    resp.status_code if resp is not None else -1,
                    f"File download failed without response {e!s}",
                ) from e

            if resp.status_code == 404:
                self._storage.delete_meta(session.meta)

            raise ApiError(
                resp.status_code if resp is not None else -1,
                f"File download failed with response {resp.text}",
            ) from e

        except Timeout as e:
            raise ApiError(
                resp.status_code if resp is not None else -1,
                f"Download timed out: {e!s}",
            ) from e

        except RequestException as e:
            raise NetworkError(f"Request failed: {e!s}") from e
