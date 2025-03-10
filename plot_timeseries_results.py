from pathlib import Path
from main import DUCKDB_OUTPUT_PATH, PANDAS_OUTPUT_PATH, POLARS_OUTPUT_PATH
import seaborn as sns
import matplotlib.pyplot as plt

import polars as pl

FIGURES_DIR = Path("./figures")


def format_rss(value):
    if value >= 1024**3:
        return f"{value / (1024**3):.2f} GB"
    elif value >= 1024**2:
        return f"{value / (1024**2):.2f} MB"
    elif value >= 1024:
        return f"{value / (1024):.2f} KB"
    else:
        return f"{value:.0f} B"


def plot_df(df: pl.DataFrame, title: str, ax):
    sns.lineplot(x="time_s", y="rss", hue="run_no", data=df, ax=ax, legend=False)
    ax.set_title(title)
    y_values = ax.get_yticks()
    ax.set_yticklabels([format_rss(y) for y in y_values])
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("RSS")
    ax.grid(True)


df_polars = pl.read_csv(POLARS_OUTPUT_PATH)
df_pandas = pl.read_csv(PANDAS_OUTPUT_PATH)
df_duckdb = pl.read_csv(DUCKDB_OUTPUT_PATH)

fig, axes = plt.subplots(3, 1, figsize=(10, 15))
plot_df(df_polars, "Polars RSS Over Time", axes[0])
plot_df(df_duckdb, "DuckDB RSS Over Time", axes[1])
plt.tight_layout()
plt.savefig(FIGURES_DIR / "timeseries.png")
