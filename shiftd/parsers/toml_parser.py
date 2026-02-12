"""Parse TOML into TableModel. Uses stdlib tomllib (Python 3.11+)."""

import tomllib
from pathlib import Path
from typing import Any

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


def _find_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Find the first list-of-dicts in the TOML structure."""
    # Top-level list of dicts (e.g. [[row]] or [[items]])
    for v in data.values():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
    # Flat dict -> single row
    if data:
        return [data]
    return []


@register_parser("toml")
class TOMLParser:
    """Read TOML file into TableModel.

    Expects an array of tables (e.g. ``[[row]]``) or a flat dict (single row).
    """

    def parse(self, source: Path | str) -> TableModel:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(str(path))
        with open(path, "rb") as f:
            data = tomllib.load(f)
        rows = _find_rows(data)
        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
