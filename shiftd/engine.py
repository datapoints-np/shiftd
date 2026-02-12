"""Engine: the core of shiftd. Use from Python or from the CLI."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from shiftd.parsers import get_parser, list_parser_formats
from shiftd.schema import TableModel
from shiftd.serializers import get_serializer, list_serializer_formats

# Extension -> format name (lowercase, without dot)
_EXT_TO_FORMAT: dict[str, str] = {
    "csv": "csv",
    "tsv": "tsv",
    "json": "json",
    "jsonl": "jsonl",
    "ndjson": "jsonl",
    "xml": "xml",
    "html": "html",
    "md": "markdown",
    "markdown": "markdown",
    "toml": "toml",
    "yaml": "yaml",
    "yml": "yml",
    "parquet": "parquet",
    "arrow": "arrow",
    "xlsx": "xlsx",
    "toon": "toon",
    "db": "sqlite",
    "sqlite": "sqlite",
    "duckdb": "duckdb",
}


def infer_format(path: Path | str) -> str:
    """Infer format name from file extension."""
    ext = Path(path).suffix.lower().lstrip(".")
    if ext not in _EXT_TO_FORMAT:
        raise ValueError(f"Unknown extension '.{ext}'. Supported: {sorted(_EXT_TO_FORMAT)}")
    return _EXT_TO_FORMAT[ext]


@dataclass
class Engine:
    """Any data to any data.

    >>> engine = Engine()
    >>> engine.convert("data.csv", "data.json")
    >>> engine.batch(["a.csv", "b.csv"], "output/", to="json")
    """

    def convert(
        self,
        source: str | Path,
        target: str | Path,
        *,
        to: str | None = None,
    ) -> Path:
        """Convert a single file. Output format inferred from extension or set with ``to``."""
        source, target = Path(source), Path(target)
        table = get_parser(infer_format(source))().parse(source)
        get_serializer(to or infer_format(target))().serialize(table, target)
        return target

    def batch(
        self,
        sources: Sequence[str | Path],
        output_dir: str | Path,
        *,
        to: str,
    ) -> list[Path]:
        """Convert multiple files to the same output format."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        return [self.convert(src, output_dir / f"{Path(src).stem}.{to}", to=to) for src in sources]

    def parse(self, source: str | Path, *, format: str | None = None) -> TableModel:
        """Read a file into a validated TableModel."""
        source = Path(source)
        return get_parser(format or infer_format(source))().parse(source)

    def serialize(
        self,
        table: TableModel,
        target: str | Path,
        *,
        format: str | None = None,
    ) -> Path:
        """Write a TableModel to a file."""
        target = Path(target)
        get_serializer(format or infer_format(target))().serialize(table, target)
        return target

    @staticmethod
    def formats() -> dict[str, list[str]]:
        """Supported formats for reading and writing."""
        return {"read": list_parser_formats(), "write": list_serializer_formats()}
