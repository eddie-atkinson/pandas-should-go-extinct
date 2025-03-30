#!/bin/bash

BASE_URL=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_
YEARS=(2021 2022)
MONTHS=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12")

for year in "${YEARS[@]}"; do
	for month in "${MONTHS[@]}"; do
		DATE="${year}-${month}"
		URL="${BASE_URL}${DATE}.parquet"
		curl $URL -o "${DATE}.parquet"
	done
done
