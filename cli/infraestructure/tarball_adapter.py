from cli.persistence.tarball_repository import TarballRepository
from cli.application.config import Config
import os
import tarfile
import io
import shutil
from pathlib import Path


class TarballAdapter(TarballRepository):
    def __init__(self, folder_name: str, filename: str = "archive.tar.gz",
                 compression: str = "gz"):
        """
        Initializes the repository.

        :param folder_name: The target subdirectory (e.g., 'temp' or '/').
                            If '/', it saves directly to the base path.
        :param filename: The name of the tarball file itself.
        :param compression: Compression type ('gz', 'bz2', or '').
        """
        # 1. Fetch the base path from your Config singleton
        config = Config()
        base_path = Path(config.get("path", "."))

        # 2. Resolve the folder structure ("/" means root of the base path)
        if folder_name == "/":
            self.target_dir = base_path
        else:
            self.target_dir = base_path / folder_name

        # Ensure the directory exists on the disk
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # 3. Set up full path and compression modes
        self.tar_path = str(self.target_dir / filename)
        self.mode_suffix = f":{compression}" if compression else ""

        # Initialize an empty tarball safely if it doesn't exist
        if not os.path.exists(self.tar_path):
            with tarfile.open(self.tar_path, f"w{self.mode_suffix}") as _:
                pass

    def _file_exists(self, arcname: str) -> bool:
        """Helper to check if a file exists in the archive."""
        with tarfile.open(self.tar_path, f"r{self.mode_suffix}") as tar:
            return arcname in tar.getnames()

    def create_file(self, arcname: str, data: bytes) -> None:
        if self._file_exists(arcname):
            raise FileExistsError(f"File '{arcname}' already exists" +
                                  " in the archive. Use update_file instead.")

        # FIX: 'a' mode fails on compressed tarballs (gz).
        # We read the old content and stream the new file
        # into a temp file instead.
        temp_path = self.tar_path + ".tmp"
        with tarfile.open(self.tar_path, f"r{self.mode_suffix}") as src_tar, \
             tarfile.open(temp_path, f"w{self.mode_suffix}") as dest_tar:

            # Copy existing members
            for member in src_tar.getmembers():
                f = src_tar.extractfile(member) if member.isreg() else None
                dest_tar.addfile(member, f)

            # Append the brand new file
            tarinfo = tarfile.TarInfo(name=arcname)
            tarinfo.size = len(data)
            dest_tar.addfile(tarinfo, io.BytesIO(data))

        shutil.move(temp_path, self.tar_path)

    def read_file(self, arcname: str) -> bytes:
        with tarfile.open(self.tar_path, f"r{self.mode_suffix}") as tar:
            try:
                member = tar.getmember(arcname)
                f = tar.extractfile(member)
                if f is not None:
                    return f.read()
                raise FileNotFoundError(f"'{arcname}' could not " +
                                        "be extracted (likely a directory).")
            except KeyError:
                raise FileNotFoundError(f"File '{arcname}'" +
                                        " not found in the archive.")

    def list_files(self) -> list[str]:
        with tarfile.open(self.tar_path, f"r{self.mode_suffix}") as tar:
            return tar.getnames()

    def update_file(self, arcname: str, data: bytes) -> None:
        if not self._file_exists(arcname):
            raise FileNotFoundError(f"File '{arcname}'" +
                                    " does not exist to update.")

        temp_path = self.tar_path + ".tmp"
        with tarfile.open(self.tar_path, f"r{self.mode_suffix}") as src_tar, \
             tarfile.open(temp_path, f"w{self.mode_suffix}") as dest_tar:

            for member in src_tar.getmembers():
                if member.name == arcname:
                    new_tarinfo = tarfile.TarInfo(name=arcname)
                    new_tarinfo.size = len(data)
                    dest_tar.addfile(new_tarinfo, io.BytesIO(data))
                else:
                    f = src_tar.extractfile(member) if member.isreg() else None
                    dest_tar.addfile(member, f)

        shutil.move(temp_path, self.tar_path)

    def delete_file(self, arcname: str) -> None:
        if not self._file_exists(arcname):
            raise FileNotFoundError(f"File '{arcname}' does" +
                                    "not exist in the archive.")

        temp_path = self.tar_path + ".tmp"
        with tarfile.open(self.tar_path, f"r{self.mode_suffix}") as src_tar, \
             tarfile.open(temp_path, f"w{self.mode_suffix}") as dest_tar:

            for member in src_tar.getmembers():
                if member.name == arcname:
                    continue  # Skip to delete

                f = src_tar.extractfile(member) if member.isreg() else None
                dest_tar.addfile(member, f)

        shutil.move(temp_path, self.tar_path)
