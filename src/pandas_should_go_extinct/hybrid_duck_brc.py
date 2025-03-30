import duckdb
import pandas as pd


def do_1brc_hybrid_duck():
    df = pd.read_parquet("https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet")

    breakpoint()
    output_df = duckdb.sql(
        "select station, min(measurement) min, cast(avg(measurement) as decimal(8, 1)) avg, max(measurement) max from df group by station order by station"
    ).df()


