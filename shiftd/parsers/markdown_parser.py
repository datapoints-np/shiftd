"""Parse Markdown tables into TableModel."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


def _parse_value(v: str) -> Any:
    """Try to coerce string values to int/float/bool."""
    v = v.strip()
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if v.isdigit():
        return int(v)
    try:
        return float(v)
    except ValueError:
        return v


def _parse_row(line: str) -> list[str]:
    """Split a Markdown table row into cell values."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def _is_separator(line: str) -> bool:
    """Check if a line is a Markdown table separator (|---|---|)."""
    stripped = line.strip().replace("|", "").replace("-", "").replace(":", "").strip()
    return stripped == ""


@register_parser("markdown")
class MarkdownParser:
    """Read the first Markdown table from a file into TableModel."""

    def parse(self, path: Path) -> TableModel:
        if not path.exists():
            raise FileNotFoundError(str(path))
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()

        # Find table lines (lines containing |)
        table_lines: list[str] = []
        in_table = False
        for line in lines:
            stripped = line.strip()
            if "|" in stripped:
                in_table = True
                table_lines.append(stripped)
            elif in_table:
                break  # End of table

        if len(table_lines) < 2:
            return TableModel(columns=[], rows=[])

        # First line: headers
        columns = _parse_row(table_lines[0])

        # Skip separator line(s), parse data rows
        rows: list[dict[str, Any]] = []
        for line in table_lines[1:]:
            if _is_separator(line):
                continue
            values = _parse_row(line)
            row = {col: _parse_value(val) for col, val in zip(columns, values)}
            rows.append(row)

        if not rows:
            return TableModel(columns=[], rows=[])
        return TableModel(columns=columns, rows=rows)
