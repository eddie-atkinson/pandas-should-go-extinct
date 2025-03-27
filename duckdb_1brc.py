from pandas_should_go_extinct.constants import DATA_PATH
from pandas_should_go_extinct.duckdb_1brc import do_1brc_duckdb


def main():
    do_1brc_duckdb(DATA_PATH, output_data=False)


if __name__ == "__main__":
    main()
