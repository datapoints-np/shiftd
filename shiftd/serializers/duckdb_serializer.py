"""Serialize TableModel to DuckDB. Requires optional dependency: shiftd[duckdb]."""

from __future__ import annotations

from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


def _sanitize_name(name: str) -> str:
    """Use only alphanumeric and underscore for table/column names."""
    return "".join(c if c.isalnum() or c == "_" else "_" for c in name) or "col"


@register_serializer("duckdb")
class DuckDBSerializer:
    """Write TableModel to a DuckDB file. Optional: table name (default 'data')."""

    def __init__(self, table: str = "data", **kwargs: object) -> None:
        self.table = table
        self.kwargs = kwargs

    def serialize(self, table: TableModel, target: Path | str) -> None:
        try:
            import duckdb
        except ImportError as e:
            raise ImportError(
                "DuckDB support requires optional dependency: uv add 'shiftd[duckdb]'"
            ) from e

        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        safe_table = _sanitize_name(self.table)

        conn = duckdb.connect(str(path))
        try:
            conn.execute(f'DROP TABLE IF EXISTS "{safe_table}"')
            if not table.columns and not table.rows:
                conn.execute(f'CREATE TABLE "{safe_table}" (id INTEGER)')
            else:
                columns = [_sanitize_name(c) for c in table.columns]
                col_defs = ", ".join(f'"{c}" VARCHAR' for c in columns)
                conn.execute(f'CREATE TABLE "{safe_table}" ({col_defs})')
                placeholders = ", ".join("?" for _ in columns)
                col_list = ", ".join(f'"{c}"' for c in columns)
                for row in table.rows:
                    values = [
                        str(v) if v is not None else None
                        for v in (row.get(c) for c in table.columns)
                    ]
                    conn.execute(
                        f'INSERT INTO "{safe_table}" ({col_list}) VALUES ({placeholders})',
                        values,
                    )
        finally:
            conn.close()
