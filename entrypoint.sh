#!/bin/bash

# Import yellow taxi information
python ingest_data_yellow.py --user=root --password=root --host=pgdatabase --port=5432 --db=ny_taxi --table_name=yellow_taxi_trips --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz  

# Check it worked
if [ $? -eq 0 ]; then
    # Import green taxi information
    python ingest_data_green.py --user=root --password=root --host=pgdatabase --port=5432 --db=ny_taxi --table_name=green_taxi_trips --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz 

else 
    echo "Error - the first script failed, skipping the second script"
fi


