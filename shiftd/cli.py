"""CLI for shiftd"""

from __future__ import annotations

import sys
from pathlib import Path

from shiftd.engine import Engine

USAGE = """\
Usage:
  shiftd convert [--to FORMAT] INPUT OUTPUT
  shiftd batch   --to FORMAT   INPUT [INPUT ...] OUTPUT_DIR
  shiftd formats
"""


def _die(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


def _pop_flag(args: list[str], flag: str) -> tuple[str | None, list[str]]:
    """Extract a --flag VALUE pair from args, return (value, remaining_args)."""
    if flag not in args:
        return None, args
    idx = args.index(flag)
    if idx + 1 >= len(args):
        _die(f"{flag} requires a value")
    value = args[idx + 1].lower()
    return value, args[:idx] + args[idx + 2 :]


def _cmd_convert(args: list[str]) -> None:
    to, args = _pop_flag(args, "--to")
    if len(args) != 2:
        _die(USAGE)
    source, target = Path(args[0]), Path(args[1])
    if not source.exists():
        _die(f"Input not found: {source}")
    Engine().convert(source, target, to=to)
    print(f"Converted {source} -> {target}")


def _cmd_batch(args: list[str]) -> None:
    to, args = _pop_flag(args, "--to")
    if not to:
        _die("batch requires --to FORMAT")
    if len(args) < 2:
        _die("batch requires at least one INPUT and an OUTPUT_DIR")
    *inputs, output_dir = args
    sources = [Path(p) for p in inputs]
    for s in sources:
        if not s.exists():
            _die(f"Input not found: {s}")
    results = Engine().batch(sources, output_dir, to=to)
    for r in results:
        print(f"  -> {r}")
    print(f"Converted {len(results)} file(s)")


def _cmd_formats() -> None:
    fmts = Engine.formats()
    print(f"Read:  {', '.join(fmts['read'])}")
    print(f"Write: {', '.join(fmts['write'])}")


def main() -> None:
    if len(sys.argv) < 2:
        _die(USAGE)
    cmd, args = sys.argv[1], sys.argv[2:]
    match cmd:
        case "convert":
            _cmd_convert(args)
        case "batch":
            _cmd_batch(args)
        case "formats":
            _cmd_formats()
        case _:
            _die(USAGE)


if __name__ == "__main__":
    main()
