"""Serialize TableModel to a Markdown table."""

from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("markdown")
class MarkdownSerializer:
    """Write TableModel as a Markdown table."""

    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs

    def serialize(self, table: TableModel, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not table.columns:
            with open(path, "w", encoding="utf-8") as f:
                f.write("")
            return

        lines: list[str] = []
        # Header
        header = "| " + " | ".join(table.columns) + " |"
        lines.append(header)
        # Separator
        sep = "| " + " | ".join("---" for _ in table.columns) + " |"
        lines.append(sep)
        # Data rows
        for row in table.rows:
            vals = [str(row.get(c, "")) if row.get(c) is not None else "" for c in table.columns]
            lines.append("| " + " | ".join(vals) + " |")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
