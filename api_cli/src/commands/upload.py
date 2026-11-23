from pathlib import Path

from api.exceptions import AppError
from commands.base import BaseCommand
from commands.utils.archive_options import ArchiveOptions


class UploadCommand(BaseCommand):
    def execute(self, args):
        file_path = Path(args.file)

        archive_options = ArchiveOptions(
            args.extract_archive, args.archive_password, args.archive_entry_path
        )

        if not file_path.exists():
            raise AppError(f"File not found: {file_path}")

        self.console.info(f"Uploading '{file_path.name}'...")

        result = self.api.upload_file(
            file_path,
            args.duration,
            args.plugins,
            archive_options,
            args.template_name,
        )

        self.console.info("Uploaded file successfuly")
        self.console.json(result)
