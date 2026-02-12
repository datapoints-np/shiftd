"""Parse MySQL databases into TableModel. Requires optional dependency: shiftd[mysql]."""

from __future__ import annotations

from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("mysql")
class MySQLParser:
    """Read a MySQL table into TableModel.

    Source should be a connection string: ``mysql://user:pass@host:port/dbname``
    or a path to a file containing the connection string.
    """

    def __init__(self, table: str | None = None, **kwargs: object) -> None:
        self.table = table
        self.kwargs = kwargs

    def parse(self, source: Path | str) -> TableModel:
        try:
            import pymysql
        except ImportError as e:
            raise ImportError(
                "MySQL support requires optional dependency: uv add 'shiftd[mysql]'"
            ) from e

        dsn = self._resolve_dsn(source)
        conn_params = self._parse_dsn(dsn)
        conn = pymysql.connect(
            **conn_params,
            cursorclass=pymysql.cursors.DictCursor,
            **self.kwargs,
        )
        try:
            with conn.cursor() as cur:
                if self.table:
                    table_name = self.table
                else:
                    cur.execute("SHOW TABLES")
                    row = cur.fetchone()
                    if not row:
                        return TableModel(columns=[], rows=[])
                    table_name = list(row.values())[0]

                cur.execute(f"SELECT * FROM `{table_name}`")
                rows = list(cur.fetchall())
        finally:
            conn.close()

        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)

    @staticmethod
    def _resolve_dsn(source: Path | str) -> str:
        """If source is a file path, read the DSN from it; otherwise treat as DSN string."""
        p = Path(source)
        if p.exists() and p.is_file():
            return p.read_text().strip()
        return str(source)

    @staticmethod
    def _parse_dsn(dsn: str) -> dict:
        """Parse ``mysql://user:pass@host:port/dbname`` into connection kwargs."""
        from urllib.parse import urlparse

        parsed = urlparse(dsn)
        return {
            "host": parsed.hostname or "localhost",
            "port": parsed.port or 3306,
            "user": parsed.username or "root",
            "password": parsed.password or "",
            "database": (parsed.path or "/").lstrip("/"),
        }
