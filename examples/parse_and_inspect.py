"""
02 - Parse a file and inspect the intermediate TableModel.

Useful for debugging or previewing data before serializing.
"""

from pathlib import Path

from shiftd import Engine

DATA = Path(__file__).parent / "data"

engine = Engine()

# Parse CSV into a TableModel
table = engine.parse(str(DATA / "users.csv"))

print("Columns:", table.columns)
print(f"Rows:    {len(table.rows)}\n")

for row in table.rows:
    print(row)

# You can also access individual fields
print(f"\nFirst user: {table.rows[0]['name']} from {table.rows[0]['city']}")
