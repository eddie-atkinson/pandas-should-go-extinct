from pathlib import Path
from pandas_should_go_extinct.Benchmark import Benchmark


DUCKDB_PATH = Path("./duckdb_1brc.py")
DUCKDB_OUTPUT_PATH = Path("./data/duckdb_timeseries.csv")

POLARS_PATH = Path("./polars_1brc.py")
POLARS_OUTPUT_PATH = Path("./data/polars_timeseries.csv")

PANDAS_PATH = Path("./pandas_1brc.py")
PANDAS_OUTPUT_PATH = Path("./data/pandas_timeseries.csv")


PROFILE_FIXTURES = [
    (POLARS_PATH, POLARS_OUTPUT_PATH),
    (DUCKDB_PATH, DUCKDB_OUTPUT_PATH),
    (PANDAS_PATH, PANDAS_OUTPUT_PATH),
]


def main():
    for test_script, output_path in PROFILE_FIXTURES:
        print(f"Running benchmark script {test_script} with output in {output_path}")
        benchmark = Benchmark(script_path=test_script, output_file_path=output_path)
        benchmark.run()


if __name__ == "__main__":
    main()
