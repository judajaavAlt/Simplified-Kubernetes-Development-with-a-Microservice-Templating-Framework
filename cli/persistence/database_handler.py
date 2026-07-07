from abc import ABC, abstractmethod
from .template_repository import (
    TemplateRepository,
    ReferenceRepository,
    TagRepository,
    LayerRepository
    )


class DatabaseHandler(
    TemplateRepository,
    ReferenceRepository,
    TagRepository,
    LayerRepository,
    ABC
                     ):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def close(self):
        ...
