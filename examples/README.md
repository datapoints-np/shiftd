# shiftd - Examples

This folder contains mock data files and Python scripts that demonstrate how to use **shiftd** for format conversions.

## Mock data (`data/`)

| File | Format | Description |
|------|--------|-------------|
| `users.csv` | CSV | List of users with name, age, email, city, role |
| `products.json` | JSON | Product catalog with prices and categories |
| `cities.toml` | TOML | World cities with population and landmarks |
| `books.yaml` | YAML | Book collection (requires `shiftd[yaml]`) |
| `sensors.xml` | XML | IoT sensor readings |
| `scores.tsv` | TSV | Game leaderboard scores |
| `tasks.toon` | TOON | Task tracker in Token-Oriented Object Notation |
| `movies.db` | SQLite | Movie database with ratings |

## Example scripts

| Script | What it shows |
|--------|---------------|
| `01_basic_conversion.py` | Simple file-to-file conversions (CSV→JSON, JSON→TOML, etc.) |
| `02_parse_and_inspect.py` | Parse a file into `TableModel` and inspect columns/rows |
| `03_tablemodel_from_code.py` | Build a `TableModel` from scratch and export to multiple formats |
| `04_sqlite_conversion.py` | Read/write SQLite databases |
| `05_chain_conversions.py` | Parse once, serialize to every format |
| `06_batch_conversion.py` | Convert multiple files at once with `Engine.batch()` |
| `07_list_formats.py` | List all supported read/write formats |

## Running the examples

```bash
# from the project root
uv run python examples/01_basic_conversion.py
uv run python examples/02_parse_and_inspect.py
# ... etc.
```

Output files will be created in `examples/output/` (git-ignored).
