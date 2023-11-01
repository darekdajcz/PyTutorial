from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://daarekdajcz:{password}@pythonclaster.9nprnvx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)

# from typing import List
# from uuid import UUID
# from fastapi import FastAPI,HTTPException
# from models import User, Gender, Role
#
# app = FastAPI()
#
# db: List[User] = [
#     User(
#         id=UUID("8673cb7d-ae08-4d10-9c0d-7816f0aa6c52"),
#         first_name="Dariusz",
#         last_name="Dajcz",
#         gender=Gender.male,
#         roles=[Role.user, Role.admin]
#     ),
#     User(
#         id=UUID("596566ba-2301-456b-95c9-63c267b9483c"),
#         first_name="Alexa",
#         last_name="Jones",
#         gender=Gender.female,
#         roles=[Role.user, Role.student]
#     )
# ]
#
#
# @app.get("/")
# async def root():
#     return {"HelloS": "World"}
#
#
# @app.get("/api/v1/users")
# async def fetch_users():
#     return db
#
#
# @app.post("/api/v1/users")
# async def fetch_users(user: User):
#     db.append(user)
#     return {"id": user.id}
#
#
# @app.delete("/api/v1/users/{user_id}")
# async def delete_users(user_id: UUID):
#     for user in db:
#         if user.id == user_id:
#             db.remove(user)
#             return
#     raise HTTPException(
#         status_code=404,
#         detail=f"user with id: {user_id} does not exists"
#     )
