"""Registry of format serializers."""

from pathlib import Path
from typing import Protocol

from shiftd.schema import TableModel

Target = Path | str


class Serializer(Protocol):
    """Serialize TableModel to a target (file path or connection string)."""

    def serialize(self, table: TableModel, target: Target) -> None: ...


_REGISTRY: dict[str, type[Serializer]] = {}


def register_serializer(format_name: str):
    """Decorator to register a serializer class for a format."""

    def decorator(cls: type[Serializer]) -> type[Serializer]:
        _REGISTRY[format_name.lower()] = cls
        return cls

    return decorator


def get_serializer(format_name: str) -> type[Serializer]:
    name = format_name.lower()
    if name not in _REGISTRY:
        raise ValueError(f"Unknown format: {format_name}. Available: {sorted(_REGISTRY)}")
    return _REGISTRY[name]


def list_serializer_formats() -> list[str]:
    return sorted(_REGISTRY.keys())
