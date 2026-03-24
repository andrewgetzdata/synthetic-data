# synthetic-data

Generate synthetic/fake data for example projects using Python.

## Structure

- Each example is a top-level folder (e.g., `frying-nemo/`)
- Each folder has a `generate.py` at its root and outputs parquet files alongside it
- Each example is self-contained — Pydantic models live in the generate script

## Tech Stack

- Python 3.10+, Faker, Polars, Pydantic
- Output: zstd-compressed parquet (`polars.DataFrame.write_parquet(path, compression="zstd")`)
- Packaging: hatchling + uv

## Conventions

- Pydantic models define schemas for each data domain
- Generation scripts are standalone: `python frying-nemo/generate.py`
- Parquet files are gitignored — they're generated artifacts
- MotherDuck database: `synthetic_data`, schema per example: `{folder_name}` (hyphens to underscores)

## Commands

- Install: `uv venv && uv pip install -e ".[dev]"`
- Lint: `ruff check .`
- Format: `ruff format .`
- Type check: `mypy .`
- Test: `pytest`
