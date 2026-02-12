"""Serialize TableModel to JSONL (JSON Lines)."""

import json
from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("jsonl")
class JSONLSerializer:
    """Write TableModel as JSONL (one JSON object per line)."""

    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs

    def serialize(self, table: TableModel, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for row in table.rows:
                f.write(json.dumps(row, **self.kwargs) + "\n")
