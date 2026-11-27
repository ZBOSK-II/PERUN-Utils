import json
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ArchiveOptions:
    archive_entry_path: str
    archive_password: str | None = None

    def to_form_data(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "extract_archive": True,
            "archive_entry_path": self.archive_entry_path,
        }
        if self.archive_password is not None:
            data["archive_password"] = self.archive_password

        return {"archive_options": json.dumps(data)}
