import os 
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    zones_url = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv'

    if url.endswith('.csv.gz'):
        csv_name = 'yellow_output.csv.gz'
    else:
        csv_name = 'yellow_output.csv'

    os.system(f"wget {url} -O {csv_name}")
    os.system(f"wget {zones_url} -O {'zones.csv'}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    zones_df = pd.read_csv('zones.csv')
    zones_df.to_sql(name='zones', con=engine, if_exists='replace')

    while True:

        try:
            t_start = time()

            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists="append")

            t_end = time()

            print("inserted another chunk, took %.3f second" % (t_end - t_start))
        
        except StopIteration:
            print("Finishing with all the ingesting.")
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingesting data from csv to Postgres")

    parser.add_argument('--user', help='username for Postgres')
    parser.add_argument('--password', help='password for Postgres')
    parser.add_argument('--host', help='host for Postgres')
    parser.add_argument('--port', help='port for Postgres')
    parser.add_argument('--db', help='database name for Postgres')
    parser.add_argument('--table_name', help='table where results will be written to')
    parser.add_argument('--url', help='url of CSV file')

    args = parser.parse_args()

    main(args)
