from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ArchiveOptions:
    extract_archive: bool = False
    archive_password: str | None = None
    archive_entry_path: str | None = None

    def to_form_data(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.extract_archive:
            data["extract_archive"] = True

        if self.archive_password is not None:
            data["archive_password"] = self.archive_password
            data["extract_archive"] = True

        if self.archive_entry_path is not None:
            data["archive_entry_path"] = self.archive_entry_path
            data["extract_archive"] = True

        return data
