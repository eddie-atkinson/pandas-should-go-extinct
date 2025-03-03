from constants import DATA_PATH
from pandas_should_go_extinct.duckdb_1brc import do_1brc_duckdb
from pandas_should_go_extinct.pandas_1brc import do_1brc_pandas
from pandas_should_go_extinct.polars_1brc import do_1brc_polars

# N_RUNS = 5
# Why only one core per test? Simply because Polars and DuckDB are multi-threaded,
# so we want to give their threads room to gallop without having other tests interfering
# N_PROCESSES = 1

# runner = pyperf.Runner(processes=N_PROCESSES, values=N_RUNS)


def main():
    do_1brc_duckdb(DATA_PATH)
    # results = runner.bench_func("DuckDB", do_1brc_duckdb, DATA_PATH)
    # if results is not None:
    #     results.dump("./data/duckdb.json", replace=True)

    # results = runner.bench_func("Polars", do_1brc_polars, DATA_PATH)
    # if results is not None:
    #     results.dump("./data/polars.json", replace=True)

    # results = runner.bench_func("Pandas", do_1brc_pandas, DATA_PATH)
    # if results is not None:
    #     results.dump("./data/pandas.json", replace=True)


if __name__ == "__main__":
    main()
