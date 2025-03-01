import pandas as pd
import polars as pl
from pathlib import Path

SALES_PATH = Path("./data") / "sales.csv"
OUTPUT_DATA_PATH = Path("./data") / "output"


def read_and_split_data_pandas():
    df = pd.read_csv(SALES_PATH, parse_dates=["SalesDate"])

    groups = df.groupby(df["SalesDate"].dt.date)
    for date, group in groups:
        out_path = OUTPUT_DATA_PATH / f"{date}.csv"
        group.to_csv(out_path)


def read_and_split_data_polars():
    df = pl.read_csv(SALES_PATH, try_parse_dates=True)

    groups = df.group_by(pl.col("SalesDate").dt.date())
    for date, group in groups:
        out_path = OUTPUT_DATA_PATH / f"{date[0]}.csv"
        group.write_csv(out_path)


def main():
    OUTPUT_DATA_PATH.mkdir(exist_ok=True, parents=True)
    # read_and_split_data_pandas()
    read_and_split_data_polars()


if __name__ == "__main__":
    main()
