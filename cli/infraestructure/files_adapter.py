from pathlib import Path
import shutil
from cli.persistence.file_repository import FileRepository


class LocalFileRepository(FileRepository):
    _base_path = ""

    def _path(self, template_id: str) -> Path:
        return self._base_path / f"{template_id}.tar"

    def save(self, template_id: str, archive: Path) -> None:
        self._base_path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(archive, self._path(template_id))

    def get(self, template_id: str) -> Path:
        path = self._path(template_id)

        if not path.exists():
            raise FileNotFoundError(path)

        return path

    def delete(self, template_id: str) -> None:
        self._path(template_id).unlink(missing_ok=True)

    def exists(self, template_id: str) -> bool:
        return self._path(template_id).exists()
