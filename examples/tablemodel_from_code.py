"""
03 - Build a TableModel from scratch in Python and serialize it.

You don't need a source file: create data programmatically
and export to any format.
"""

from pathlib import Path

from shiftd import Engine, TableModel

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

engine = Engine()

# Build a table by hand
table = TableModel(
    columns=["language", "creator", "year", "paradigm"],
    rows=[
        {
            "language": "Python",
            "creator": "Guido van Rossum",
            "year": 1991,
            "paradigm": "multi-paradigm",
        },
        {"language": "Rust", "creator": "Graydon Hoare", "year": 2010, "paradigm": "systems"},
        {"language": "Go", "creator": "Rob Pike et al.", "year": 2009, "paradigm": "concurrent"},
        {
            "language": "TypeScript",
            "creator": "Anders Hejlsberg",
            "year": 2012,
            "paradigm": "multi-paradigm",
        },
        {"language": "Zig", "creator": "Andrew Kelley", "year": 2015, "paradigm": "systems"},
    ],
)

# Export to multiple formats
engine.serialize(table, str(OUT / "languages.csv"))
engine.serialize(table, str(OUT / "languages.json"))
engine.serialize(table, str(OUT / "languages.xml"))
engine.serialize(table, str(OUT / "languages.toml"))
engine.serialize(table, str(OUT / "languages.toon"))

print("TableModel serialized to CSV, JSON, XML, TOML, TOON")
print(f"Check {OUT}/")
