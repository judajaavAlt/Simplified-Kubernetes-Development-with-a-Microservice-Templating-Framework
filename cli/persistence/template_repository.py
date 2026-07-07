from abc import ABC, abstractmethod

from .template_models import (
    Template,
    Reference,
    Tag,
    Layer,
    CompleteTemplate
)


class TemplateRepository(ABC):
    @abstractmethod
    def create_template(self, template: Template) -> None:
        ...

    @abstractmethod
    def get_template(self, template_id: str) -> Template | None:
        ...

    @abstractmethod
    def delete_template(self, template_id: str) -> None:
        ...

    @abstractmethod
    def get_by_reference(self, reference_id: int) -> list[Template]:
        ...

    @abstractmethod
    def get_complete(
        self, reference_id: int,
        tag: str
    ) -> CompleteTemplate | None:
        """
        Returns the template together with its reference, tags and layers.
        """
        ...


class ReferenceRepository(ABC):
    @abstractmethod
    def create_reference(self, reference: Reference) -> None:
        ...

    @abstractmethod
    def get_reference(self, reference_id: int) -> Reference | None:
        ...

    @abstractmethod
    def delete_reference(self, reference_id: int) -> None:
        ...


class TagRepository(ABC):
    @abstractmethod
    def create_tag(self, tag: Tag) -> None:
        ...

    @abstractmethod
    def get_by_template(self, template_id: str) -> list[Tag]:
        ...

    @abstractmethod
    def delete_tag(self, template_id: str, tag: str) -> None:
        ...


class LayerRepository(ABC):
    @abstractmethod
    def create_layer(self, layer: Layer) -> None:
        ...

    @abstractmethod
    def get_layers(self, template_id: str) -> list[Layer]:
        ...

    @abstractmethod
    def delete_layer(self, template_id: str, layer_id: str) -> None:
        ...
