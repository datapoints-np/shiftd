"""Tests for shiftd. Execute via: uv run python -m tasks.test (or invoke test)."""

import sys
import tempfile
from pathlib import Path

from pydantic import ValidationError
from shiftd import Engine, TableModel
from shiftd.engine import infer_format


def _assert(cond: bool, msg: str = "Assertion failed") -> None:
    if not cond:
        print(f"FAIL: {msg}", file=sys.stderr)
        sys.exit(1)


# -- infer_format -----------------------------------------------------------


def test_infer_format() -> None:
    _assert(infer_format(Path("a.csv")) == "csv")
    _assert(infer_format(Path("b.json")) == "json")
    _assert(infer_format(Path("c.xml")) == "xml")
    _assert(infer_format(Path("x.toml")) == "toml")
    _assert(infer_format(Path("x.yaml")) == "yaml")
    _assert(infer_format(Path("x.yml")) == "yml")
    _assert(infer_format(Path("x.tsv")) == "tsv")
    _assert(infer_format(Path("x.xlsx")) == "xlsx")
    _assert(infer_format(Path("x.parquet")) == "parquet")
    _assert(infer_format(Path("x.toon")) == "toon")
    _assert(infer_format(Path("x.db")) == "sqlite")
    try:
        infer_format(Path("d.txt"))
        _assert(False, "Expected ValueError for .txt")
    except ValueError as e:
        _assert("Unknown extension" in str(e))


# -- Engine.convert ---------------------------------------------------------


def test_convert_csv_to_json() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "sample.csv").write_text("name,age\nAlice,30\nBob,25\n", encoding="utf-8")
        Engine().convert(tmp / "sample.csv", tmp / "out.json")
        _assert((tmp / "out.json").exists(), "output not created")
        _assert("Alice" in (tmp / "out.json").read_text(), "Alice not in output")


def test_convert_json_to_csv() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "sample.json").write_text(
            '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]',
            encoding="utf-8",
        )
        Engine().convert(tmp / "sample.json", tmp / "out.csv")
        lines = (tmp / "out.csv").read_text().strip().splitlines()
        _assert(lines[0] == "name,age")
        _assert("Alice" in lines[1] and "30" in lines[1])


def test_convert_csv_to_xml() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "data.csv").write_text("a,b\n1,2\n", encoding="utf-8")
        Engine().convert(tmp / "data.csv", tmp / "data.xml")
        content = (tmp / "data.xml").read_text()
        _assert("<a>1</a>" in content)


def test_convert_csv_to_toml() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "data.csv").write_text("name,age\nAlice,30\n", encoding="utf-8")
        Engine().convert(tmp / "data.csv", tmp / "data.toml")
        content = (tmp / "data.toml").read_text()
        _assert("[[row]]" in content)
        _assert("Alice" in content)


def test_convert_toml_to_json() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "data.toml").write_text(
            '[[row]]\nname = "Alice"\nage = 30\n\n[[row]]\nname = "Bob"\nage = 25\n',
            encoding="utf-8",
        )
        Engine().convert(tmp / "data.toml", tmp / "data.json")
        content = (tmp / "data.json").read_text()
        _assert("Alice" in content and "Bob" in content)


def test_convert_csv_to_tsv() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "data.csv").write_text("a,b\n1,2\n", encoding="utf-8")
        Engine().convert(tmp / "data.csv", tmp / "data.tsv")
        content = (tmp / "data.tsv").read_text()
        _assert("a\tb" in content)
        _assert("1\t2" in content)


def test_convert_with_explicit_to() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "data.csv").write_text("a,b\n1,2\n", encoding="utf-8")
        Engine().convert(tmp / "data.csv", tmp / "data.json", to="json")
        _assert("1" in (tmp / "data.json").read_text())


# -- Engine.batch -----------------------------------------------------------


