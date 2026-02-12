<p align="center">
  <img src="assets/shiftd_logo.png" alt="shiftd logo">
</p>

# shiftd

[![License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![GitHub stars](https://img.shields.io/github/stars/datapoints-np/shiftd)](https://github.com/datapoints-np/shiftd)
[![GitHub forks](https://img.shields.io/github/forks/datapoints-np/shiftd)](https://github.com/datapoints-np/shiftd)
[![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/datapoints-np/shiftd/main)](https://github.com/datapoints-np/shiftd)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/datapoints-np/shiftd/main)](https://github.com/datapoints-np/shiftd)
[![PyPI version](https://img.shields.io/pypi/v/shiftd.svg)](https://pypi.org/project/shiftd/)
[![Static Badge](https://img.shields.io/badge/data-converter?logo=link&logoColor=white&color=7c6ef6)](https://github.com/datapoints-np/shiftd)

**Any data to any data.**

Convert any data to any data flawless.

## Install

```bash
uv add shiftd
```

## Usage

**Terminal (CLI):**

```bash
shiftd convert input.csv output.json
shiftd convert --to xml input.csv output.xml
shiftd batch --to json file1.csv file2.csv output_dir/
shiftd formats
```

**Python library (Engine):**

```python
from shiftd import Engine, TableModel

engine = Engine()

# Single conversion
engine.convert("data.csv", "data.json")
engine.convert("data.csv", "data.toml", to="toml")

# Batch conversion
engine.batch(["a.csv", "b.csv"], "output/", to="json")

# Parse -> TableModel -> serialize
table = engine.parse("data.csv")
engine.serialize(table, "out.yaml")

# Build a table in code
table = TableModel(columns=["a", "b"], rows=[{"a": 1, "b": 2}])
engine.serialize(table, "out.json")

# List supported formats
engine.formats()  # {'read': [...], 'write': [...]}
```

## Supported formats

| Format | Extension | Dependencies |
|--------|-----------|-------------|
| CSV | `.csv` | — |
| TSV | `.tsv` | — |
| JSON | `.json` | — |
| JSONL | `.jsonl` `.ndjson` | — |
| XML | `.xml` | — |
| HTML | `.html` | — |
| Markdown | `.md` `.markdown` | — |
| TOML | `.toml` | — |
| YAML | `.yaml` `.yml` | `uv add 'shiftd[yaml]'` |
| Parquet | `.parquet` | `uv add 'shiftd[arrow]'` |
| Arrow | `.arrow` | `uv add 'shiftd[arrow]'` |
| Excel | `.xlsx` | `uv add 'shiftd[excel]'` |
| SQLite | `.sqlite` `.db` | — |
| DuckDB | `.duckdb` | `uv add 'shiftd[duckdb]'` |
| PostgreSQL | connection string | `uv add 'shiftd[postgres]'` |
| MySQL | connection string | `uv add 'shiftd[mysql]'` |
| TOON | `.toon` | — |

## Development

Development uses **Python 3.13** and **[Ruff](https://docs.astral.sh/ruff/)** (format + lint).

```bash
# Clone and enter project
cd shiftd

# Create env and install deps (including dev)
uv sync

# Format and lint
uv run inv format
uv run inv lint

# Run tests
uv run inv test
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=datapoints-np/shiftd&type=Date)](https://star-history.com/#datapoints-np/shiftd&Date)

## License

AGPL-3.0-or-later.
