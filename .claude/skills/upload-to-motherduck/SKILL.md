---
name: upload-to-motherduck
description: Upload generated parquet files from an example folder to MotherDuck. Creates a dedicated "synthetic_data" database, a schema named {folder_name}, and loads all parquet files as tables.
argument-hint: [folder-name]
version: 1.2.0
user-invocable: true
---

Upload parquet files from an example folder to MotherDuck. All synthetic data lives in a dedicated `synthetic_data` database with one schema per example.

## Procedure

### 1. Resolve the folder

If `$ARGUMENTS` is provided, use it as the folder name. Otherwise, ask the user which example folder to upload.

Verify the folder exists at the repo root.

### 2. Find parquet files

Glob for `{folder}/*.parquet` files. List them with their names.

If none found, tell the user to run the generation script first:
```
python {folder}/generate.py
```

### 3. Derive the schema name

Convert the folder name to a schema name:
- Replace hyphens with underscores

Example: `frying-nemo` → `frying_nemo`

### 4. Upload via local DuckDB

The MotherDuck cloud MCP cannot read local files. Use local DuckDB with the `md:` connection to upload.

All synthetic data goes into the `synthetic_data` database (created if it doesn't exist). Each example folder gets its own schema within that database.

Run via Bash:
```python
.venv/bin/python -c "
import duckdb, glob

con = duckdb.connect('md:synthetic_data')
con.execute('CREATE SCHEMA IF NOT EXISTS {folder_name}')

for f in sorted(glob.glob('{folder}/*.parquet')):
    table = f.split('/')[-1].replace('.parquet', '')
    con.execute(f'CREATE OR REPLACE TABLE {folder_name}.{table} AS SELECT * FROM read_parquet(\'{f}\')')
    count = con.execute(f'SELECT COUNT(*) FROM {folder_name}.{table}').fetchone()[0]
    print(f'{table}: {count:,} rows')

con.close()
"
```

If authentication fails, tell the user to run `! .venv/bin/python -c "import duckdb; duckdb.connect('md:')"` to complete browser SSO, or set `MOTHERDUCK_TOKEN` in `.env`.

### 5. Verify the upload

Use the MotherDuck MCP `query` tool to verify:
```sql
SELECT schema_name, table_name, estimated_size
FROM duckdb_tables()
WHERE database_name = 'synthetic_data'
  AND schema_name = '{folder_name}'
ORDER BY table_name;
```

### 6. Report

Print a summary table:

| Table | Rows |
|-------|------|
| staff | 25 |
| orders | 49,622 |
| ... | ... |

Report: database (`synthetic_data`), schema name, and total number of tables loaded.
