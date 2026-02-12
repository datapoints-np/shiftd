"""Serialize TableModel to XML."""

import xml.etree.ElementTree as ET
from pathlib import Path

from shiftd.schema import TableModel
from shiftd.serializers.registry import register_serializer


def _dict_to_elem(parent: ET.Element, tag: str, value: object) -> None:
    if isinstance(value, dict):
        child = ET.SubElement(parent, tag)
        for k, v in value.items():
            _dict_to_elem(child, k, v)
    elif value is not None:
        child = ET.SubElement(parent, tag)
        child.text = str(value)


@register_serializer("xml")
class XMLSerializer:
    def __init__(self, root_tag: str = "root", row_tag: str = "row") -> None:
        self.root_tag = root_tag
        self.row_tag = row_tag

    def serialize(self, table: TableModel, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        root = ET.Element(self.root_tag)
        for row in table.rows:
            row_el = ET.SubElement(root, self.row_tag)
            for col in table.columns:
                _dict_to_elem(row_el, col, row.get(col))
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(path, encoding="utf-8", xml_declaration=True, default_namespace="")
