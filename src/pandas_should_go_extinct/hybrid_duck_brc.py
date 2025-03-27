import duckdb
import pandas as pd


def do_1brc_hybrid_duck(file_path: str, output_data=True) -> str:
    df = pd.read_csv(
        file_path, sep=";", names=["station", "measurement"], nrows=500_000
    )

    output_df = duckdb.sql("select station, min(measurement) min, cast(avg(measurement) as decimal(8, 1)) avg, max(measurement) max from df group by station order by station").df()


    if output_data:
        result = []
        for _,station, min_val, mean_val, max_val in output_df.to_records():
            result.append(f"{station}={min_val}/{mean_val}/{max_val}")
        return "{" + ", ".join(result) + "}"
    return ""
