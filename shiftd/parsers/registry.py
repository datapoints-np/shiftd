"""Registry of format parsers."""

from pathlib import Path
from typing import Protocol

from shiftd.schema import TableModel

Source = Path | str


class Parser(Protocol):
    """Parse a source (file path or connection string) into TableModel."""

    def parse(self, source: Source) -> TableModel: ...


_REGISTRY: dict[str, type[Parser]] = {}


def register_parser(format_name: str):
    """Decorator to register a parser class for a format."""

    def decorator(cls: type[Parser]) -> type[Parser]:
        _REGISTRY[format_name.lower()] = cls
        return cls

    return decorator


def get_parser(format_name: str) -> type[Parser]:
    name = format_name.lower()
    if name not in _REGISTRY:
        raise ValueError(f"Unknown format: {format_name}. Available: {sorted(_REGISTRY)}")
    return _REGISTRY[name]


def list_parser_formats() -> list[str]:
    return sorted(_REGISTRY.keys())
