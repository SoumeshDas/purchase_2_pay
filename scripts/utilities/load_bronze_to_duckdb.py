import duckdb

PROJECT_ROOT = "/jobs"

PARQUET_PATH = f"{PROJECT_ROOT}/output/sales_stream/*.parquet"

DB_PATH = f"{PROJECT_ROOT}/output/quality.duckdb"

print("=" * 60)
print("Loading Bronze into DuckDB")
print("=" * 60)

con = duckdb.connect(DB_PATH)

con.execute(
    """
DROP TABLE IF EXISTS sales
"""
)

con.execute(
    f"""
CREATE TABLE sales AS
SELECT *
FROM read_parquet('{PARQUET_PATH}')
"""
)

rows = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]

print(f"Rows Loaded : {rows}")

con.close()

print("DuckDB database created successfully.")
