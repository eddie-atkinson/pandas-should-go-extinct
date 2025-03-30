from pandas_should_go_extinct.constants import TAXI_PATH
from pandas_should_go_extinct.hybrid_duck_taxi import (
    do_taxi_duck,
    do_taxi_duck_compute,
    do_taxi_duck_read,
    do_taxi_pandas,
)
import sys

PANDAS_ONLY = "pandas"
DUCK_ONLY = "duck"
PANDAS_DUCK_READ = "duck_read"
PANDAS_READ_DUCK_THINK = "duck_compute"
OPTIONS = [PANDAS_ONLY, PANDAS_DUCK_READ, PANDAS_READ_DUCK_THINK, DUCK_ONLY]

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in OPTIONS:
        print(f"Usage pandas_duck_hybrid.py [{PANDAS_ONLY} | {PANDAS_DUCK_READ} | {PANDAS_READ_DUCK_THINK} | {DUCK_ONLY}]")
    
    opt = sys.argv[1]
    if opt == PANDAS_ONLY:
        do_taxi_pandas(TAXI_PATH)
    elif opt == PANDAS_DUCK_READ:
        do_taxi_duck_read(TAXI_PATH)
    elif opt == PANDAS_READ_DUCK_THINK:
        do_taxi_duck_compute(TAXI_PATH)
    elif opt == DUCK_ONLY:
        do_taxi_duck(TAXI_PATH)
