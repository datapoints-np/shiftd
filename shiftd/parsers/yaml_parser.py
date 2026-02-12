"""Parse YAML into TableModel. Requires optional dependency: pyyaml."""

from __future__ import annotations

from pathlib import Path

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


@register_parser("yaml")
@register_parser("yml")
class YAMLParser:
    """Read YAML file into TableModel. Expects a list of objects or a single object."""

    def parse(self, source: Path | str) -> TableModel:
        try:
            import yaml
        except ImportError as e:
            raise ImportError(
                "YAML support requires optional dependency: uv add 'shiftd[yaml]'"
            ) from e
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(str(path))
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if isinstance(data, list):
            rows = [dict(r) for r in data if isinstance(r, dict)]
        elif isinstance(data, dict):
            rows = [data]
        else:
            rows = []
        if not rows:
            return TableModel(columns=[], rows=[])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
