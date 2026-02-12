# Contributing to shiftd

Thanks for your interest in contributing to **shiftd**! This guide will help you get up and running.

## Prerequisites

- **Python 3.13+**
- [**uv**](https://docs.astral.sh/uv/) - fast Python package & project manager
- [**Ruff**](https://docs.astral.sh/ruff/) - linter and formatter (installed automatically as dev dependency)

## Setup

1. **Fork and clone** the repository:

   ```bash
   git clone https://github.com/<your-username>/shiftd.git
   cd shiftd
   ```

2. **Install dependencies** with uv:

   ```bash
   uv sync                  # core dependencies
   uv sync --all-extras     # include all optional formats (arrow, excel, yaml, postgres, llm-*)
   ```

   This creates a virtual environment and installs everything you need.

3. **Verify** the setup:

   ```bash
   uv run shiftd formats
   ```

## Development workflow

### Running the project

```bash
uv run shiftd convert input.csv output.json
uv run python examples/01_basic_conversion.py
```

### Code style - Ruff

We use **Ruff** for both linting and formatting. The configuration lives in `pyproject.toml`:

- Line length: **100**
- Target: **Python 3.13**
- Quote style: **double**
- Lint rules: `E`, `F`, `I`, `N`, `W`, `UP`

**Check for lint errors:**

```bash
uv run ruff check shiftd tasks
```

**Auto-fix lint errors:**

```bash
uv run ruff check --fix shiftd tasks
```

**Format code:**

```bash
uv run ruff format shiftd tasks
```

> **Tip:** you can also use [Invoke](https://www.pyinvoke.org/) shortcuts:
>
> ```bash
> uv run invoke lint
> uv run invoke format
> ```

Please make sure `ruff check` and `ruff format --check` pass before opening a PR.

### Running tests

```bash
uv run invoke test
```

or directly:

```bash
uv run python -m tasks.test
```

## Adding a new format

shiftd uses a registry-based plugin system. To add support for a new format:

1. **Create a parser** in `shiftd/parsers/` (e.g. `my_format_parser.py`):

   ```python
   from shiftd.parsers.registry import register_parser
   from shiftd.schema import TableModel

   @register_parser("my_format")
   class MyFormatParser:
       def parse(self, source: str) -> TableModel:
           # Read source file and return a TableModel
           ...
   ```

2. **Create a serializer** in `shiftd/serializers/` (e.g. `my_format_serializer.py`):

   ```python
   from shiftd.serializers.registry import register_serializer
   from shiftd.schema import TableModel

   @register_serializer("my_format")
   class MyFormatSerializer:
       def serialize(self, table: TableModel, target: str) -> None:
           # Write the TableModel to target file
           ...
   ```

3. **Register the file extension** in `shiftd/engine.py` by adding an entry to `_EXT_TO_FORMAT`.

4. **Import** the new modules in `shiftd/parsers/__init__.py` and `shiftd/serializers/__init__.py`.

5. If the format requires an external library, add it as an **optional dependency** in `pyproject.toml`:

   ```toml
   [project.optional-dependencies]
   my_format = ["some-library>=1.0.0"]
   ```

6. **Add tests** and an example in `examples/`.

## Project structure

```
shiftd/
├── shiftd/
│   ├── __init__.py          # Public API: Engine, TableModel
│   ├── cli.py               # CLI entry point
│   ├── engine.py            # Core conversion engine
│   ├── schema.py            # TableModel (Pydantic)
│   ├── parsers/             # One file per input format
│   │   ├── registry.py      # @register_parser decorator
│   │   └── *_parser.py
│   └── serializers/         # One file per output format
│       ├── registry.py      # @register_serializer decorator
│       └── *_serializer.py
├── examples/                # Usage examples + mock data
├── tasks/                   # Invoke tasks (test, lint, format)
└── pyproject.toml
```

## Submitting a Pull Request

1. Create a **feature branch** from `main`:

   ```bash
   git checkout -b feat/my-awesome-feature
   ```

2. Make your changes and ensure:
   - `uv run ruff check shiftd tasks` reports no errors
   - `uv run ruff format --check shiftd tasks` reports no changes needed
   - `uv run invoke test` passes

3. **Commit** with a clear message:

   ```bash
   git commit -m "feat: add support for XYZ format"
   ```

4. **Push** and open a PR against `main`.

## Commit message convention

We follow a lightweight convention:

| Prefix | Use case |
|--------|----------|
| `feat:` | New feature or format |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code restructuring (no behavior change) |
| `test:` | Adding or updating tests |
| `chore:` | Tooling, CI, dependencies |

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
