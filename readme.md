# Brief Cluster Cassandra / FastApi

This REST API built using FastApi provides a simple interface for performing operations on a Cassandra database.

## Dataset:

* restaurants.csv
* restaurants_inspections.csv

Unzip the two csv in the same directory as the docker-compose.yaml

## Endpoints / More info accessible at:

```bash
http://localhost:8000/docs
```

| Endpoint | Description | Path parameters |
|---|---|---|
| GET /restaurant/{id} | Retrieves information about a restaurant based on its ID | `id` |
| GET /restaurant/name/{name} | Retrieves the ID of a restaurant based on its name | `name` |
| GET /restaurant/id/{id}/name | Retrieves the name of a restaurant based on its ID | `id` |
| GET /restaurant/cuisine/{cuisine_type} | Retrieves the names of restaurants that offer a specified cuisine type | `cuisine_type` |
| GET /inspection/count/{id} | Retrieves the count of inspections for a specified restaurant ID | `id` |
| GET /restaurant/grade/{grade} | Retrieves a list of ten restaurants for a specified grade | `grade` |
| POST /restaurant | Adds a new restaurant entry | `restaurant details` |


# Api:

**To run the api:**

```bash
pip install -r requirements.txt
```

```bash
python app.py
```

## Step 1: Start the Docker containers

```bash
git clone https://github.com/Hatchi-Kin/api_Cassandra_Inspection.git
```

```bash
cd api_Cassandra_Inspection
```

Start all services defined in the `docker-compose.yml` file:

```bash
docker compose up -d
```

## Step 2: Prepare the Database before importing Data

```bash
# Create a Bash shell in the Cassandra container.
docker exec -it cas1 /bin/bash

# Connect to the Cassandra database.
cqlsh

# Create a new keyspace called `resto`.
CREATE KEYSPACE IF NOT EXISTS resto WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor': 2};

# Use the `resto` keyspace.
USE resto;

# Create a table to store the restaurant data.
CREATE TABLE IF NOT EXISTS restaurant (
  id int PRIMARY KEY,
  name varchar,
  borough varchar,
  buildingnum varchar,
  street varchar,
  zipcode int,
  phone text,
  cuisinetype varchar
);

# Describe the `restaurant` table.
DESCRIBE tables;

# Create a table to store the inspection data.
CREATE TABLE IF NOT EXISTS inspection (
  idrestaurant int,
  inspectiondate date,
  violationcode varchar,
  violationdescription varchar,
  criticalflag varchar,
  score int,
  grade varchar,
  PRIMARY KEY (idrestaurant, inspectiondate)
);

# Describe the `inspection` table.
DESCRIBE tables;

# Create an index on the `cuisinetype` column of the `restaurant` table.
CREATE INDEX IF NOT EXISTS restaurant_cuisinetype_idx ON restaurant (cuisinetype);

# Create an index on the `grade` column of the `inspection` table.
CREATE INDEX IF NOT EXISTS inspection_grade_idx ON inspection (grade);

# Copy the restaurant data file into the Cassandra container.
docker cp restaurants.csv cassandra1:/

# Copy the inspection data file into the Cassandra container.
docker cp restaurants_inspections.csv cassandra-c01:/
```

## Step 3: Import the data into the Cassandra database

```bash
# Connect to the Cassandra database.
docker exec -it cassandra1 cqlsh

# Use the `resto` keyspace.
USE resto;

# Copy the restaurant data into the `restaurant` table.
COPY restaurant (id, name, borough, buildingnum, street, zipcode, phone, cuisinetype) FROM '/restaurants.csv' WITH DELIMITER=',';

# Copy the inspection data into the `inspection` table.
COPY inspection (idrestaurant, inspectiondate, violationcode, violationdescription, criticalflag, score, grade) FROM '/restaurants_inspections.csv' WITH DELIMITER=',';
```

## Step 4: Run some basic queries

```bash
# Select just 1 entry from the table restaurant
SELECT * FROM restaurant LIMIT 1;

# Select the number of restaurants in the database.
SELECT COUNT(*) FROM restaurant;

# Select the number of inspections in the database.
SELECT COUNT(*) FROM inspection;
```

## CQL statements

```bash
docker exec -it cassandra1 cqlsh
USE resto;

# for info about restaurant based on it's ID
SELECT * FROM restaurant WHERE id = <restaurant_id>;

# for name of restaurant based on cuisine type
SELECT name FROM restaurant WHERE cuisinetype = 'American';

# Select just 1 entry from the table restaurant
SELECT * FROM restaurant LIMIT 1;

# Select the idrestaurant from inspection where grade is A
SELECT idrestaurant FROM inspection WHERE grade = 'A' LIMIT 10;
```
