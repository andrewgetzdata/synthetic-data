---
name: data-design
description: Interactively design a synthetic data schema for a new example. Use when planning what fake data to generate — asks follow-up questions about domains, relationships, volumes, and time ranges before producing a data spec and README.
version: 1.1.0
user-invocable: true
---

Interactively design a synthetic data schema. Walk through the following steps with the user, asking questions at each stage before moving on.

## Procedure

### 1. Understand the domain

Ask the user:
- What kind of business or scenario? (e.g., restaurant, e-commerce, SaaS, clinic)
- What's the business name? (this becomes the folder name)
- What scale? (small = ~100 records, medium = ~1K, large = ~10K+ per table)
- What time period should the data span? (e.g., 2024-01-01 to 2025-12-31)

### 2. Propose data domains

Based on the business type, propose relevant data domains. For example, a restaurant might have: staff, menu, inventory, sales, guests, reviews, marketing, financials, vendors.

Present the proposed domains as a list. Ask the user to confirm, add, or remove domains.

### 3. Define schemas per domain

For each confirmed domain, propose a table schema:

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| ... | ... | ... | ... |

Present one domain at a time. Ask for feedback before moving to the next.

### 4. Map relationships

Document foreign key relationships between tables. Present as a text-based dependency list:

```
vendors (no deps)
staff (no deps)
menu_items (no deps)
recipes -> menu_items
inventory -> vendors
guests (no deps)
reservations -> guests
orders -> staff, guests
order_items -> orders, menu_items
reviews -> guests
campaigns (no deps)
campaign_events -> campaigns, guests
daily_financials (derived from orders, staff, campaigns)
```

Confirm with the user.

### 5. Set volume and time range

Propose sensible defaults based on the business scale. Ask the user to confirm or adjust:
- Record counts per table
- Date range for time-series data
- Any seasonal patterns or trends to model (e.g., holiday spikes, summer slowdowns)

### 6. Distribution and realism rules

Propose realistic distributions for key fields. Examples:
- Ratings: skewed positive (mean ~4.0 on 1-5 scale)
- Sales: higher on weekends, lunch/dinner peaks, seasonal variation
- Food cost ratio: ~28-35% of menu price
- No orders outside business hours
- NULLs at realistic rates for optional fields (e.g., 30% of guests have no email)

Ask the user to confirm or adjust.

### 7. Write the data spec

Write a complete spec to `{example-folder}/DATA_SPEC.md` containing:
- Business description
- All table schemas with column names, types, and constraints
- Relationship diagram (text)
- Volume targets per table
- Time range
- Distribution and realism rules
- Generation order (respecting dependencies)

### 8. Write the README

Write `{example-folder}/README.md` with:

1. **Title and description** — what this example is

2. **Data model** — a table for every table in the schema:

   #### `table_name`
   | Column | Type | Description |
   |--------|------|-------------|
   | column_name | VARCHAR | Primary key |
   | ... | ... | ... |

3. **Relationships and join patterns** — an ASCII diagram showing how tables connect, plus example SQL joins:

   ```
   vendors ─────────────── inventory
                               │
   staff ──── orders ──── order_items ──── menu_items
                 │                              │
              guests ──── reservations      recipes
                 │
              reviews
                 │
           campaigns ──── campaign_events
   ```

   **Common joins:**
   ```sql
   -- Order details with item names
   SELECT o.*, oi.*, m.name
   FROM orders o
   JOIN order_items oi ON o.order_id = oi.order_id
   JOIN menu_items m ON oi.item_id = m.item_id;
   ```

4. **How to generate** — the command to run

### 9. Next steps

Tell the user:
1. Create `{example-folder}/generate.py` with Pydantic models and Faker generation logic
2. Run the script to produce parquet files
3. Use `/upload-to-motherduck {example-folder}` to load into MotherDuck

## Best Practices (embedded knowledge)

- Always include surrogate IDs (UUIDs or sequential strings like `VND-001`)
- Use realistic value distributions, not uniform random
- Time-series data needs consistent timestamps (no orders at 3am for a restaurant)
- Financial data should be internally consistent (revenue = sum of sales, COGS derived from actual ingredient costs)
- Include NULL values at realistic rates for optional fields
- Seed Faker for reproducibility
- Output as zstd-compressed parquet via Polars
