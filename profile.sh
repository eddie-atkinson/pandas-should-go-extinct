#!/bin/bash

# Script to run a Python script with iteration and warmup counts, capturing results in /usr/bin/time format, CPU%, and max RSS.

# Usage: ./run_python_script.sh <python_binary path> <python_script.py> <iterations> <warmup> <output_file.csv>
# If you use a Mac you will need to install the GNU time implementation using `brew install gnu-time`

interpreter="$1"
python_script="$2"
iterations="$3"
warmup="$4"
output_file="$5"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    time_binary="/usr/bin/time"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    time_binary="gtime"
fi

if [ ! -f "$output_file" ] || [ -z "$(cat "$output_file")" ]; then
    echo "Iteration,real,user,sys,cpu%,maxrss" >"$output_file"
fi

# Warmup
if [ $warmup -ne 0 ]; then
    echo "Performing warmup ($warmup iterations)..."
    for i in $(seq 1 "$warmup"); do
        echo "Warm up run $i"
        $interpreter "$python_script" >/dev/null
        if [ $? -ne 0 ]; then
            echo "Warning: Python script crashed during warmup iteration $i."
            exit 1
        fi
    done
fi

echo "Running measured iterations ($iterations iterations)..."
for i in $(seq 1 "$iterations"); do
    echo "Execution run $i"
    { $time_binary -p -f "%E,%U,%S,%P,%M" $interpreter "$python_script" >/dev/null; } 2>&1 | awk -F',' '{printf "%s,%s,%s,%s,%s,%s\n", "'$i'", $1, $2, $3, $4, $5}' >>"$output_file"

    if [ $? -ne 0 ]; then
        echo "Warning: Python script crashed during measured iteration $i."
        exit 1
    fi
done

echo "Results saved to $output_file"
