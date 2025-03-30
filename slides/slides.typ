#import "@preview/touying:0.6.1": *
#import themes.metropolis: *

#import "@preview/numbly:0.1.0": numbly



#show: metropolis-theme.with(
  aspect-ratio: "16-9",
  config-info(
    title: [Pandas Should Go Extinct],
    author: [Eddie Atkinson (he/him)],
    date: datetime(year: 2025, month: 4, day: 4),
    institution: [Senior Software Engineer - Atlassian],
  ),
  config-colors(
  primary: rgb("#000000"),
  primary-light: rgb("#d6c6b7"),
  secondary: rgb("#23373b"),
  neutral-lightest: rgb("#fafafa"),
  neutral-dark: rgb("#23373b"),
  neutral-darkest: rgb("#23373b"),
)
)

#title-slide()



== Who's Who in the Zoo?
#figure(
  image("figures/tools_comparison.png"),
  caption: [Rough Guide to Data Tool Adoption Curve by Data Size],
)

#figure(
  image("figures/tools_comparison_gap.png"),
  caption: [Pandas Data Size Cliff],
)

= Why do you care so much about \~100GB data sets?
== Who's got Big Data™️?
#figure(
  image("figures/fleet_size_data_comparison.png"),
  caption: [Bucketed Total Row Counts for Amazon RedShift Fleet Over 1 Month @van2024tpc],
)

== Who's got Big Data™️?
#figure(
  image("figures/fleet_size_query_comparison.png"),
  caption: [Bucketed Query Runtime for Amazon RedShift Fleet Over 1 Month @van2024tpc],
)
= No one stores or queries Big Data\*
#pause
\*almost no one
= Shut up and show me the code

== Example: 1 Billion Row Challenge
Contest to create the fastest JVM implementation which could compute the min, mean, max for 1 billion rows of weather station data
#pause
```csv
Perth;12.0
Sydney;2.0
```
to
```js
{Perth=12.0/12.0/12.0...}
```
== Example: 1 Billion Row Challenge
Fastest JVM implementation: *1.535 seconds*

#pause
Our Experimental Setup:
- ~16GB CSV
- AWS M7a.8xlarge
  - 32 core AMD CPU
  - 128 GB of RAM
- 30 x repetitions (2 x warmups)
#pause
*We won't benchmark output serialisation*

== Pandas
```py
def do_1brc_pandas(file_path: str):
    df = (
        pd.read_csv(file_path, sep=";", names=["station", "measurement"])
        .groupby("station")
        .agg({"measurement": ["min", "mean", "max"]})
        .round(2)
    )
```
== Polars
```py
def do_1brc_polars(file_path: str):
    df = (
        pl.scan_csv(
            file_path,
            separator=";",
            new_columns=["station", "measurement"],
            has_header=False,
        )
        .group_by("station")
        .agg(
            pl.col("measurement").min().round(2).alias("min"),
            pl.col("measurement").mean().round(2).alias("mean"),
            pl.col("measurement").max().round(2).alias("max"),
        )
        .sort(by="station")
        .collect(new_streaming=True) # Trigger evaluation in streaming mode
    )

```
== DuckDB
```py
def do_1brc_duckdb(file_path: str):
    df = duckdb.read_csv(file_path, names=["station", "measurements"])

    src = duckdb.sql("""
          create table src as 
          select 
            station, 
            min(measurements) min, 
            max(measurements) max, 
            cast(avg(measurements) as decimal(8, 1)) avg 
          from df 
          group by station
        """
    )
```
== Results (M7a.8xlarge)
#alternatives[#table(
  columns: (auto, auto, auto, auto, auto),
  align: center,
  inset: 15pt,
  table.header(
    [*Library*],[*Median Duration*], [*Median Max CPU %*],[*Median Max USS*],[*Median Max Swap*],
  ),
  $ "Pandas" $,
  $"4m 28s" $,
  $"113.0%"$,
  $"38.12 GB"$,
  $"0 MB"$,
)][#table(
  columns: (auto, auto, auto, auto, auto),
  align: center,
  inset: 15pt,
  table.header(
    [*Library*],[*Median Duration*], [*Median Max CPU %*],[*Median Max USS*],[*Median Max Swap*],
  ),
  $ "Pandas" $,
  $"4m 28s" $,
  $"113.0%"$,
  $"38.12 GB"$,
  $"0 MB"$,
  $ "Polars" $,
  $"5.04s" $,
  $"3202.60%"$,
  $"18.02 GB"$,
  $"0 MB"$,
)][#table(
  columns: (auto, auto, auto, auto, auto),
  align: center,
  inset: 15pt,
  table.header(
    [*Library*],[*Median Duration*], [*Median Max CPU %*],[*Median Max USS*],[*Median Max Swap*],
  ),
  $ "Pandas" $,
  $"4m 28s" $,
  $"113.0%"$,
  $"38.12 GB"$,
  $"0 MB"$,
  $ "Polars" $,
  $"5.04s" $,
  $"3202.60%"$,
  $"18.02 GB"$,
  $"0 MB"$,
  $ "DuckDB" $,
  $"5.19s" $,
  $"3174.64%"$,
  $"1.93 GB"$,
  $"0 MB"$,
)]

