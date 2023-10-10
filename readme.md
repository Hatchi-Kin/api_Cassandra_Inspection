# 🧑🏻‍💻  Brief Cluster Cassandra / FastApi  
This REST API built using FastApi provides a simple interface for performing operations on a Cassandra database.


## 💾 Dataset:
restaurants.csv
restaurants_inspections.csv


##  🧐  Endpoints / More info accessible at:
```bash
http://localhost:8000/docs
```

## 🙇 Api
To run the api:
* In /api-REST_Mongodb-CRUD
```bash
pip install -r requirements.txt
```
```bash
streamlit run app.py
```   

## 🛠️ Deployment:
* Navigate to the directory where you want to download the repo then run the following commands:
```bash
git clone https://github.com/Hatchi-Kin/api-REST_Mongodb-CRUD.git
```
```bash
cd api-REST_Mongodb-CRUD
```

```markdown
## Step 1: Start the Docker containers

```bash
# Start all services defined in the docker-compose.yml file.
docker compose up -d
```

## Step 2: Import the restaurant data

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



## Step 3: Copy the data files into the Docker container

```bash
# Copy the restaurant data file into the Cassandra container.
docker cp restaurants.csv cassandra1:/

# Copy the inspection data file into the Cassandra container.
docker cp restaurants_inspections.csv cassandra-c01:/
```

## Step 4: Import the data into the Cassandra database

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

## Step 5: Run some basic queries

```bash
# Select just 1 entry from the table restaurant
SELECT * FROM restaurant LIMIT 1;

# Select the number of restaurants in the database.
SELECT COUNT(*) FROM restaurant;

# Select the number of inspections in the database.
SELECT COUNT(*) FROM inspection;
```

# CQL statement
```bash
docker exec -it cassandra1 cqlsh
USE resto;
```
```bash
# for info about restaurant based on it's ID
SELECT * FROM restaurant WHERE id = <restaurant_id>;
```
```bash
# for name of restaurant based on cuisine type
SELECT name FROM restaurant WHERE cuisinetype = 'American';
```
```bash
SELECT * FROM restaurant LIMIT 1;
```

```bash
SELECT idrestaurant FROM inspection WHERE grade = 'A' LIMIT 10;
```
