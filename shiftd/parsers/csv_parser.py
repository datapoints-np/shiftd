"""Parse CSV into TableModel."""

import csv
from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("csv")
class CSVParser:
    """Read CSV file into validated TableModel."""

    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs

    def parse(self, path: Path) -> TableModel:
        if not path.exists():
            raise FileNotFoundError(str(path))
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, **self.kwargs)
            rows = list(reader)
        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