== Results (11th Gen 8 Core i5, 16GiB RAM)
#table(
  columns: (auto, auto, auto, auto, auto),
  align: center,
  inset: 15pt,
  table.header(
    [*Library*],[*Median Duration*], [*Median Max CPU %*],[*Median Max USS*],[*Median Max Swap*],
  ),
  $ "Pandas" $,
  $"12m 15s" $,
  $"110.35%"$,
  $"15.67 GB"$,
  $"21.02 GB"$,
  $ "Polars" $,
  $"39s" $,
  $"765.75%"$,
  $"15.22 GB"$,
  $"35.85 MB"$,
  $ "DuckDB" $,
  $"47s" $,
  $"807.0%"$,
  $"546.87 MB"$,
  $"0 MB"$,
)

== What do these tools give us?
- Great performance on a *flawed benchmark*
#pause
- Painless multi-threading
- Streaming
- Spill to disk
- Lazy evaluation

= I'm interested but I've been hurt before

== Painless Adoption with Arrow
- In-memory column oriented data format
#pause
- Supported in Pandas since 2.0 (April 2023)
  #pause
  - Support is *getting there*
#pause
- *Polars and DuckDB support zero copy serialisation to and from Arrow-backed Pandas DataFrames*
  - Otherwise you get a fresh copy

== Practical Example: New York Taxi Data
- Dataset of every taxi trip taken in New York
- 1 Parquet file per month from 2009-
#pause
- Corporate wants us to find out if the Pandemic made cash less common
  - 2019-2022 (~2.71GB of Parquet)
#pause
- We're using DuckDB with Pandas, also works with Polars and Pandas

== Pure Pandas (helpers)
```py
def read_and_merge_dfs(folder: Path) -> pd.DataFrame:
    df = None
    for entry in folder.iterdir():
        if not entry.name.endswith("parquet"): continue
        temp = pd.read_parquet(entry, columns=COLUMNS, dtype_backend="pyarrow")
        if df is not None:
            df = pd.concat([df, temp])
        else:
            df = temp
    df = df[df["tpep_pickup_datetime"] > pd.to_datetime(MIN_DATETIME)]
    df = df[df["tpep_pickup_datetime"] < pd.to_datetime(MAX_DATETIME)]

    df["month"] = df["tpep_pickup_datetime"].dt.month
    df["year"] = df["tpep_pickup_datetime"].dt.year
    df = df.drop(["tpep_pickup_datetime"], axis="columns")
    return df
```

== Pure Pandas
```py
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
```

