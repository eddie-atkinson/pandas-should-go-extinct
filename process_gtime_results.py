import polars as pl
from pathlib import Path


DUCKDB_OUTPUT_PATH = Path("./data/duckdb.csv")
POLARS_OUTPUT_PATH = Path("./data/polars.csv")
PANDAS_OUTPUT_PATH = Path("./data/pandas.csv")

SECONDS_IN_MINUTE = 60


def parse_duration_string(value: str) -> float:
    whole_part, fractional_seconds = value.split(".")
    seconds = float(fractional_seconds) / 100

    parts = whole_part.split(":")

    multiplier = 1

    while parts:
        part = parts.pop()
        seconds += float(part) * multiplier
        multiplier *= SECONDS_IN_MINUTE

    return seconds * 1000


def print_stats(path: Path, name: str):
    df = pl.read_csv(path)
    df = df.with_columns(
        pl.col("real")
        .map_elements(parse_duration_string, return_dtype=pl.Float32)
        .cast(pl.Duration(time_unit="ms"))
        .alias("real_duration"),
        pl.col("cpu%").str.strip_suffix("%").cast(pl.Float32).alias("cpu"),
    )

    print(name)
    print("-----")

    print(
        df.select(
            pl.col("real_duration").median().alias("median_duration"),
            pl.col("cpu").median().alias("median_max_cpu"),
            (pl.col("maxrss").median() / 1000).alias("median_rss_mb"),
        )
    )
    print("---")


print_stats(DUCKDB_OUTPUT_PATH, "DuckDB")
print_stats(PANDAS_OUTPUT_PATH, "Pandas")
print_stats(POLARS_OUTPUT_PATH, "Polars")
