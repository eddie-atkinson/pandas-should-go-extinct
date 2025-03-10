#!/bin/bash
# TODO: up to 50 or 100 for real testing
N_ITER=10
N_WARMUP=0

./profile.sh ./.venv/bin/python duckdb_1brc.py $N_ITER $N_WARMUP ./data/duckdb.csv
./profile.sh ./.venv/bin/python polars_1brc.py $N_ITER $N_WARMUP ./data/polars.csv
# ./profile.sh ./.venv/bin/python pandas_1brc.py $N_ITER $N_WARMUP ./data/pandas.csv
