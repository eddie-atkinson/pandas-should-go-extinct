import duckdb
from pathlib import Path


DUCKDB_OUTPUT_PATH_M7A = Path("./data/duckdb_timeseries_m7a.csv")
POLARS_OUTPUT_PATH_M7A = Path("./data/polars_timeseries_m7a.csv")
PANDAS_OUTPUT_PATH_M7A = Path("./data/pandas_timeseries_m7a.csv")

DUCKDB_OUTPUT_PATH_LAPTOP = Path("./data/duckdb_timeseries_laptop.csv")
POLARS_OUTPUT_PATH_LAPTOP = Path("./data/polars_timeseries_laptop.csv")
PANDAS_OUTPUT_PATH_LAPTOP = Path("./data/pandas_timeseries_laptop.csv")


PANDAS_ONLY_OUTPUT_PATH = Path("./data/taxi/pandas.csv")
DUCK_READ_OUTPUT_PATH = Path("./data/taxi/duck_read.csv")
DUCK_COMPUTE_OUTPUT_PATH = Path("./data/taxi/duck_compute.csv")
DUCK_ONLY_OUTPUT_PATH = Path("./data/taxi/duck_only.csv")


def print_stats(path: Path, name: str):
    str_path = str(path.absolute())
    # Have to slightly fudge the time here to account for the Python interpreter starting
    by_run_no = duckdb.sql(
        f"select max(uss) / 1_000_000 as uss_mb, max(cpu_pct) as cpu_pct, max(time_s) as time_s, max(swap) / 1_000_000 as swap_mb from '{str_path}' where time_s > 1 group by run_no;"
    )
    print(name)
    print("-----")
    duckdb.sql(
        "select median(time_s) time_s, median(cpu_pct) cpu_pct, median(uss_mb) uss_mb, median(swap_mb) swap_mb from by_run_no"
    ).show()
    print("---")


print_stats(PANDAS_OUTPUT_PATH_M7A, "Pandas M7A")
print_stats(POLARS_OUTPUT_PATH_M7A, "Polars M7A")
print_stats(DUCKDB_OUTPUT_PATH_M7A, "DuckDB M7A")

print_stats(PANDAS_OUTPUT_PATH_LAPTOP, "Pandas Laptop")
print_stats(POLARS_OUTPUT_PATH_LAPTOP, "Polars Laptop")
print_stats(DUCKDB_OUTPUT_PATH_LAPTOP, "DuckDB Laptop")

# print_stats(PANDAS_ONLY_OUTPUT_PATH, "Pandas Taxi")
# print_stats(DUCK_READ_OUTPUT_PATH, "DuckDB Read Taxi")
# print_stats(DUCK_COMPUTE_OUTPUT_PATH, "DuckDB Compute Taxi")
# print_stats(DUCK_ONLY_OUTPUT_PATH, "DuckDB Taxi")
