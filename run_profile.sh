#!/bin/bash
N_ITER=30
N_WARMUP=2

./profile.sh ./.venv/bin/python duckdb_1brc.py $N_ITER $N_WARMUP ./data/duckdb.csv
./profile.sh ./.venv/bin/python polars_1brc.py $N_ITER $N_WARMUP ./data/polars.csv
./profile.sh ./.venv/bin/python pandas_1brc.py $N_ITER $N_WARMUP ./data/pandas.csv
