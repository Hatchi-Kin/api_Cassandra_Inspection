from fastapi import FastAPI, Depends
from cassandra.cluster import Cluster
import uvicorn
import random


app = FastAPI()


# Establishing two separate Cassandra clusters for load balancing
cluster1 = Cluster(['localhost'], port=9042)
session1 = cluster1.connect('resto')
session1.execute('USE resto')

cluster2 = Cluster(['localhost'], port=9043)
session2 = cluster2.connect('resto')
session2.execute('USE resto')
'''
# deuxieme possibilité = mettre les deux nodes dans le même cluster et de faire un load balancing avec le driver
cluster = Cluster(['172.26.0.2', '172.26.0.2'])
session = cluster.connect("resto")
session.execute('USE resto')

'''
##################################################################
def is_node_up(session):
    try:
        session.execute('SELECT * FROM system.local')
        return True
    except Exception:
        return False
    
# Function to select a Cassandra session based on the provided ID.
# If no ID is provided, a session is randomly selected.
def get_session(id: int = None):
    if id is None:
        session = random.choice([session1, session2])
        return session if is_node_up(session) else None
    elif id % 2 == 0:
        return session1 if is_node_up(session1) else None
    else:
        return session2 if is_node_up(session2) else None
    
##################################################################

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return {"error": str(exc)}


@app.get('/restaurant/{id}')
# Get info about a restaurant based on it's id in the database
def get_one(id: int, session = Depends(get_session)):
    row = session.execute(f'SELECT * FROM restaurant WHERE id = {id}')
    return row.one()


@app.get('/restaurant/name/{name}')
# Get the ID of a restaurant based on its name
def get_id_by_name(name: str, session = Depends(get_session)):
    row = session.execute(f"SELECT id FROM restaurant WHERE name = '{name}' ALLOW FILTERING")
    return row.one().id


@app.get('/restaurant/id/{id}/name')
# Get the name of a restaurant based on its ID
def get_name_by_id(id: int, session = Depends(get_session)):
    row = session.execute(f"SELECT name FROM restaurant WHERE id = {id} ALLOW FILTERING")
    return row.one().name


@app.get('/restaurant/cuisine/{cuisine_type}')
# Get the name of the restaurants that propose a specified cuisine type
def get_by_cuisine(cuisine_type: str, session = Depends(get_session)):
    rows = session.execute(f"SELECT name FROM restaurant WHERE cuisinetype = '{cuisine_type}' LIMIT 10")
    return rows.all()


@app.get('/inspection/count/{id}')
# Get the count of inspections for the specified restaurant id
def get_inspection_count(id: int, session = Depends(get_session)):
    rows = session.execute(f"SELECT COUNT(*) FROM inspection WHERE idrestaurant = {id}")
    # Get the count from the first row returned by the query
    count = rows[0][0]
    return count


@app.get('/restaurant/grade/{grade}')
# Get a list of ten restaurants for a specified grade
def get_by_grade(grade: str, session = Depends(get_session)):
    # query on the inspection table to get the IDs THEN query on the restaurant table to get the names
    rows = session.execute(f"SELECT idrestaurant FROM inspection WHERE grade = '{grade}' LIMIT 10")
    ids = [row.idrestaurant for row in rows]
    rows = session.execute(f"SELECT name FROM restaurant WHERE id IN {tuple(ids)}")
    results = [row.name for row in rows]
    return results


@app.post('/restaurant')
# Add a new restaurant entry
def add_restaurant(id: str, name: str, borough: str, buildingnum: str, street: str, zipcode: str, phone: str, cuisinetype: str, session = Depends(get_session)):
    id_int = int(id)  # Convert id to integer
    zipcode_int = int(zipcode)  # Convert zipcode to integer
    try:
        session.execute(f"""
            INSERT INTO restaurant (id, name, borough, buildingnum, street, zipcode, phone, cuisinetype) 
            VALUES ({id_int}, '{name}', '{borough}', '{buildingnum}', '{street}', {zipcode_int}, '{phone}', '{cuisinetype}')
        """)
        return {'message': 'Restaurant added successfully'}
    except Exception as e:
        raise Exception(f"Error adding restaurant: {str(e)}")

##################################################################

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)