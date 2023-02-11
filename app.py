from fastapi import FastAPI, Request
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware 
from datetime import datetime
import motor.motor_asyncio
import pydantic

app = FastAPI()

origins=[
    "http://localhost:8000",
    "https://ecse3038-lab3-tester.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://week4:oKbzC9wuJa6nIJKI@cluster0.ldjatx3.mongodb.net/?retryWrites=true&w=majority")

db = client.water_tank
#dbb = client.actual_water_tank_details

@app.get("/profile")
async def get_all_profiles():
    mulprofiles = await db["profile"].find().to_list(999)
    if len(mulprofiles) == 0:
        return "No profile present"
    return mulprofiles[0]

@app.post("/profile",status_code=201)
async def create_new_profile(request: Request):
    profile_obj = await request.json()
    profile_obj["last_updated"]=datetime.now()

    new_profile = await db["profile"].insert_one(profile_obj)
    created_profile = await db["profile"].find_one({"_id": new_profile.inserted_id})
    return created_profile

@app.get("/data",status_code=201)
async def get_all_data():
    tank_data = await db["data"].find().to_list(999)
    return tank_data

@app.get("/data/{id}")
async def get_one_tank(id: str):
    tank_one = await db["data"].find_one({"_id": ObjectId(id)})
    return tank_one

@app.post("/data",status_code=201)
async def create_new_tank(request: Request):
    tank_obj = await request.json()

    new_tank = await db["data"].insert_one(tank_obj)
    created_tank = await db["data"].find_one({"_id": new_tank.inserted_id})
    return created_tank

""""
@app.post("/todos")
async def create_new_todo(request: Request):
    todo_object = await request.json()

    new_todo = await db["todos"].insert_one(todo_object)
    created_todo = await db["todos"].find_one({"_id": new_todo.inserted_id})

    return created_todo

@app.get("/todos")
async def get_all_todos():
    todos = await db["todos"].find().to_list(999) 
    return todos

@app.get("/todo/{id}")
async def get_one_todo_by_id(id:str):
    todo = await db["todos"].find_one({"_id": ObjectId(id)})
    return todo
"""
