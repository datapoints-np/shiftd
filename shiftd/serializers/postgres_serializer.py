"""Serialize TableModel to PostgreSQL. Requires optional dependency: shiftd[postgres]."""

from __future__ import annotations

from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


def _sanitize_name(name: str) -> str:
    """Use only alphanumeric and underscore for identifiers."""
    return "".join(c if c.isalnum() or c == "_" else "_" for c in name) or "col"


@register_serializer("postgres")
@register_serializer("postgresql")
class PostgresSerializer:
    """Write TableModel to a PostgreSQL table. Target: connection string. Optional: table name."""

    def __init__(self, table: str = "data", **kwargs: object) -> None:
        self.table = table
        self.kwargs = kwargs

    def serialize(self, table: TableModel, target: Path | str) -> None:
        try:
            import psycopg2
        except ImportError as e:
            raise ImportError(
                "PostgreSQL support requires optional dependency: uv add 'shiftd[postgres]'"
            ) from e
        dsn = str(target)
        safe_table = _sanitize_name(self.table)
        conn = psycopg2.connect(dsn, **self.kwargs)
        cur = conn.cursor()
        try:
            cur.execute(f'DROP TABLE IF EXISTS "{safe_table}"')
            if not table.columns and not table.rows:
                cur.execute(f'CREATE TABLE "{safe_table}" (id SERIAL PRIMARY KEY)')
            else:
                cols = [f'"{_sanitize_name(c)}" TEXT' for c in table.columns]
                cur.execute(f'CREATE TABLE "{safe_table}" ({", ".join(cols)})')
                for row in table.rows:
                    values = [row.get(c) for c in table.columns]
                    placeholders = ", ".join("%s" for _ in table.columns)
                    col_list = ", ".join(f'"{_sanitize_name(c)}"' for c in table.columns)
                    cur.execute(
                        f'INSERT INTO "{safe_table}" ({col_list}) VALUES ({placeholders})',
                        values,
                    )
            conn.commit()
        finally:
            conn.close()
