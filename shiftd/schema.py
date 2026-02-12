"""Pydantic models for validated tabular data."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, field_validator


class TableModel(BaseModel):
    """Validated table: columns and rows. Every row must have exactly the column keys."""

    columns: list[str]
    rows: list[dict[str, Any]]

    @field_validator("columns")
    @classmethod
    def columns_unique(cls, v: list[str]) -> list[str]:
        if v and len(v) != len(set(v)):
            raise ValueError("columns must be unique")
        return v

    @field_validator("rows", mode="after")
    @classmethod
    def rows_match_columns(cls, rows: list[dict[str, Any]], info: Any) -> list[dict[str, Any]]:
        columns = info.data.get("columns")
        if not columns:
            return rows
        for i, row in enumerate(rows):
            if not isinstance(row, dict):
                raise ValueError(f"row {i} must be a dict")
            keys = set(row.keys())
            expected = set(columns)
            if keys != expected:
                missing = expected - keys
                extra = keys - expected
                msg = f"row {i}: columns mismatch"
                if missing:
                    msg += f"; missing: {sorted(missing)}"
                if extra:
                    msg += f"; extra: {sorted(extra)}"
                raise ValueError(msg)
        return rows
