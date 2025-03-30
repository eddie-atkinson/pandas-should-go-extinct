from pathlib import Path
import pandas as pd
import duckdb

COLUMNS = ["tpep_pickup_datetime", "payment_type"]
MIN_DATETIME = "2019-01-01"
MAX_DATETIME = "2023-01-01"
CASH = 2


def read_and_merge_dfs(folder: Path) -> pd.DataFrame:
    df = None
    for entry in folder.iterdir():
        if not entry.name.endswith("parquet"):
            continue
        temp_df = pd.read_parquet(entry, columns=COLUMNS, dtype_backend="pyarrow")
        if df is not None:
            df = pd.concat([df, temp_df])
        else:
            df = temp_df
    df = df[df["tpep_pickup_datetime"] > pd.to_datetime(MIN_DATETIME)]
    df = df[df["tpep_pickup_datetime"] < pd.to_datetime(MAX_DATETIME)]

    df["month"] = df["tpep_pickup_datetime"].dt.month
    df["year"] = df["tpep_pickup_datetime"].dt.year
    df = df.drop(["tpep_pickup_datetime"], axis="columns")

    return df


def do_taxi_pandas(folder: Path):
    df = read_and_merge_dfs(folder)
    df = (
        df.groupby(["year", "month", "payment_type"])
        .agg({"payment_type": "count"})
        .unstack(fill_value=0, level=2)["payment_type"]
        .reset_index()
    )

    df["total_payments"] = df.iloc[:, 2:8].sum(axis=1)
    df["cash_pct"] = (df[CASH] / df["total_payments"]) * 100


def do_taxi_duck_read(folder: Path):
    df = duckdb.sql(f"""
        select datepart('year', tpep_pickup_datetime) as year, datepart('month', tpep_pickup_datetime) as month, payment_type from '{str(folder.absolute())}/*.parquet'
        where tpep_pickup_datetime > '{MIN_DATETIME}' and tpep_pickup_datetime < '{MAX_DATETIME}';
    """).df()

    df = (
        df.groupby(["year", "month", "payment_type"])
        .agg({"payment_type": "count"})
        .unstack(fill_value=0, level=2)["payment_type"]
        .reset_index()
    )
    df["total_payments"] = df.iloc[:, 2:8].sum(axis=1)
    df["cash_pct"] = (df[CASH] / df["total_payments"]) * 100


def do_taxi_duck_compute(folder: Path):
    df = read_and_merge_dfs(folder)
    result = duckdb.sql(f"""
        with total as (
            select year, month,  count(payment_type) total_payments from df group by year, month
        ),
        total_cash as (
            select year, month, count(payment_type) cash_payments from df where payment_type={CASH} group by year, month
        )
        select total.*, cash_payments, (cash_payments / total_payments) * 100 cash_pct from total join total_cash on total.year=total_cash.year and total.month=total_cash.month order by total.year, total.month
    """).df()


def do_taxi_duck(folder: Path):
    result = duckdb.sql(f"""
        with data as (
            select datepart('year', tpep_pickup_datetime) as year, datepart('month', tpep_pickup_datetime) as month, payment_type from '{str(folder.absolute())}/*.parquet'
            where tpep_pickup_datetime > '{MIN_DATETIME}' and tpep_pickup_datetime < '{MAX_DATETIME}'
        ),
        total as (
            select year, month,  count(payment_type) total_payments from data group by year, month
        ),
        total_cash as (
            select year, month, count(payment_type) cash_payments from data where payment_type={CASH} group by year, month
        )
        select total.*, cash_payments, (cash_payments / total_payments) * 100 cash_pct from total join total_cash on total.year=total_cash.year and total.month=total_cash.month order by total.year, total.month
    """).df()
