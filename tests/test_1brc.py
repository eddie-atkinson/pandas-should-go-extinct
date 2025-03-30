from pathlib import Path
from unittest import TestCase, main


from pandas_should_go_extinct.duckdb_1brc import do_1brc_duckdb
from pandas_should_go_extinct.pandas_1brc import do_1brc_pandas
from pandas_should_go_extinct.polars_1brc import do_1brc_polars

SIMPLE_PATH = Path("./tests/fixtures/simple.csv")
SIMPLE_WITH_AGG_PATH = Path("./tests/fixtures/simple_with_agg.csv")


EXPECTED_SIMPLE = "{Irún=6.8/6.8/6.8, Kalush=70.4/70.4/70.4, Kumanovo=-79.9/-79.9/-79.9, Villa Elisa=-85.4/-85.4/-85.4}"
EXPECTED_SIMPLE_WITH_AGG = "{Irún=-8.0/4.6/15.0, Kalush=70.4/70.4/70.4, Kumanovo=-79.9/0.0/79.9, Villa Elisa=-85.4/-10.6/54.0}"


class TestOneBillionRowChallenge(TestCase):
    def test_duckdb_simple(self):
        result = do_1brc_duckdb(str(SIMPLE_PATH.absolute()))
        self.assertEqual(EXPECTED_SIMPLE, result)

    def test_duckdb_simple_agg(self):
        result = do_1brc_duckdb(str(SIMPLE_WITH_AGG_PATH.absolute()))
        self.assertEqual(EXPECTED_SIMPLE_WITH_AGG, result)

    def test_polars_simple(self):
        result = do_1brc_polars(str(SIMPLE_PATH.absolute()))
        self.assertEqual(EXPECTED_SIMPLE, result)

    def test_polars_simple_agg(self):
        result = do_1brc_polars(str(SIMPLE_WITH_AGG_PATH.absolute()))
        self.assertEqual(EXPECTED_SIMPLE_WITH_AGG, result)

    def test_pandas_simple(self):
        result = do_1brc_pandas(str(SIMPLE_PATH.absolute()))
        self.assertEqual(EXPECTED_SIMPLE, result)

    def test_pandas_simple_agg(self):
        result = do_1brc_pandas(str(SIMPLE_WITH_AGG_PATH.absolute()))
        self.assertEqual(EXPECTED_SIMPLE_WITH_AGG, result)


if __name__ == "__main__":
    main()
