"""Serialize TableModel to SQLite. Writes one table (default name: data)."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


def _sanitize_name(name: str) -> str:
    """Use only alphanumeric and underscore for table/column names."""
    return "".join(c if c.isalnum() or c == "_" else "_" for c in name) or "col"


@register_serializer("sqlite")
class SQLiteSerializer:
    """Write TableModel to a SQLite file. Optional: table name (default 'data')."""

    def __init__(self, table: str = "data", **kwargs: object) -> None:
        self.table = table
        self.kwargs = kwargs

    def serialize(self, table: TableModel, target: Path | str) -> None:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        safe_table = _sanitize_name(self.table)
        conn = sqlite3.connect(str(path), **self.kwargs)
        cur = conn.cursor()
        try:
            cur.execute(f'DROP TABLE IF EXISTS "{safe_table}"')
            if not table.columns and not table.rows:
                cur.execute(f'CREATE TABLE "{safe_table}" (id INTEGER PRIMARY KEY)')
            else:
                columns = [_sanitize_name(c) for c in table.columns]
                col_list = ", ".join(f'"{c}"' for c in columns)
                cur.execute(f'CREATE TABLE "{safe_table}" ({col_list})')
                placeholders = ", ".join("?" for _ in columns)
                for row in table.rows:
                    values = [row.get(c) for c in table.columns]
                    cur.execute(
                        f'INSERT INTO "{safe_table}" ({col_list}) VALUES ({placeholders})',
                        values,
                    )
            conn.commit()
        finally:
            conn.close()
