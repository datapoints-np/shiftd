"""Parse HTML tables into TableModel."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


def _parse_attr(v: str) -> Any:
    """Try to coerce string values to int/float/bool."""
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if v.isdigit():
        return int(v)
    try:
        return float(v)
    except ValueError:
        return v


@register_parser("html")
class HTMLParser:
    """Read the first HTML <table> into TableModel.

    Uses only the stdlib html.parser — no extra dependencies.
    """

    def __init__(self, table_index: int = 0, **kwargs: object) -> None:
        self.table_index = table_index
        self.kwargs = kwargs

    def parse(self, path: Path) -> TableModel:
        if not path.exists():
            raise FileNotFoundError(str(path))

        from html.parser import HTMLParser as _HTMLParser

        class _TableExtractor(_HTMLParser):
            def __init__(self) -> None:
                super().__init__()
                self.tables: list[list[list[str]]] = []
                self._in_table = False
                self._in_row = False
                self._in_cell = False
                self._current_row: list[str] = []
                self._current_cell = ""
                self._current_table: list[list[str]] = []

            def handle_starttag(self, tag: str, attrs: list) -> None:
                if tag == "table":
                    self._in_table = True
                    self._current_table = []
                elif tag in ("tr",) and self._in_table:
                    self._in_row = True
                    self._current_row = []
                elif tag in ("td", "th") and self._in_row:
                    self._in_cell = True
                    self._current_cell = ""

            def handle_endtag(self, tag: str) -> None:
                if tag in ("td", "th") and self._in_cell:
                    self._in_cell = False
                    self._current_row.append(self._current_cell.strip())
                elif tag == "tr" and self._in_row:
                    self._in_row = False
                    self._current_table.append(self._current_row)
                elif tag == "table" and self._in_table:
                    self._in_table = False
                    self.tables.append(self._current_table)

            def handle_data(self, data: str) -> None:
                if self._in_cell:
                    self._current_cell += data

        with open(path, encoding="utf-8") as f:
            content = f.read()

        extractor = _TableExtractor()
        extractor.feed(content)

        if not extractor.tables or self.table_index >= len(extractor.tables):
            return TableModel(columns=[], rows=[])

        raw = extractor.tables[self.table_index]
        if len(raw) < 2:
            return TableModel(columns=[], rows=[])

        columns = raw[0]
        rows = [{col: _parse_attr(val) for col, val in zip(columns, r)} for r in raw[1:]]
        return TableModel(columns=columns, rows=rows)
