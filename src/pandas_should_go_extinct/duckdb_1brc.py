import duckdb


def do_1brc_duckdb(file_path: str, output_data=True) -> str:
    """
    Run the 1BRC using Duck DB. Note: the output serialisation isn't a main focus of this test for performance purposes,
    so there is an option not to serialise the output. However, having the output is useful for testing correctness
    """
    df = duckdb.read_csv(file_path, names=["station", "measurements"])

    src = duckdb.sql(
        "create or replace table src as select station, min(measurements) min, max(measurements) max, cast(avg(measurements) as decimal(8, 1)) avg from df group by station"
    )

    if output_data:
        return duckdb.sql(
            """
            select '{' || array_to_string(list(station || '=' || concat_ws('/', min, avg, max) order by station), ', ') || '}'
            from src;
            """
        ).fetchall()[0][0]
    return ""
