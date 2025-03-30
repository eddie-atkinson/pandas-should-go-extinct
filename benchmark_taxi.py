from pathlib import Path
from pandas_should_go_extinct.Benchmark import Benchmark


DUCKDB_PATH = Path("./duckdb_1brc.py")
DUCKDB_OUTPUT_PATH = Path("./data/duckdb_timeseries.csv")

POLARS_PATH = Path("./polars_1brc.py")
POLARS_OUTPUT_PATH = Path("./data/polars_timeseries.csv")

PANDAS_PATH = Path("./pandas_1brc.py")
PANDAS_OUTPUT_PATH = Path("./data/pandas_timeseries.csv")

SCRIPT_PATH = Path("./pandas_duck_hybrid.py")
PANDAS_ONLY_OUTPUT_PATH = Path("./data/taxi/pandas.csv")
DUCK_READ_OUTPUT_PATH = Path("./data/taxi/duck_read.csv")
DUCK_COMPUTE_OUTPUT_PATH = Path("./data/taxi/duck_compute.csv")
DUCK_ONLY_OUTPUT_PATH = Path("./data/taxi/duck_only.csv")

PROFILE_FIXTURES = [
    (SCRIPT_PATH, "pandas", PANDAS_ONLY_OUTPUT_PATH),
    (SCRIPT_PATH, "duck_read", DUCK_READ_OUTPUT_PATH),
    (SCRIPT_PATH, "duck_compute", DUCK_COMPUTE_OUTPUT_PATH),
    (SCRIPT_PATH, "duck", DUCK_ONLY_OUTPUT_PATH),
]


def main():
    for test_script, variant, output_path in PROFILE_FIXTURES:
        print(f"Running benchmark script {test_script} with output in {output_path}")
        benchmark = Benchmark(
            script_path=test_script, output_file_path=output_path, args=[variant]
        )
        benchmark.run()


if __name__ == "__main__":
    main()