def test_batch() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "a.csv").write_text("x\n1\n", encoding="utf-8")
        (tmp / "b.csv").write_text("x\n2\n", encoding="utf-8")
        results = Engine().batch([tmp / "a.csv", tmp / "b.csv"], tmp / "out", to="json")
        _assert(len(results) == 2, "expected 2 results")
        _assert((tmp / "out" / "a.json").exists(), "a.json not created")
        _assert((tmp / "out" / "b.json").exists(), "b.json not created")


# -- Engine.parse / serialize -----------------------------------------------


def test_parse_and_serialize() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "in.csv").write_text("col\nval\n", encoding="utf-8")
        engine = Engine()
        table = engine.parse(tmp / "in.csv")
        _assert(table.columns == ["col"])
        _assert(table.rows == [{"col": "val"}])
        engine.serialize(table, tmp / "out.json")
        _assert((tmp / "out.json").exists())


# -- Engine.formats ---------------------------------------------------------


def test_formats() -> None:
    fmts = Engine.formats()
    _assert("csv" in fmts["read"])
    _assert("json" in fmts["write"])
    _assert("toml" in fmts["read"])
    _assert("tsv" in fmts["write"])


# -- CLI (via main) ---------------------------------------------------------


def test_cli_convert() -> None:
    from shiftd.cli import main

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "sample.csv").write_text("name,age\nAlice,30\n", encoding="utf-8")
        old_argv = sys.argv
        sys.argv = ["shiftd", "convert", str(tmp / "sample.csv"), str(tmp / "out.json")]
        try:
            main()
        finally:
            sys.argv = old_argv
        _assert((tmp / "out.json").exists(), "CLI output not created")


def test_cli_batch() -> None:
    from shiftd.cli import main

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "a.csv").write_text("x\n1\n", encoding="utf-8")
        (tmp / "b.csv").write_text("x\n2\n", encoding="utf-8")
        out = tmp / "batch_out"
        old_argv = sys.argv
        sys.argv = [
            "shiftd",
            "batch",
            "--to",
            "json",
            str(tmp / "a.csv"),
            str(tmp / "b.csv"),
            str(out),
        ]
        try:
            main()
        finally:
            sys.argv = old_argv
        _assert((out / "a.json").exists(), "CLI batch a.json not created")
        _assert((out / "b.json").exists(), "CLI batch b.json not created")


# -- TableModel validation --------------------------------------------------


def test_table_model_valid() -> None:
    t = TableModel(columns=["a", "b"], rows=[{"a": 1, "b": 2}])
    _assert(t.columns == ["a", "b"])


def test_table_model_empty() -> None:
    t = TableModel(columns=[], rows=[])
    _assert(t.columns == [] and t.rows == [])


def test_table_model_extra_key() -> None:
    try:
        TableModel(columns=["a"], rows=[{"a": 1, "b": 2}])
        _assert(False, "Expected ValidationError")
    except ValidationError:
        pass


def test_table_model_missing_key() -> None:
    try:
        TableModel(columns=["a", "b"], rows=[{"a": 1}])
        _assert(False, "Expected ValidationError")
    except ValidationError:
        pass


def test_table_model_duplicate_columns() -> None:
    try:
        TableModel(columns=["a", "a"], rows=[{"a": 1}])
        _assert(False, "Expected ValidationError")
    except ValidationError:
        pass


# -- Runner -----------------------------------------------------------------


def main_tests() -> None:
    test_infer_format()
    test_convert_csv_to_json()
    test_convert_json_to_csv()
    test_convert_csv_to_xml()
    test_convert_csv_to_toml()
    test_convert_toml_to_json()
    test_convert_csv_to_tsv()
    test_convert_with_explicit_to()
    test_batch()
    test_parse_and_serialize()
    test_formats()
    test_cli_convert()
    test_cli_batch()
    test_table_model_valid()
    test_table_model_empty()
    test_table_model_extra_key()
    test_table_model_missing_key()
    test_table_model_duplicate_columns()
    print("All tests passed.")


if __name__ == "__main__":
    main_tests()
