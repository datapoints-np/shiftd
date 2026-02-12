"""Parse TOON (Token-Oriented Object Notation) into TableModel.

Tabular format: [N]{field1,field2,...}: then N lines of comma-separated values.
"""

import re
from pathlib import Path
from typing import Any

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


def _parse_cell(s: str) -> Any:
    """Parse one TOON cell string to Python type."""
    s = s.strip()
    if s == "" or s.lower() == "null":
        return None
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        return s[1:-1].replace('\\"', '"')
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if s.isdigit():
        return int(s)
    try:
        return float(s)
    except ValueError:
        return s


def _split_row(row_str: str) -> list[str]:
    """Split a TOON row by comma, respecting double-quoted strings."""
    out: list[str] = []
    cur: list[str] = []
    i = 0
    in_quote = False
    while i < len(row_str):
        c = row_str[i]
        if c == '"':
            if in_quote and i + 1 < len(row_str) and row_str[i + 1] == '"':
                cur.append('"')
                i += 2
                continue
            in_quote = not in_quote
            i += 1
            continue
        if c == "," and not in_quote:
            out.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    out.append("".join(cur))
    return out


# Root-level: [N]{fields}:   or   key[N]{fields}:
_TABULAR_HEADER = re.compile(r"^(?:(?P<key>\w+))?\[(?P<n>\d+)\]\{(?P<fields>[^}]+)\}:\s*$")


def _parse_toon_content(content: str) -> list[dict[str, Any]]:
    """Parse TOON tabular format. Returns list of dicts (the array rows)."""
    lines = [ln.rstrip() for ln in content.strip().split("\n") if ln.strip()]
    if not lines:
        return []
    first = lines[0].strip()
    m = _TABULAR_HEADER.match(first)
    if not m:
        return []
    n = int(m.group("n"))
    fields_str = m.group("fields")
    fields = [f.strip() for f in fields_str.split(",")]
    if not fields:
        return []
    result: list[dict[str, Any]] = []
    idx = 1
    for _ in range(n):
        if idx >= len(lines):
            break
        row_str = lines[idx].strip().lstrip()
        idx += 1
        cells = _split_row(row_str)
        row = {
            name: _parse_cell(cells[j]) if j < len(cells) else None for j, name in enumerate(fields)
        }
        result.append(row)
    return result


@register_parser("toon")
class TOONParser:
    """Read TOON file into TableModel."""

    def parse(self, source: Path | str) -> TableModel:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(str(path))
        content = path.read_text(encoding="utf-8")
        rows = _parse_toon_content(content)
        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
