# synthetic-data

Quickly generate fake or synthetic data to use in example projects, MVPs, tests, etc.

Uses Python (Faker, Polars, Pydantic) and information from the web to generate realistic synthetic datasets. All output is zstd-compressed Parquet, optimized for DuckDB and MotherDuck.

## Examples

### Frying Nemo — Seafood Restaurant

Full operational data for a fictional seafood restaurant: 13 tables, 2 years (2024-2025), ~370K total rows.

```bash
python frying-nemo/generate.py
```

```mermaid
erDiagram
    vendors ||--o{ inventory : "vendor_id"
    menu_items ||--o{ recipes : "item_id"
    menu_items ||--o{ order_items : "item_id"
    staff ||--o{ orders : "server_id"
    guests ||--o{ orders : "guest_id"
    guests ||--o{ reservations : "guest_id"
    guests ||--o{ reviews : "guest_id"
    guests ||--o{ campaign_events : "guest_id"
    orders ||--o{ order_items : "order_id"
    campaigns ||--o{ campaign_events : "campaign_id"

    vendors { varchar vendor_id PK }
    staff { varchar staff_id PK }
    menu_items { varchar item_id PK }
    recipes { varchar recipe_id PK }
    inventory { varchar ingredient_id PK }
    guests { varchar guest_id PK }
    reservations { varchar reservation_id PK }
    orders { varchar order_id PK }
    order_items { varchar order_item_id PK }
    reviews { varchar review_id PK }
    campaigns { varchar campaign_id PK }
    campaign_events { varchar event_id PK }
    daily_financials { date financial_date PK }
```

See [`frying-nemo/README.md`](frying-nemo/README.md) for the full data model, column details, and example SQL joins.

## Structure

Each example is a top-level folder with its own generator and output:

```
frying-nemo/          # Seafood restaurant — staff, sales, inventory, reviews, etc.
  generate.py         # Run to produce parquet files
  *.parquet           # Generated output (gitignored)
  README.md           # Data model, ER diagram, example joins
```

## Getting Started

```bash
uv venv && uv pip install -e ".[dev]"
python frying-nemo/generate.py
```

## Claude Code Skills

- `/data-design` — Interactively design a synthetic data schema for a new example
- `/upload-to-motherduck [folder]` — Upload parquet files to MotherDuck
- `/ship [commit message]` — Stage, commit, push, and open a PR

## Tech Stack

- **Python 3.10+** with Faker, Polars, Pydantic
- **Parquet** (zstd compression) for all output
- **DuckDB / MotherDuck** as the target analytical database
