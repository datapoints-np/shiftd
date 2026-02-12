"""Parse JSON into TableModel."""

import json
from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("json")
class JSONParser:
    """Read JSON (array of objects or single object) into TableModel."""

    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs

    def parse(self, path: Path) -> TableModel:
        if not path.exists():
            raise FileNotFoundError(str(path))
        with open(path, encoding="utf-8") as f:
            data = json.load(f, **self.kwargs)
        if isinstance(data, list):
            rows = [dict(r) for r in data]
        elif isinstance(data, dict):
            rows = [data]
        else:
            rows = []
        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
