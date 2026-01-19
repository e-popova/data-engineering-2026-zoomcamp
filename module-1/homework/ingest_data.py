#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine

@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--db', default='ny_taxi_green', help='PostgreSQL database')
@click.option('--port', default=5433, type=int, help='PostgreSQL port')
@click.option('--year', default=2025, type=int, help='Year of data')
@click.option('--month', default=11, type=int, help='Month of data')
@click.option('--table', default='yellow_taxi_data', help='Target table name for trips')
@click.option('--zonestable', default='zones', help='Target table name for zones')

def run(user, password, host, db, port, year, month, table, zonestable):
    prefix_trips = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    file_name_trips = f'green_tripdata_{year}-{month:02d}.parquet'
    url_trips = f'{prefix_trips}/{file_name_trips}'

    prefix_zones = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc'
    file_name_zones = 'taxi_zone_lookup.csv'
    url_zones = f'{prefix_zones}/{file_name_zones}'

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read and ingest trips data in chunks
    df = pd.read_parquet(url_trips)
    df.to_sql(name=table, con=engine, if_exists='replace')


    # Read and ingest zones data
    df = pd.read_csv(url_zones)
    df.to_sql(name=zonestable, con=engine, if_exists='replace')


if __name__ == '__main__':
    run()


