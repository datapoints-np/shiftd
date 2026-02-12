"""Parse JSONL (JSON Lines) into TableModel."""

import json
from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("jsonl")
class JSONLParser:
    """Read JSONL file (one JSON object per line) into TableModel."""

    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs

    def parse(self, path: Path) -> TableModel:
        if not path.exists():
            raise FileNotFoundError(str(path))
        rows: list[dict] = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line, **self.kwargs))
        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
