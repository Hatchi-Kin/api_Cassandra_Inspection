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
Navigate to the directory where you want to download the repo then run the following commands:
```bash
git clone https://github.com/Hatchi-Kin/api-REST_Mongodb-CRUD.git
```
```bash
cd api-REST_Mongodb-CRUD
```

## Step 1: Start the Docker containers
Start all services defined in the docker-compose.yml file.
```bash
docker compose up -d
```

## Step 2: Import the restaurant data
```bash
# Create a Bash shell in the Cassandra container.
docker exec -it cas1 /bin/bash
```

Connect to the Cassandra database.
```bash
cqlsh
```

Create a new keyspace called `resto`.
```bash
CREATE KEYSPACE IF NOT EXISTS resto WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor': 2};
```
Use the `resto` keyspace.
```bash
USE resto;
```

Create a table to store the restaurant data.
```bash
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
```

Describe the `restaurant` table.
```bash
DESCRIBE tables;
```

Create a table to store the inspection data.
```bash
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
```

Describe the `inspection` table.
```bash
DESCRIBE tables;
```

Create an index on the `cuisinetype` column of the `restaurant` table.
```bash
CREATE INDEX IF NOT EXISTS restaurant_cuisinetype_idx ON restaurant (cuisinetype);
```

Create an index on the `grade` column of the `inspection` table.
```bash
CREATE INDEX IF NOT EXISTS inspection_grade_idx ON inspection (grade);
```

## Step 3: Copy the data files into the Docker container
Copy the restaurant data file into the Cassandra container.
```bash
docker cp restaurants.csv cassandra1:/
```

Copy the inspection data file into the Cassandra container.
```bash
docker cp restaurants_inspections.csv cassandra-c01:/
```

## Step 4: Import the data into the Cassandra database

Connect to the Cassandra database.
```bash
docker exec -it cassandra1 cqlsh
```

Use the `resto` keyspace.
```bash
USE resto;
```

Copy the restaurant data into the `restaurant` table.
```bash
COPY restaurant (id, name, borough, buildingnum, street, zipcode, phone, cuisinetype) FROM '/restaurants.csv' WITH DELIMITER=',';
```

Copy the inspection data into the `inspection` table.
```bash
COPY inspection (idrestaurant, inspectiondate, violationcode, violationdescription, criticalflag, score, grade) FROM '/restaurants_inspections.csv' WITH DELIMITER=',';
```

## Step 5: Run some basic queries

Select just 1 entry from the table restaurant
```bash
SELECT * FROM restaurant LIMIT 1;
```
Select the number of restaurants in the database.
```bash
SELECT COUNT(*) FROM restaurant;
```
Select the number of inspections in the database.
```bash
SELECT COUNT(*) FROM inspection;
```

CQL statements
```bash
docker exec -it cassandra1 cqlsh
USE resto;
```
for info about restaurant based on it's ID
```bash
SELECT * FROM restaurant WHERE id = <restaurant_id>;
```
for name of restaurant based on cuisine type
```bash
SELECT name FROM restaurant WHERE cuisinetype = 'American';
```
```bash
SELECT * FROM restaurant LIMIT 1;
```
```bash
SELECT idrestaurant FROM inspection WHERE grade = 'A' LIMIT 10;
```
