"""Parse Parquet files into TableModel. Requires optional dependency: shiftd[arrow]."""

from __future__ import annotations

from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("parquet")
class ParquetParser:
    """Read Parquet file into TableModel."""

    def parse(self, source: Path | str) -> TableModel:
        try:
            import pyarrow.parquet as pq
        except ImportError as e:
            raise ImportError(
                "Parquet support requires optional dependency: uv add 'shiftd[arrow]'"
            ) from e
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(str(path))
        table = pq.read_table(path)
        if table.num_rows == 0 and table.num_columns == 0:
            return TableModel(columns=[], rows=[])
        columns = table.column_names
        rows = table.to_pylist()
        return TableModel(columns=columns, rows=rows)
