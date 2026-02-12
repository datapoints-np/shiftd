"""Serialize TableModel to MySQL. Requires optional dependency: shiftd[mysql]."""

from __future__ import annotations

from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


def _sanitize_name(name: str) -> str:
    """Use only alphanumeric and underscore for table/column names."""
    return "".join(c if c.isalnum() or c == "_" else "_" for c in name) or "col"


@register_serializer("mysql")
class MySQLSerializer:
    """Write TableModel to a MySQL database.

    Target should be a connection string: ``mysql://user:pass@host:port/dbname``
    or a path to a file containing the connection string.
    """

    def __init__(self, table: str = "data", **kwargs: object) -> None:
        self.table = table
        self.kwargs = kwargs

    def serialize(self, table: TableModel, target: Path | str) -> None:
        try:
            import pymysql
        except ImportError as e:
            raise ImportError(
                "MySQL support requires optional dependency: uv add 'shiftd[mysql]'"
            ) from e

        dsn = self._resolve_dsn(target)
        conn_params = self._parse_dsn(dsn)
        safe_table = _sanitize_name(self.table)

        conn = pymysql.connect(**conn_params, **self.kwargs)
        try:
            with conn.cursor() as cur:
                cur.execute(f"DROP TABLE IF EXISTS `{safe_table}`")
                if not table.columns and not table.rows:
                    cur.execute(f"CREATE TABLE `{safe_table}` (id INT AUTO_INCREMENT PRIMARY KEY)")
                else:
                    columns = [_sanitize_name(c) for c in table.columns]
                    col_defs = ", ".join(f"`{c}` TEXT" for c in columns)
                    cur.execute(f"CREATE TABLE `{safe_table}` ({col_defs})")
                    placeholders = ", ".join("%s" for _ in columns)
                    col_list = ", ".join(f"`{c}`" for c in columns)
                    for row in table.rows:
                        values = [
                            str(v) if v is not None else None
                            for v in (row.get(c) for c in table.columns)
                        ]
                        cur.execute(
                            f"INSERT INTO `{safe_table}` ({col_list}) VALUES ({placeholders})",
                            values,
                        )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _resolve_dsn(target: Path | str) -> str:
        """If target is a file path, read the DSN from it; otherwise treat as DSN string."""
        p = Path(target)
        if p.exists() and p.is_file():
            return p.read_text().strip()
        return str(target)

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
