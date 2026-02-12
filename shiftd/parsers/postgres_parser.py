"""Parse PostgreSQL tables into TableModel. Requires optional dependency: shiftd[postgres]."""

from __future__ import annotations

from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("postgres")
@register_parser("postgresql")
class PostgresParser:
    """Read a PostgreSQL table into TableModel. Source: connection string. Optional: table name."""

    def __init__(self, table: str | None = None, **kwargs: object) -> None:
        self.table = table
        self.kwargs = kwargs

    def parse(self, source: Path | str) -> TableModel:
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
        except ImportError as e:
            raise ImportError(
                "PostgreSQL support requires optional dependency: uv add 'shiftd[postgres]'"
            ) from e
        dsn = str(source)
        conn = psycopg2.connect(dsn, **self.kwargs)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            if self.table:
                cur.execute(f'SELECT * FROM "{self.table}"')
            else:
                cur.execute(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = 'public' AND table_type = 'BASE TABLE' LIMIT 1"
                )
                row = cur.fetchone()
                if not row:
                    conn.close()
                    return TableModel(columns=[], rows=[])
                cur.execute(f'SELECT * FROM "{row["table_name"]}"')
            rows = [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()
        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
