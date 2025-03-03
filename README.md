## 1 Billion Row Challenge Benchmarking
This is a somewhat scientific look at how various standard Python data processing tools handle the One Billion Row Challenge.

To run this project you will need to [install](https://docs.astral.sh/uv/getting-started/installation/) `uv` as your package manager and run:
```{sh}
uv run python src/pandas_should_go_extinct/create_1brc_data.py
```
To generate the data. This should create a `measurements.csv` and `measurements.parquet` in the `data` directory.
