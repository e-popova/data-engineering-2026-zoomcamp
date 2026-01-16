 docker run -it \
  taxi_ingest:v001 \
    --network=pipeline_default \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_trips_v3 \
    --zonestable=zones