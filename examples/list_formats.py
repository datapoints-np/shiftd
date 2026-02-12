"""
07 - List all supported formats.

Shows which formats shiftd can read and write.
"""

from shiftd import Engine

engine = Engine()
supported = engine.formats()

print("Readable formats:")
for fmt in sorted(supported["read"]):
    print(f"  - {fmt}")

print("\nWritable formats:")
for fmt in sorted(supported["write"]):
    print(f"  - {fmt}")
