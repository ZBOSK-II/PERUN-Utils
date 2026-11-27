from pathlib import Path

from api.exceptions import AppError
from commands.base import BaseCommand
from commands.utils.archive_options import ArchiveOptions


class UploadCommand(BaseCommand):
    def execute(self, args):
        file_path = Path(args.file)

        archive_options = (
            ArchiveOptions(
                args.archive_entry_path,
                args.archive_password,
            )
            if args.archive_cmd == "archive"
            else None
        )

        if not file_path.exists():
            raise AppError(f"File not found: {file_path}")

        self.console.info(f"Uploading '{file_path.name}'...")

        result = self.api.upload_file(
            file_path,
            args.duration,
            args.plugins,
            args.template_name,
            archive_options,
        )

        self.console.info("Uploaded file successfuly")
        self.console.json(result)
