"""Serialize TableModel to TOML. No external deps (manual formatting)."""

from pathlib import Path
from typing import Any

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


def _format_value(v: Any) -> str:
    """Format a Python value as a TOML literal."""
    if v is None:
        return '""'
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return str(v)
    # String — escape backslashes and quotes
    s = str(v).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def _format_key(k: str) -> str:
    """Quote key if it contains non-bare characters."""
    if k.isidentifier() and k.isascii():
        return k
    return f'"{k}"'


@register_serializer("toml")
class TOMLSerializer:
    """Write TableModel as TOML array of tables (``[[row]]``)."""

    def __init__(self, table_name: str = "row") -> None:
        self.table_name = table_name

    def serialize(self, table: TableModel, target: Path | str) -> None:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines: list[str] = []
        for row in table.rows:
            lines.append(f"[[{self.table_name}]]")
            for col in table.columns:
                lines.append(f"{_format_key(col)} = {_format_value(row.get(col))}")
            lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")
