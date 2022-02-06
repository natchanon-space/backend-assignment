from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

class Reservation(BaseModel):
    name : str
    time: int
    table_number: int
    
client = MongoClient('mongodb://localhost', 27017)

# TODO fill in database name
db = client["restaurants"]

# TODO fill in collection name
collection = db["reservation"]

mylist = client.list_database_names()
print(mylist)

app = FastAPI()


# TODO complete all endpoint.
@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    result = collection.find_one({"name": name})
    return {
        "name": result["name"],
        "table": result["table"],
        "time": result["time"]
    }

@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    result = collection.find_one({"table": table})
    return {
        "name": result["name"],
        "table": result["table"],
        "time": result["time"]
    }

@app.post("/reservation")
def reserve(reservation : Reservation):
    pass

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    pass

