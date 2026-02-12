"""Serialize TableModel to TOON (Token-Oriented Object Notation).

Tabular format: [N]{field1,field2,...}: then N lines of comma-separated values.
"""

from pathlib import Path
from typing import Any

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


def _format_cell(v: Any) -> str:
    """Format one cell for TOON. Quote if contains comma, newline, or quote."""
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        if isinstance(v, float) and (v != v or v == float("inf") or v == float("-inf")):
            return "null"
        return str(v)
    s = str(v)
    if "," in s or "\n" in s or '"' in s:
        s = '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def _to_toon(columns: list[str], rows: list[dict[str, Any]]) -> str:
    """Encode to TOON tabular: [N]{field1,field2,...}: then N data lines."""
    if not columns or not rows:
        return ""
    n = len(rows)
    header = f"[{n}]{{{','.join(columns)}}}:"
    lines = [header]
    for row in rows:
        cells = [_format_cell(row.get(k)) for k in columns]
        lines.append("  " + ",".join(cells))
    return "\n".join(lines)


@register_serializer("toon")
class TOONSerializer:
    def serialize(self, table: TableModel, target: Path | str) -> None:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_to_toon(table.columns, table.rows), encoding="utf-8")
