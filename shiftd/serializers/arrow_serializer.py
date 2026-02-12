"""Serialize TableModel to Arrow IPC. Requires optional dependency: shiftd[arrow]."""

from __future__ import annotations

from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("arrow")
class ArrowSerializer:
    def serialize(self, table: TableModel, target: str | Path) -> None:
        try:
            import pyarrow as pa
            import pyarrow.ipc as ipc
        except ImportError as e:
            raise ImportError(
                "Arrow support requires optional dependency: uv add 'shiftd[arrow]'"
            ) from e
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not table.columns and not table.rows:
            pa_table = pa.table({})
        else:
            pa_table = pa.Table.from_pylist(table.rows)
        with pa.OSFile(str(path), "wb") as f:
            writer = ipc.new_file(f, pa_table.schema)
            writer.write_table(pa_table)
            writer.close()
