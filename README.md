## 1 Billion Row Challenge Benchmarking
This is a somewhat scientific look at how various standard Python data processing tools handle the One Billion Row Challenge.

To run this project you will need to [install](https://docs.astral.sh/uv/getting-started/installation/) `uv` as your package manager and run:
```{sh}
uv venv
uv run python src/pandas_should_go_extinct/create_1brc_data.py
```
To generate the data. This should create a `measurements.csv` and `measurements.parquet` in the `data` directory.

To run tests using the GNU `time` command do:
```{sh}
chmod +x ./run_profile.sh ./profile.sh
./run_profile.sh
```
If you are using a Mac you will need to install GNU time using `brew install gtime`.

To summarise the results you can use:
```{sh}
uv run process_gtime_results.py
```

To get timeseries data regarding RSS and CPU % using `psutil` run:
```{sh}
uv run main.py
```

To plot the outputs run:
```{sh}
uv run plot_timeseries_results.py
```

This will produce a figure in `figures/timeseries.png`

## General Experimentation Approach
I have opted to use `time` as a simple profiling mechanism for run time as it should have a relatively low overhead and our focus for the `time` tests is the user observed run time, as this is ultimately what we pay $CLOUD_PROVIDER for and what our employer pays us for.

For the purposes of plotting `psutil` is also used. Given the naive approach to sampling (read info from `psutil` every ~50ms) I wouldn't trust the runtime statistics for these tests as it's possible the capturing of statistics competes for CPU time and/or causes cache coherency problems. The aim for this script is really to see how the resident set size (RSS) changes over time