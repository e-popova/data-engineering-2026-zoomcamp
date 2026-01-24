# Module 2 - Homework 
## Implementation Steps
Prepared docker-compose file: 
- created docker-compose.yaml to use Kestra locally
- put my GCP credentials to keys/my-creds.json (and gitignored that file)
- used command "cat my-creds.json | base64 -w 0" to encode my credentials to base64
- used command "export GOOGLE_CREDS='<encoded credentials>'" to set environment variable with encoded string
- added using that environment variable in docker-compose.yaml for secrets
- run "docker compose up"

Then the following flows were created (see in the [module-2/homework/flows/]()) 
- `gcp_create.yaml` sets up GCP bucket and bigquery dataset 
- `gcp_taxi.yaml is` the main flow which executes gcp_taxi_subflow.yaml for every month in a given month range
- `gcp_taxi_subflow.yaml` is a subflow to download, upload to GCP bucket and ingest to bigquery one month of taxi data

## Quiz Questions
1. Execute gcp_taxi.yaml with inputs:
    - taxi: yellow
    - from: 2020-12-01
    - to: 2020-12-01
   
   In GCP Bucket the file yellow_tripdata_2020-12.csv is 134.5 MB


2. Execute gcp_taxi.yaml with inputs:
    - taxi: green
    - from: 2020-04-01
    - to: 2020-04-01
   
    In gcp_taxi_subflow execution the file label value is "green_tripdata_2020-04.csv"


3. Execute gcp_taxi.yaml with inputs:
    - taxi: yellow
    - from: 2020-01-01
    - to: 2020-12-01
   
    In GCP bigquery run query:
    ```
    select count()
    from zoomcamp_homework.yellow_tripdata
    where filename like 'yellow_tripdata_2020%'
    ```
    The result is 24 648 499

4. Execute gcp_taxi.yaml with inputs:
    - taxi: green
    - from: 2020-01-01
    - to: 2020-12-01
   
    In GCP bigquery run query:
    ```
    select count(*)
    from zoomcamp_homework.green_tripdata
    where filename like 'green_tripdata_2020%'
    ```
    The result is 1 734 051
5. Execute gcp_taxi.yaml with inputs:
    - taxi: yellow
    - from: 2021-03-01
    - to: 2021-03-01

    In GCP bigquery run query:
    ```
    select count(*)
    from zoomcamp_homework.yellow_tripdata
    where filename = 'yellow_tripdata_2021-03.csv'
    ```
    The result is 1 925 152

6. Correct answer: timezone: America/New_York 

    The first ("EST") and third ("UTC-5") options don’t take the time change into account (EDT ↔ EST).
    The fourth option ("New_York") is just wrong.
    


