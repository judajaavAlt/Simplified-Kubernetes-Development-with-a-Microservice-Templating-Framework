from abc import ABC, abstractmethod


class TarballRepository(ABC):
    """
    Abstract Base Class defining the CRUD operations for managing 
    files inside a tarball archive.
    """

    @abstractmethod
    def create_file(self, arcname: str, data: bytes) -> None:
        """
        CREATE: Add a new file with the given raw bytes into the tarball.
        Raises an exception if the file already exists.
        """
        ...

    @abstractmethod
    def read_file(self, arcname: str) -> bytes:
        """
        READ: Retrieve the raw bytes of a specific file inside the tarball.
        Raises FileNotFoundError if it doesn't exist.
        """
        ...

    @abstractmethod
    def list_files(self) -> list[str]:
        """
        READ (List): Return a list of all file paths present in the tarball.
        """
        ...

    @abstractmethod
    def update_file(self, arcname: str, data: bytes) -> None:
        """
        UPDATE: Modify an existing file's contents.
        If the file doesn't exist, it should raise a FileNotFoundError.
        """
        ...

    @abstractmethod
    def delete_file(self, arcname: str) -> None:
        """
        DELETE: Remove a file from the tarball.
        Raises FileNotFoundError if the file is not found.
        """
        ...
