from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://daarekdajcz:{password}@pythonclaster.9nprnvx.mongodb.net/?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(connection_string)

dbs = client.list_database_names()
production = client.production


def create_book_collection():
    book_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "authors", "publish_date", "type", "copies"],
            "properties": {
                "title": {
                    "bsonType": "string",
                    "description": "must  be a string and required"
                },
                "authors": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId",
                        "description": "must  be a string and required"
                    }
                },
                "publish_date": {
                    "bsonType": "date",
                    "description": "must  be a date and required"
                },
                "type": {
                    "enum": ["Ficition", "Non-Fiction"],
                    "description": "can only be one of the enum values and is required"
                },
                "copies": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be an integer greater than 0 ani is required"
                }
            }
        }
    }

    try:
        production.create_collection("book")
    except Exception as e:
        print(e)

    production.command("collMod", "book", validator=book_validator)


def create_author_validator():
    author_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["first_name", "last_name", "date_of_birth"],
            "properties": {
                "first_name": {
                    "bsonType": "string",
                    "description": "must  be a string and required"
                },
                "last_name": {
                    "bsonType": "string",
                    "description": "must  be a string and required"
                },
                "date_of_birth": {
                    "bsonType": "date",
                    "description": "must  be a date and required"
                }
            }
        }
    }

    try:
        production.create_collection("author")
    except Exception as e:
        print(e)

    production.command("collMod", "author", validator=author_validator)


create_book_collection()
create_author_validator()
