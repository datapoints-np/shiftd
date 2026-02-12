"""Serialize TableModel to TSV (tab-separated values)."""

import csv
from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("tsv")
class TSVSerializer:
    """Write TableModel as TSV."""

    def serialize(self, table: TableModel, target: Path | str) -> None:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            if not table.columns:
                return
            writer = csv.DictWriter(f, fieldnames=table.columns, delimiter="\t")
            writer.writeheader()
            writer.writerows(table.rows)
