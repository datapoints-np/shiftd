"""
06 - Batch conversion: convert multiple files at once.

Uses `Engine.batch()` to convert several source files
into a single output directory with a target format.
"""

from pathlib import Path

from shiftd import Engine

DATA = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "output" / "batch_json"
OUT.mkdir(parents=True, exist_ok=True)

engine = Engine()

sources = [
    str(DATA / "users.csv"),
    str(DATA / "scores.tsv"),
    str(DATA / "cities.toml"),
]

engine.batch(sources, str(OUT), to="json")

print(f"Batch converted {len(sources)} files to JSON")
print(f"Check {OUT}/")
