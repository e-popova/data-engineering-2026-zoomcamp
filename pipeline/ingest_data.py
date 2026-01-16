#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--db', default='ny_taxi', help='PostgreSQL database')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--year', default=2021, type=int, help='Year of data')
@click.option('--month', default=1, type=int, help='Month of data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
@click.option('--table', default='yellow_taxi_data', help='Target table name for trips')
@click.option('--zonestable', default='zones', help='Target table name for zones')


def run(user, password, host, db, port, year, month, chunksize, table, zonestable):
    prefix_trips = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    file_name_trips = f'yellow_tripdata_{year}-{month:02d}.csv.gz'
    url_trips = f'{prefix_trips}/{file_name_trips}'

    prefix_zones = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/'
    file_name_zones = 'taxi_zone_lookup.csv'
    url_zones = f'{prefix_zones}/{file_name_zones}'


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read and ingest trips data in chunks
    df_iter = pd.read_csv(
        url_trips,
        dtype=dtype,
        parse_dates=parse_dates,
        chunksize=chunksize,
    )

    first = True

    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.to_sql(name=table, con=engine, if_exists='replace')
            first = False
        else:
            df_chunk.to_sql(name=table, con=engine, if_exists='append')

    # Read and ingest zones data
    df = pd.read_csv(url_zones)
    df.to_sql(name=zonestable, con=engine, if_exists='replace')


if __name__ == '__main__':
    run()

