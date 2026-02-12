"""Serialize TableModel to Excel (.xlsx). Requires optional dependency: openpyxl."""

from __future__ import annotations

from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("xlsx")
@register_serializer("excel")
class ExcelSerializer:
    """Write TableModel as an Excel file (.xlsx)."""

    def serialize(self, table: TableModel, target: Path | str) -> None:
        try:
            from openpyxl import Workbook
        except ImportError as e:
            raise ImportError(
                "Excel support requires optional dependency: uv add 'shiftd[excel]'"
            ) from e
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        wb = Workbook()
        ws = wb.active
        if table.columns:
            ws.append(table.columns)
            for row in table.rows:
                ws.append([row.get(c) for c in table.columns])
        wb.save(path)
