"""Invoke tasks for shiftd development."""

from invoke import task


@task
def test(c):
    """Run tests."""
    c.run("uv run python -m tasks.test", pty=True)


@task
def lint(c):
    """Run ruff check on shiftd and tasks."""
    c.run("uv run ruff check shiftd tasks", pty=True)


@task
def format(c):
    """Run ruff format on shiftd and tasks."""
    c.run("uv run ruff format shiftd tasks", pty=True)
