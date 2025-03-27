from pandas_should_go_extinct.constants import DATA_PATH
from pandas_should_go_extinct.pandas_1brc import do_1brc_pandas


def main():
    do_1brc_pandas(DATA_PATH, output_data=False)


if __name__ == "__main__":
    main()
