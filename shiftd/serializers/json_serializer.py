"""Serialize TableModel to JSON."""

import json
from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("json")
class JSONSerializer:
    def __init__(self, indent: int | None = 2, **kwargs: object) -> None:
        self.indent = indent
        self.kwargs = kwargs

    def serialize(self, table: TableModel, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(table.rows, f, indent=self.indent, **self.kwargs)
