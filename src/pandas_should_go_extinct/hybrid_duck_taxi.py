from pathlib import Path
import duckdb
import pandas as pd

COLUMNS = ["tpep_pickup_datetime", "payment_type"]

def do_taxi_hybrid_duck(folder: Path):
    df = None
    for entry in folder.iterdir():
        if not entry.name.endswith("parquet"): continue
        df = pd.concat([df, pd.read_parquet(entry, columns=COLUMNS, dtype_backend="pyarrow")], axis="index") if df is not None else pd.read_parquet(entry, columns=COLUMNS, dtype_backend="pyarrow")
    

    df = df[df["tpep_pickup_datetime"] > "2019-01-01" & (df["tpep_pickup_datetime"] < "2023-01-01")]
    


