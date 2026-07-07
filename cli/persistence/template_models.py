from dataclasses import dataclass


@dataclass(slots=True)
class Template:
    TemplateID: str
    ReferenceID: int


@dataclass(slots=True)
class Reference:
    ReferenceID: int
    Description: str
    Host: str
    Port: str
    Namespace: str
    Repository: str


@dataclass(slots=True)
class Tag:
    TemplateID: str
    Tag: str


@dataclass(slots=True)
class Layer:
    TemplateID: str
    LayerID: str
    LayerStep: int

@dataclass(slots=True)
class CompleteTemplate:
    TemplateID: str
    Reference: Reference
    Tag: str
    Layers: list[Layer]
