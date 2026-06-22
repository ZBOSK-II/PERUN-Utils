from pathlib import Path
from requests.exceptions import HTTPError, RequestException, Timeout

from api.exceptions import ApiError, NetworkError
from commands.base import BaseCommand


class DownloadCommand(BaseCommand):
    def execute(self, args):
        output_path = Path(args.output) if args.output else Path(args.filename)
        existing_size = output_path.stat().st_size if output_path.exists() else 0
        mode = "wb"

        if existing_size > 0:
            self.console.info(
                f"Resuming '{args.filename}' from {existing_size} bytes..."
            )
        else:
            self.console.info(f"Downloading '{args.filename}'...")

        resp = None
        try:
            resp = self.api.get_download_stream(
                args.task_uid, args.filename, existing_size
            )

            if existing_size > 0 and resp.status_code == 200:
                self.console.warning(
                    "Server ignored 'Range' header. Restarting download..."
                )
                mode, existing_size = "wb", 0
            elif existing_size > 0 and resp.status_code == 416:
                self.console.info("File already fully downloaded.")
                return
            elif resp.status_code >= 400:
                resp.raise_for_status()

            remaining_size = int(resp.headers.get("content-length", 0))
            total_size = existing_size + remaining_size

            with open(output_path, mode) as f:
                with self.console.progress_bar(
                    args.filename, total_size, existing_size
                ) as bar:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

            self.console.info(f"Saved to: {output_path.resolve()}")

        except HTTPError as e:
            error_detail = resp.text if resp and resp.text else str(e)
            if output_path.exists() and resp and resp.status_code < 500:
                output_path.unlink()
            raise ApiError(
                resp.status_code if resp else -1,
                f"File download failed {error_detail}",
            ) from e

        except Timeout as e:
            raise ApiError(
                resp.status_code if resp else -1,
                f"Download timed out: {e}\nPartial file saved. Run the command again to resume.",
            ) from e

        except RequestException as e:
            raise NetworkError(f"Request failed: {e}") from e
