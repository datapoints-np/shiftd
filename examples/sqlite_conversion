"""
04 - Convert to and from SQLite.

Demonstrates reading from a local SQLite database
and writing data into a new one.
"""

from pathlib import Path

from shiftd import Engine

DATA = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

engine = Engine()

# SQLite → JSON  (read from the mock movies database)
engine.convert(str(DATA / "movies.db"), str(OUT / "movies.json"))
print("SQLite → JSON  ✔")

# SQLite → CSV
engine.convert(str(DATA / "movies.db"), str(OUT / "movies.csv"))
print("SQLite → CSV   ✔")

# CSV → SQLite  (write users into a new database)
engine.convert(str(DATA / "users.csv"), str(OUT / "users.db"))
print("CSV    → SQLite ✔")

# JSON → SQLite
engine.convert(str(DATA / "products.json"), str(OUT / "products.db"))
print("JSON   → SQLite ✔")

print("\nSQLite conversions completed! Check examples/output/")
