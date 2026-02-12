"""Serialize TableModel to Parquet. Requires optional dependency: shiftd[arrow]."""

from __future__ import annotations

from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("parquet")
class ParquetSerializer:
    def serialize(self, table: TableModel, target: str | Path) -> None:
        try:
            import pyarrow as pa
            import pyarrow.parquet as pq
        except ImportError as e:
            raise ImportError(
                "Parquet support requires optional dependency: uv add 'shiftd[arrow]'"
            ) from e
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not table.columns and not table.rows:
            pa_table = pa.table({})
        else:
            pa_table = pa.Table.from_pylist(table.rows)
        pq.write_table(pa_table, str(path))
