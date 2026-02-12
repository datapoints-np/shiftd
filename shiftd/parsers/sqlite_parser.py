"""Parse SQLite databases into TableModel. Reads one table (by name or first available)."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("sqlite")
class SQLiteParser:
    """Read a SQLite table into TableModel. Source: path to .db file. Optional: table name."""

    def __init__(self, table: str | None = None, **kwargs: object) -> None:
        self.table = table
        self.kwargs = kwargs

    def parse(self, source: Path | str) -> TableModel:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(str(path))
        db_path = str(path)
        conn = sqlite3.connect(db_path, **self.kwargs)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            if self.table:
                cur.execute(f'SELECT * FROM "{self.table}"')
            else:
                cur.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
                row = cur.fetchone()
                if not row:
                    conn.close()
                    return TableModel(columns=[], rows=[])
                cur.execute(f'SELECT * FROM "{row[0]}"')
            rows = [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()
        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
