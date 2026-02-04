# Module 3 - Homework
## Steps
- Downloaded Parquet files from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Manually created a bucket 'bq_homework' in GCP Cloud Storage and uploaded files 
- Created a dataset 'bq_homework' in GCP BigQuery
- Created external table using:
    ```
    CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-de-2026.bq_homework.external_yellow_tripdata`
    OPTIONS (
      format = 'Parquet',
      uris = ['gs://bq_homework/yellow_tripdata_2024-*.parquet']
    );
    ```
- Created a non partitioned table from external table
    ```
  CREATE OR REPLACE TABLE zoomcamp-de-2026.bq_homework.yellow_tripdata_non_partitioned AS
    SELECT * FROM zoomcamp-de-2026.bq_homework.external_yellow_tripdata;
  ```

## Quiz Answers

### Question 1 - Answer
- In GCP BigQuery run query:
    ```
    -- First option
    select count(*)
    from `zoomcamp-de-2026.bq_homework.external_yellow_tripdata`;
    -- Second option
    select count(*)
    from `zoomcamp-de-2026.bq_homework.yellow_tripdata_non_partitioned`;
    ```
- The result is 20332093

### Question 2 - Answer
- In GCP BigQuery prepare queries:
    ```
    -- Query for external table
    select count(distinct(PULocationID))
    from `zoomcamp-de-2026.bq_homework.external_yellow_tripdata`
    
    -- Query for regular table
    select count(distinct(PULocationID))
    from `zoomcamp-de-2026.bq_homework.yellow_tripdata_non_partitioned`
    ```
- The estimated amount of data that will be read is: 
  - 0 MB for the External Table
  - 155.12 MB for the Regular Table

### Question 3 - Answer
- In GCP BigQuery prepare queries:
    ```
    select PULocationID
    from `zoomcamp-de-2026.bq_homework.yellow_tripdata_non_partitioned`
    
    select PULocationID, DOLocationID
    from `zoomcamp-de-2026.bq_homework.yellow_tripdata_non_partitioned`
    ```
- The estimated amount of data that will be read is: 
  - 155.12 MB for the first query
  - 310.24 MB for the second query
- The reason why estimated amount of data read is because: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

### Question 4 - Answer
- In GCP BigQuery run query:
    ```
    select count(*)
    from `zoomcamp-de-2026.bq_homework.yellow_tripdata_non_partitioned`
    where fare_amount = 0
    ```
- The result is 8333

### Question 5 - Answer
- The Answer is: Partition by tpep_dropoff_datetime and Cluster on VendorID
- In GCP BigQuery run query:
    ```
    CREATE OR REPLACE TABLE zoomcamp-de-2026.bq_homework.yellow_tripdata_optimized
    PARTITION BY DATE(tpep_dropoff_datetime) 
    CLUSTER BY VendorID AS
    SELECT * FROM zoomcamp-de-2026.bq_homework.external_yellow_tripdata;
    ```
  
### Question 6 - Answer
- In GCP BigQuery prepare queries:
    ```
    -- Query for regular table
    select count(distinct(PULocationID))
    from `zoomcamp-de-2026.bq_homework.yellow_tripdata_non_partitioned`
    where date(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-15'
    
    -- Query for optimized table
    select count(distinct(PULocationID))
    from `zoomcamp-de-2026.bq_homework.yellow_tripdata_optimized`
    where date(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-15'
    ```
- The estimated amount of data that will be read is: 
  - 310.24 MB for the first query
  - 26.84 MB for the second query

### Question 7 - Answer
- The answer is in GCP Bucket because it's external table

### Question 8 - Answer
- The answer is false, because clustering is not always a good idea, e.g.:
  - if the column has low cardinality
  - if the table is small
  - if the most of the queries do not filter or aggregate on the clustered columns
  - if we need to control costs tightly

### Question 9 - Answer
- In GCP BigQuery prepare query:
    ``` 
    select count(*) 
    from `zoomcamp-de-2026.bq_homework.yellow_tripdata_non_partitioned`;
    ```
- The estimated amount of data is 0B because this information could be taken from the table metadata since there is no additional filters  
