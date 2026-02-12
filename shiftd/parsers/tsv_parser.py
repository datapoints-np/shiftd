"""Parse TSV (tab-separated values) into TableModel."""

import csv
from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("tsv")
class TSVParser:
    """Read TSV file into validated TableModel."""

    def parse(self, source: Path | str) -> TableModel:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(str(path))
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)
        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
