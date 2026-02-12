"""Parse DuckDB databases into TableModel. Requires optional dependency: shiftd[duckdb]."""

from __future__ import annotations

from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("duckdb")
class DuckDBParser:
    """Read a DuckDB table into TableModel. Source: path to .duckdb file."""

    def __init__(self, table: str | None = None, **kwargs: object) -> None:
        self.table = table
        self.kwargs = kwargs

    def parse(self, source: Path | str) -> TableModel:
        try:
            import duckdb
        except ImportError as e:
            raise ImportError(
                "DuckDB support requires optional dependency: uv add 'shiftd[duckdb]'"
            ) from e

        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(str(path))

        conn = duckdb.connect(str(path), read_only=True)
        try:
            if self.table:
                table_name = self.table
            else:
                result = conn.execute(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = 'main' LIMIT 1"
                ).fetchone()
                if not result:
                    return TableModel(columns=[], rows=[])
                table_name = result[0]

            result = conn.execute(f'SELECT * FROM "{table_name}"')
            columns = [desc[0] for desc in result.description]
            raw_rows = result.fetchall()
        finally:
            conn.close()

        if not raw_rows:
            return TableModel(columns=columns, rows=[])
        rows = [dict(zip(columns, row)) for row in raw_rows]
        return TableModel(columns=columns, rows=rows)
