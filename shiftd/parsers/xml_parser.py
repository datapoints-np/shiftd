"""Parse XML into TableModel."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from shiftd.parsers.registry import register_parser
from shiftd.schema import TableModel


def _elem_to_dict(elem: ET.Element) -> dict[str, Any]:
    d: dict[str, Any] = {}
    if elem.attrib:
        for k, v in elem.attrib.items():
            d[k] = _parse_attr(v)
    for child in elem:
        if len(child) == 0 and (child.text or "").strip():
            d[child.tag] = _parse_attr((child.text or "").strip())
        elif len(child) == 0:
            d[child.tag] = (child.text or "").strip() or None
        else:
            d[child.tag] = _elem_to_dict(child)
    return d


def _parse_attr(v: str) -> Any:
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if v.isdigit():
        return int(v)
    try:
        return float(v)
    except ValueError:
        return v


@register_parser("xml")
class XMLParser:
    """Read XML (root with repeated child elements) into TableModel."""

    def parse(self, path: Path) -> TableModel:
        if not path.exists():
            raise FileNotFoundError(str(path))
        with open(path, encoding="utf-8") as f:
            content = f.read()
        root = ET.fromstring(content)
        rows = [_elem_to_dict(child) for child in root]
        if not rows:
            return TableModel(columns=[], rows=[{}])
        columns = list(rows[0].keys())
        return TableModel(columns=columns, rows=rows)
