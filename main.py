from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://daarekdajcz:{password}@pythonclaster.9nprnvx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)

dbs = client.list_database_names()
test_db = client.test
collections = test_db.list_collection_names()


def insert_test_doc():
    collection = test_db.test
    test_document = {
        "name": "Darek",
        "type": "Test"
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(inserted_id)


# insert_test_doc()

production = client.production
person_collection = production.person_collection


def create_document():
    first_names = ["Darek", "Natalia", "Uzi", "Szymon", "Krzysztof"]
    last_names = ["Dajcz", "Miano", "Kostka", "Kołecki", "Krawczyk"]
    ages = [28, 25, 3, 42, 65]

    docs = []

    for first_name, last_name, age in zip(first_names, last_names, ages):
        doc = {"first_name": first_name, "last_name": last_name, "age": age}
        docs.append(doc)
        # person_collection.insert_one(doc)
    person_collection.insert_many(docs)


# create_document()

printer = pprint.PrettyPrinter()


def find_all_people():
    people = person_collection.find()
    for person in people:
        printer.pprint(person)


# find_all_people()

def find_person():
    darek = person_collection.find_one({"first_name": "Darek", "last_name": "Dajcz"})
    printer.pprint(darek)


# find_person()


def count_all_people():
    count = person_collection.count_documents(filter={})
    # count = person_collection.find()count()
    printer.pprint(count)


# count_all_people()

def get_person_by_id(person_id):
    from bson.objectid import ObjectId

    _id = ObjectId(person_id)
    person = person_collection.find_one({"_id": _id})
    printer.pprint("person")
    printer.pprint(person)


# get_person_by_id("65425873c4544feae7e1820f")


def get_age_range(min_age, max_age):
    query = {
        "$and": [
            {"age": {"$gte": min_age}},
            {"age": {"$lte": max_age}},
        ]
    }
    people = person_collection.find(query).sort("age")
    for person in people:
        printer.pprint(person)


# get_age_range(20, 40)

def project_columns():
    columns = {"_id": 0, "first_name": 1, "last_name": 1}
    people = person_collection.find({}, columns)
    for person in people:
        printer.pprint(person)


# project_columns()


def update_person_by_id(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    # req_update = {
    #     "$set": {"is_developer": True, "extra_field": True},
    #     "$inc": {"age": -1},
    #     "$rename": {"Dajcz (renamed)": "surname"}
    # }
    # person_collection.update_one({"_id": _id}, req_update)
    person_collection.update_one({"_id": _id}, {"$unset": {"extra_field": ""}})


update_person_by_id("65425873c4544feae7e1820e")

def replace_person(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    doc_replace = {
        "first_name": "New Krzysztof",
        "last_name": "New Krawczyk",
        "age": 99
    }
    person_collection.replace_one({"_id": _id}, doc_replace)


replace_person("65425873c4544feae7e18212")


# def delete_doc_by_id(person_id):
#     from bson.objectid import ObjectId
#     _id = ObjectId(person_id)
#
#     person_collection.delete_one({"_id": _id})
#     # person_collection.delete_many({"_id": _id})
#
#
# delete_doc_by_id("65425873c4544feae7e18212")





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
