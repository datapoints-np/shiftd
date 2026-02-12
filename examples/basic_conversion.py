"""
01 - Basic conversion between formats.

Shows the simplest way to convert a file from one format to another
using `Engine.convert()`.
"""

from pathlib import Path

from shiftd import Engine

DATA = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

engine = Engine()

# CSV → JSON
engine.convert(str(DATA / "users.csv"), str(OUT / "users.json"))
print("CSV  → JSON  ✔")

# JSON → TOML
engine.convert(str(DATA / "products.json"), str(OUT / "products.toml"))
print("JSON → TOML  ✔")

# TOML → CSV
engine.convert(str(DATA / "cities.toml"), str(OUT / "cities.csv"))
print("TOML → CSV   ✔")

# XML → JSON
engine.convert(str(DATA / "sensors.xml"), str(OUT / "sensors.json"))
print("XML  → JSON  ✔")

# TSV → CSV
engine.convert(str(DATA / "scores.tsv"), str(OUT / "scores.csv"))
print("TSV  → CSV   ✔")

# TOON → JSON
engine.convert(str(DATA / "tasks.toon"), str(OUT / "tasks.json"))
print("TOON → JSON  ✔")

print("\nAll basic conversions completed! Check examples/output/")
