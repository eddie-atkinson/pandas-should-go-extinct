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
= No one has or queries or Big Data\*
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
        .collect(new_streaming=True)
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
  columns: (auto, auto, auto, auto),
  align: center,
  inset: 15pt,
  table.header(
    [*Library*],[*Median Wall Clock Duration*], [*Median Max CPU %*],[*Median Max RSS*],
  ),
  $ "Pandas" $,
  $"3m 57s" $,
  $"101.0%"$,
  $"33.34 GB"$,
)][#table(
  columns: (auto, auto, auto, auto),
  align: center,
  inset: 15pt,
  table.header(
    [*Library*],[*Median Wall Clock Duration*], [*Median Max CPU %*],[*Median Max RSS*],
  ),
  $ "Pandas" $,
  $"3m 57s" $,
  $"101.0%"$,
  $"33.34 GB"$,
  $ "Polars" $,
  $"3.92s" $,
  $"2588.5%"$,
  $"17.98 GB"$,
)][#table(
  columns: (auto, auto, auto, auto),
  align: center,
  inset: 15pt,
  table.header(
    [*Library*],[*Median Wall Clock Duration*], [*Median Max CPU %*],[*Median Max RSS*],
  ),
  $ "Pandas" $,
  $"3m 57s" $,
  $"101.0%"$,
  $"33.34 GB"$,
  $ "Polars" $,
  $"3.92s" $,
  $"2588.5%"$,
  $"17.98 GB"$,
  $ "DuckDB" $,
  $"4.19s" $,
  $"2979.0%"$,
  $"1.93 GB"$,
)]

== Results (M1 MBA, 16GB RAM)
#table(
  columns: (auto, auto, auto, auto),
  align: center,
  inset: 15pt,
  table.header(
    [*Library*],[*Median Wall Clock Duration*], [*Median Max CPU %*],[*Median Max RSS*],
  ),
  $ "Pandas" $,
  $"3m 57s" $,
  $"101.0%"$,
  $"33.34 GB"$,
  $ "Polars" $,
  $"3.92s" $,
  $"2588.5%"$,
  $"17.98 GB"$,
  $ "DuckDB" $,
  $"4.19s" $,
  $"2979.0%"$,
  $"1.93 GB"$,
)

== What do these tools give us?
- Great performance on a flawed benchmark
#pause
- Painless multi-threading
- Streaming
- Spill to disk
- Lazy evaluation
== Simple Animation

= I'm interested but I've been hurt before

== Painless Adoption with Arrow
- In-memory column oriented data format
#pause
- Supported in Pandas since 2.0 (April 2023)
  - Some functions still create NumPy arrays
#pause
- *Polars and DuckDB support zero copy serialisation from Arrow-backed Pandas DataFrames*

== Practical Example


#show: appendix
#bibliography("works.bib")

