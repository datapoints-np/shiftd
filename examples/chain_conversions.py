"""
05 - Chain conversions through multiple formats.

Parse once, serialize many times - demonstrates the power
of the intermediate TableModel representation.
"""

from pathlib import Path

from shiftd import Engine

DATA = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

engine = Engine()

# Start from CSV
table = engine.parse(str(DATA / "users.csv"))
print(f"Parsed {len(table.rows)} rows from users.csv\n")

# Serialize the same data to every supported format
formats = {
    "csv": "users_chain.csv",
    "json": "users_chain.json",
    "toml": "users_chain.toml",
    "xml": "users_chain.xml",
    "tsv": "users_chain.tsv",
    "toon": "users_chain.toon",
}

for fmt, filename in formats.items():
    engine.serialize(table, str(OUT / filename))
    print(f"  → {fmt:5s}  {filename}")

print(f"\nAll chain conversions completed! Check {OUT}/")
