"""Serialize TableModel to YAML. Requires optional dependency: pyyaml."""

from __future__ import annotations

from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("yaml")
@register_serializer("yml")
class YAMLSerializer:
    """Write TableModel as a YAML list of objects."""

    def serialize(self, table: TableModel, target: Path | str) -> None:
        try:
            import yaml
        except ImportError as e:
            raise ImportError(
                "YAML support requires optional dependency: uv add 'shiftd[yaml]'"
            ) from e
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(table.rows, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
