from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

class Reservation(BaseModel):
    name : str
    time: int
    table: int
    
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

    if result is not None:
        return {
            "name": result["name"],
            "table": result["table"],
            "time": result["time"]
        }
    return {"msg": "not found reservation"}

@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    result = collection.find_one({"table": table})

    if result is not None:
        return {
            "name": result["name"],
            "table": result["table"],
            "time": result["time"]
        }
    return {"msg": "not found reservation"}

@app.post("/reservation")
def reserve(reservation : Reservation):
    reserved_table = []
    reserved_name = []
    reserved_time = []
    results = collection.find()
    for r in results:
        reserved_name.append(r["name"])
        reserved_table.append(r["table"])
        reserved_time.append(r["time"])

    if reservation.name in reserved_name:
        return {"msg": f"{reservation.name} is already resererved"}
    if reservation.table in reserved_table:
        return {"msg": f"table {reservation.table} is already reserved"}
    if reservation.time in reserved_time:
        return {"msg": f"at {reservation.time} is already reserved"}
    
    collection.insert_one({
        "name": reservation.name,
        "table": reservation.table,
        "time": reservation.time
    })
    return {"msg": f"done!"}

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    collection.delete_one({"name": name, "table": table_number})
    return {"msg": "deleted"}

