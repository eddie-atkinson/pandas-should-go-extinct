import duckdb
from pathlib import Path


DUCKDB_OUTPUT_PATH = Path("./data/duckdb_timeseries_m7a.csv")
POLARS_OUTPUT_PATH = Path("./data/polars_timeseries_m7a.csv")
PANDAS_OUTPUT_PATH = Path("./data/pandas_timeseries_m7a.csv")




def print_stats(path: Path, name: str):
    str_path = str(path.absolute())
    # Have to slightly fudge the time here to account for the Python interpreter starting
    by_run_no = duckdb.sql(f"select max(uss) / 1_000_000 as uss_mb, max(cpu_pct) as cpu_pct, max(time_s) as time_s, max(swap) / 1_000_000 as swap_mb from '{str_path}' where time_s > 1 group by run_no;")
    print(name)
    print("-----")
    duckdb.sql("select median(time_s) time_s, median(cpu_pct) cpu_pct, median(uss_mb) uss_mb, median(swap_mb) swap_mb from by_run_no").show()
    print("---")


print_stats(PANDAS_OUTPUT_PATH, "Pandas")
print_stats(POLARS_OUTPUT_PATH, "Polars")
print_stats(DUCKDB_OUTPUT_PATH, "DuckDB")
