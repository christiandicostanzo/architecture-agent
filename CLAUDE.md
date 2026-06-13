# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

This is a Python project for an architecture agent. No source code exists yet; this file will be updated as the codebase grows.

## Environment Setup

```bash
uv sync        # install all dependencies into .venv
```

## Common Commands

| Task | Command |
|------|---------|
| Add dependency | `uv add <package>` |
| Run app | `uv run python -m architecture_agent` |
| Run tests | `uv run pytest` |
| Run single test | `uv run pytest tests/path/to/test_file.py::test_name` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy .` |
