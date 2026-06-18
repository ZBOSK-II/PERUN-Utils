from commands.base import BaseCommand
from pathlib import Path
from api.exceptions import AppError


class UploadCommand(BaseCommand):
    def execute(self, args):
        file_path = Path(args.file)

        if not file_path.exists():
            raise AppError(f"File not found: {file_path}")

        self.console.info(f"Uploading '{file_path.name}'...")

        result = self.api.upload_file(file_path, args.duration, args.plugins)

        self.console.info("Uploaded file successfuly")
        self.console.json(result)
