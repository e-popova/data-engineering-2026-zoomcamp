# Homework - Module 1

## Question 1 - Understanding Docker images

Input:
```
docker run -it --rm --entrypoint=bash python:3.13
pip -V
```
Output:
```
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

## Question 2. Understanding Docker networking and docker-compose
Input:
```
docker compose up 
```
In pgadmin it was possible to connect to the database using the following parameters:
- db:5432 
- postgres:5432 

---
To create a container with a pipeline run:
```
docker build -t taxi_ingest:v003 .
docker run -it \
    --network=homework_default \
  taxi_ingest:v003 \
    --user=root \
    --password=pass \
    --host=db \
    --db=ny_taxi \
    --port=5432 \
    --table=green_taxi_trips\
    --zonestable=green_taxi_zones
```

## Question 3. Counting short trips
``` 
select count(*) 
from public.green_taxi_trips 
where lpep_pickup_datetime between '2025-11-01 00:00:00' and '2025-11-30 23:59:59'
	and trip_distance <= 1 
```
```
8007
```

## Question 4. Longest trip for each day
```
select date(lpep_pickup_datetime)
from public.green_taxi_trips 
where trip_distance = (
	select 	max(trip_distance) max_td
	from public.green_taxi_trips 
	where trip_distance < 100)
```
```
2025-11-14
```

## Question 5. Biggest pickup zone
```
select z."LocationID" lid, 
	z."Zone" z, 
	sum(total_amount) as ta
from public.green_taxi_trips t
left join public.green_taxi_zones z on t."PULocationID"=z."LocationID"
where date(lpep_pickup_datetime) = '2025-11-18'
group by lid, z
order by ta DESC 
```
```
74	"East Harlem North"	9281.920000000004
...
```


## Question 6. Largest tip
```
select doz."LocationID" did, 
	doz."Zone" dz, 
	max(tip_amount) as ta
from public.green_taxi_trips t
left join public.green_taxi_zones puz on t."PULocationID"=puz."LocationID"
left join public.green_taxi_zones doz on t."DOLocationID"=doz."LocationID"
where lpep_pickup_datetime between '2025-11-01 00:00:00' and '2025-11-30 23:59:59'
	and puz."Zone" = 'East Harlem North'
group by did, dz
order by ta DESC 
```
```
263	"Yorkville West"	81.89
...
```