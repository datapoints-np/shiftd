"""Serialize TableModel to CSV."""

import csv
from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


@register_serializer("csv")
class CSVSerializer:
    def serialize(self, table: TableModel, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            if not table.columns:
                return
            writer = csv.DictWriter(f, fieldnames=table.columns)
            writer.writeheader()
            writer.writerows(table.rows)
