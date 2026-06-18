from pathlib import Path
import requests
from api.exceptions import NetworkError
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

        except requests.exceptions.HTTPError as e:
            if output_path.exists() and resp.status_code < 500:
                output_path.unlink()
            self.console.error(f"Download failed (HTTP {resp.status_code}): {e}")
            raise SystemExit(1)
        except requests.exceptions.Timeout as e:
            self.console.error(f"Download timed out: {e}")
            self.console.error("Partial file saved. Run the command again to resume.")
            raise SystemExit(1)
        except NetworkError as e:
            self.console.error(f"Network error: {e}")
            raise SystemExit(1)