== Duck Reads Panda Thinks
```py
def do_taxi_duck_read(folder: str):
    df = duckdb.sql(f"""
        select datepart('year', tpep_pickup_datetime) year, 
          datepart('month', tpep_pickup_datetime) month, 
          payment_type from '{folder}/*.parquet'
        where tpep_pickup_datetime > '{MIN_DATE}'
         and tpep_pickup_datetime < '{MAX_DATE}'"""
      ).df()

    df = (
        df.groupby(["year", "month", "payment_type"])
        .agg({"payment_type": "count"})
        .unstack(fill_value=0, level=2)["payment_type"]
        .reset_index()
    )
    df["total_payments"] = df.iloc[:, 2:8].sum(axis=1)
    df["cash_pct"] = (df[CASH] / df["total_payments"]) * 100
```
== Panda Reads Duck Thinks
```py
def do_taxi_duck_compute(folder: Path):
    df = read_and_merge_dfs(folder)
    result = duckdb.sql(f"""
        with total as (
            select year, month, count(payment_type) payments from df 
            group by year, month
        ),
        total_cash as (
            select year, month, count(payment_type) cash from df 
            where payment_type={CASH} 
            group by year, month
        )
        select total.*, cash, (cash / total) * 100 cash_pct from total 
        join total_cash 
          on total.year=total_cash.year and total.month=total_cash.month
        order by total.year, total.month
    """).df()
```
== Pure DuckDB
```py
def do_taxi_duck(folder: Path):
    data = duckdb.sql(f"""
        select datepart('year', tpep_pickup_datetime) year, 
          datepart('month', tpep_pickup_datetime) month, 
          payment_type from '{folder}/*.parquet'
        where tpep_pickup_datetime > '{MIN_DATE}'
         and tpep_pickup_datetime < '{MAX_DATE}'"""
      )
    # continued
```
== Duck Does All
```py
def do_taxi_duck(folder: Path):
  # Data loading on previous slide
  result = duckdb.sql(f"""
    with total as (
        select year, month, count(payment_type) payments from data 
        group by year, month
    ),
    total_cash as (
        select year, month, count(payment_type) cash from data 
        where payment_type={CASH} 
        group by year, month
    )
    select total.*, cash, (cash / total) * 100 cash_pct from total 
    join total_cash 
      on total.year=total_cash.year and total.month=total_cash.month
    order by total.year, total.month
    """).df()
```
== Results (11th Gen 8 Core i5, 16GiB RAM)
#table(
  columns: (auto, auto, auto, auto, auto),
  align: center,
  inset: 15pt,
  table.header(
    [*Approach*],[*Median Duration*], [*Median Max CPU %*],[*Median Max USS*],[*Median Max Swap*],
  ),
  $ "Pure Pandas" $,
  $"41.88s" $,
  $"146.10%"$,
  $"14.52 GB"$,
  $"1.92 GB"$,
  $ "Duck Reads\n Panda Thinks" $,
  $"28.39s" $,
  $"793.7%"$,
  $"14.79 GB"$,
  $"1.22 GB"$,
  $ "Panda Reads\n Duck Thinks" $,
  $"29.25s" $,
  $"765.4%"$,
  $"12.39 GB"$,
  $"0 MB"$,
  $ "Pure DuckDB" $,
  $"21.70s" $,
  $"814.95%"$,
  $"216.76 MB"$,
  $"0 MB"$,
)
== So...did cash usage fall over the Pandemic?
#pause
- Yes
#pause
- Correlation !== causality, don't \@ me
#pause
- TODO: add figure
= This sounds compelling, what's the catch?
== Reasons NOT to listen to me
#pause
1. I'm just a guy with a laptop - do your own research
#pause
2. You're super deeply integrated into the Pandas ecosystem
  #pause
  - e.g. Geospatial
#pause
3. Let Pandas cook
  #pause
  - Progress on integrating PyArrow nicely has been...slow
  #pause
  - There are benefits beyond performance
    #pause
    - Ergonomics / API grokkability
    #pause
    - Transferable (and cheaper) skill set

= You've suggested two tools, which is better?
== Tool comparisons
Foo

#show: appendix
#bibliography("works.bib")

