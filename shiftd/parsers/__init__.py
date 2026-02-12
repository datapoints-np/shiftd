"""Parsers: read formats into TableModel."""

import shiftd.parsers.arrow_parser  # noqa: F401
import shiftd.parsers.csv_parser  # noqa: F401
import shiftd.parsers.duckdb_parser  # noqa: F401
import shiftd.parsers.excel_parser  # noqa: F401
import shiftd.parsers.html_parser  # noqa: F401
import shiftd.parsers.json_parser  # noqa: F401
import shiftd.parsers.jsonl_parser  # noqa: F401
import shiftd.parsers.markdown_parser  # noqa: F401
import shiftd.parsers.mysql_parser  # noqa: F401
import shiftd.parsers.parquet_parser  # noqa: F401
import shiftd.parsers.postgres_parser  # noqa: F401
import shiftd.parsers.sqlite_parser  # noqa: F401
import shiftd.parsers.toml_parser  # noqa: F401
import shiftd.parsers.toon_parser  # noqa: F401
import shiftd.parsers.tsv_parser  # noqa: F401
import shiftd.parsers.xml_parser  # noqa: F401
import shiftd.parsers.yaml_parser  # noqa: F401
from shiftd.parsers.registry import get_parser, list_parser_formats

__all__ = ["get_parser", "list_parser_formats"]
