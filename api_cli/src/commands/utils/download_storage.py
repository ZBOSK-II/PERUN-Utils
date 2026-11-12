import json
from dataclasses import dataclass
from pathlib import Path

from api.exceptions import AppError


@dataclass(frozen=True)
class DownloadMeta:
    task_uid: str
    filename: str
    target: Path

    @property
    def path(self) -> Path:
        return self.target.with_name(f"{self.target.name}.meta")

    @property
    def part(self) -> Path:
        return self.target.with_name(f"{self.target.name}.part")


@dataclass(frozen=True)
class DownloadSession:
    target: Path
    offset: int

    @property
    def part(self) -> Path:
        return self.target.with_name(f"{self.target.name}.part")

    @property
    def meta(self) -> Path:
        return self.target.with_name(f"{self.target.name}.meta")


class DownloadStorage:
    def complete(self, session: DownloadSession) -> Path:
        session.part.rename(session.target)
        self._remove_meta(session.meta)
        return session.target

    def get_meta(self, meta_path: Path) -> DownloadMeta | None:
        return self._read_meta(meta_path)

    def store_meta(self, meta: DownloadMeta) -> None:
        self._write_meta(meta)

    def delete_meta(self, meta_path: Path) -> None:
        self._remove_meta(meta_path)

    def prepare(
        self,
        task_uid: str,
        filename: str,
        output: str | None = None,
        *,
        reset: bool = False,
        force: bool = False,
    ) -> DownloadSession:
        meta = self._new_meta(filename, task_uid, output)

        if force:
            self._purge_existing_files(meta)
            self._write_meta(meta)
            return self._new_download_session(meta)

        if meta.target.exists():
            raise AppError(
                f"File already exists: {meta.target}. Use --force to overwrite."
            )

        if reset:
            self._discard_partial(meta)
            self._write_meta(meta)
            return self._new_download_session(meta)

        valid_meta_exists = self._valid_meta_exists(meta)
        if valid_meta_exists:
            return self._existing_download_session(meta)

        self._write_meta(meta)
        return self._new_download_session(meta)

    def _read_meta(self, meta_path: Path) -> DownloadMeta | None:
        try:
            data = json.loads(meta_path.read_text())
        except (OSError, json.JSONDecodeError):
            return None
        return DownloadMeta(
            task_uid=data.get("task_uid"),
            filename=data.get("filename"),
            target=Path(data.get("target")),
        )

    def _write_meta(self, meta: DownloadMeta) -> None:
        meta.path.write_text(
            json.dumps(
                {
                    "task_uid": meta.task_uid,
                    "filename": meta.filename,
                    "target": meta.target.as_posix(),
                },
                indent=2,
            )
        )

    def _remove_meta(self, meta_path: Path) -> None:
        try:
            meta_path.unlink()
        except FileNotFoundError:
            pass

    @staticmethod
    def _meta_matches(meta: DownloadMeta | None, task_uid: str, filename: str) -> bool:
        return (
            meta is not None and meta.task_uid == task_uid and meta.filename == filename
        )

    def _purge_existing_files(self, meta: DownloadMeta) -> None:
        for path in (meta.target, meta.part):
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        self._remove_meta(meta.path)

    def _discard_partial(self, meta: DownloadMeta) -> None:
        try:
            meta.part.unlink()
        except FileNotFoundError:
            pass
        self._remove_meta(meta.path)

    def _new_download_session(self, meta: DownloadMeta) -> DownloadSession:
        return DownloadSession(meta.target, 0)

    def _valid_meta_exists(self, meta: DownloadMeta) -> bool:
        existing_meta = self._read_meta(meta.path)
        if existing_meta is None:
            return False
        if not self._meta_matches(existing_meta, meta.task_uid, meta.filename):
            self._discard_partial(existing_meta)
            return False
        return True

    def _existing_download_session(self, meta: DownloadMeta) -> DownloadSession:
        file_size = meta.target.stat().st_size
        return DownloadSession(meta.target, file_size)

    @staticmethod
    def _target_name(filename: str, task_uid: str) -> str:
        filename = filename.replace("/", "-")
        print(filename)
        stem, dot, ext = filename.partition(".")
        if dot:
            return f"{stem}-{task_uid}.{ext}"
        return f"{filename}-{task_uid}"

    @staticmethod
    def _target_path(
        filename: str,
        task_uid: str,
        output: str | None,
    ) -> Path:
        resolved_filename = (
            output if output else DownloadStorage._target_name(filename, task_uid)
        )
        return Path(resolved_filename)

    @staticmethod
    def _new_meta(filename: str, task_uid: str, output: str | None) -> DownloadMeta:
        return DownloadMeta(
            task_uid,
            filename,
            DownloadStorage._target_path(filename, task_uid, output),
        )
