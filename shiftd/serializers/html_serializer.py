"""Serialize TableModel to an HTML table."""

from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("html")
class HTMLSerializer:
    """Write TableModel as an HTML <table>."""

    def __init__(self, title: str = "Table", **kwargs: object) -> None:
        self.title = title
        self.kwargs = kwargs

    def serialize(self, table: TableModel, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines: list[str] = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"  <title>{self.title}</title>",
            "  <style>",
            "    table { border-collapse: collapse; width: 100%; }",
            "    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "    th { background-color: #f2f2f2; }",
            "    tr:nth-child(even) { background-color: #fafafa; }",
            "  </style>",
            "</head>",
            "<body>",
            "<table>",
        ]
        if table.columns:
            lines.append("  <thead>")
            lines.append("    <tr>")
            for col in table.columns:
                lines.append(f"      <th>{_escape(col)}</th>")
            lines.append("    </tr>")
            lines.append("  </thead>")
        lines.append("  <tbody>")
        for row in table.rows:
            lines.append("    <tr>")
            for col in table.columns:
                val = row.get(col, "")
                lines.append(f"      <td>{_escape(str(val) if val is not None else '')}</td>")
            lines.append("    </tr>")
        lines.append("  </tbody>")
        lines.append("</table>")
        lines.append("</body>")
        lines.append("</html>")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")


def _escape(s: str) -> str:
    """Escape HTML special characters."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
