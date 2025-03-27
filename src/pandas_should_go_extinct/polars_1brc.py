import polars as pl


def do_1brc_polars(file_path: str, output_data=True) -> str:
    """
    Perform the 1BRC using Polars, this function will likely OOM if you do not have a reasonable quantity of RAM (> 16GB)

    Note: the output serialisation isn't a main focus of this test for performance purposes,
    so there is an option not to serialise the output. However, having the output is useful for testing correctness
    """
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
    )  # type: ignore

    if output_data:
        result = []
        for station, min_val, mean_val, max_val in df.iter_rows():
            result.append(f"{station}={min_val}/{mean_val}/{max_val}")

        return "{" + ", ".join(result) + "}"
    return ""
