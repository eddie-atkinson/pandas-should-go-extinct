import pandas as pd

from constants import DATA_PATH


def do_1brc_pandas(file_path: str, output_data=True) -> str:
    """
    Perform the 1BRC using Pandas, this function will likely OOM if you do not have a reasonable quantity of RAM (> 32GB)

    Note: the output serialisation isn't a main focus of this test for performance purposes,
    so there is an option not to serialise the output. However, having the output is useful for testing correctness
    """
    df = (
        pd.read_csv(file_path, sep=";", names=["station", "measurement"])
        .groupby("station")
        .agg({"measurement": ["min", "mean", "max"]})
        .round(2)
    )

    if output_data:
        result = []
        for station, min_val, mean_val, max_val in df.to_records():
            result.append(f"{station}={min_val}/{mean_val}/{max_val}")
        return "{" + ", ".join(result) + "}"
    return ""


def main():
    do_1brc_pandas(DATA_PATH, output_data=False)


if __name__ == "__main__":
    main()
