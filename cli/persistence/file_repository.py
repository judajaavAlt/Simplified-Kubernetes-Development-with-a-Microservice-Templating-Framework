from abc import ABC, abstractmethod
from pathlib import Path


class FileRepository(ABC):
    """Abstract Base Class defining the contract for file repositories."""

    @abstractmethod
    def save(self, template_id: str, archive: Path) -> None:
        """Save an archive path under the given template ID."""
        ...

    @abstractmethod
    def get(self, template_id: str) -> Path:
        """Retrieve the path for the given template ID.

        Raises FileNotFoundError if it doesn't exist.
        """
        ...

    @abstractmethod
    def delete(self, template_id: str) -> None:
        """Delete the archive associated with the template ID."""
        ...

    @abstractmethod
    def exists(self, template_id: str) -> bool:
        """Check if an archive exists for the given template ID."""
        ...
