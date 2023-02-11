from fastapi import FastAPI, Request
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware 
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
x=0
@app.get("/profile")
async def get_all_profiles():
    mulprofiles = await db["profile"].find().to_list(999)
    if len(mulprofiles) == 0:
        return "No profile present"
    return mulprofiles[0]

@app.post("/profile")
async def create_new_profile(request: Request):
    profile_obj = await request.json()

    new_profile = await db["profile"].insert_one(profile_obj)
    created_profile = await db["profile"].find_one({"_id": new_profile.inserted_id})
    return created_profile

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
