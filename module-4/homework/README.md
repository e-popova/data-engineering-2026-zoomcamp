## Steps for project setup:

1. run `pip install uv`
2. run `uv init --python=3.13`
3. run `uv add dbt-bigquery`
4. run `uv run dbt init`
5. uploaded yellow and green taxi data for 2019 and 2020 to GCP bucket
6. created external tables in BigQuery for yellow and green taxi data. Run the query for green and yellow data:

```
    CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-de-2026.zoomcamp_dbt.external_yellow_tripdata`
    OPTIONS (
      format = 'csv',
      uris = ['gs://zoomcamp-de-2026-dbt/yellow_tripdata_*.csv']
    );
```


7. created partitioned table in BigQuery based on external tables (yellow and green):

```
    CREATE OR REPLACE TABLE zoomcamp-de-2026.zoomcamp_dbt.yellow_tripdata
    PARTITION BY DATE(tpep_dropoff_datetime) 
    CLUSTER BY VendorID AS
    SELECT * FROM zoomcamp-de-2026.zoomcamp_dbt.external_yellow_tripdata;
```
   
8. set up profiles.yml and set target: prod
9. copied the code from the course repository (in case of any errors in my own workshop code)
9. run `uv run dbt build`


## Quiz Answers
### Q1: dbt run --select int_trips_unioned builds which models? 

After running this command, I see only the model `int_trips_unioned` is built. This is because only that model was in `--select  `

### Question 1. Q2: New value 6 appears in payment_type. What happens on dbt test?

When dbt will run the test, it will fail because it will return rows with payment_type = 6, which is not in the accepted values list (1,2,3,4,5).

### Q3: Count of records in fct_monthly_zone_revenue?

Run:
```
select count(*)
from zoomcamp-de-2026.zoomcamp_dbt_prod.fct_monthly_zone_revenue`
```

Answer: 12184

### Q4: Zone with highest revenue for Green taxis in 2020?

Run:
```
select pickup_zone, sum(revenue_monthly_total_amount) as rmta
from zoomcamp-de-2026.zoomcamp_dbt_prod.fct_monthly_zone_revenue
where DATE_TRUNC(revenue_month, year) = '2020-01-01'
  and service_type = 'Green'
group by pickup_zone
order by rmta DESC 
limit 1 
```
Answer: East Harlem North	1817459.15	

### Q5: Total trips for Green taxis in October 2019?

Run:
```
select  sum(total_monthly_trips) as tmt
from zoomcamp-de-2026.zoomcamp_dbt_prod.fct_monthly_zone_revenue
where revenue_month = '2019-10-01'
  and service_type = 'Green'
```
Answer: 384624

### Q6: Count of records in stg_fhv_tripdata (filter dispatching_base_num IS NULL)?
Steps:
- Uploaded fhv trip data for 2019 GCP bucket and created a table based on it.
- Checked the data description at https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_fhv.pdf
- Added table definition to models/staging/sources.yml
- Run: `uv run dbt run-operation generate_base_model --args '{"source_name": "raw", "table_name": "fhv_tripdata"}'`
- Created a model `stg_fhv_tripdata` based on the generated base model but with the changes required by the task
- Run  `uv run dbt run --select stg_fhv_tripdata`
- Run:
```
select count(*)
from zoomcamp-de-2026.zoomcamp_dbt_prod.stg_fhv_tripdata
```

Answer: 43 244 693