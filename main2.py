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

printer = pprint.PrettyPrinter()


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
                    "enum": ["Fiction", "Non-Fiction"],
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


# create_book_collection()
# create_author_validator()

def create_data():
    from datetime import datetime as dt
    authors = [
        {
            "first_name": "Darek",
            "last_name": "Dajcz",
            "date_of_birth": dt(2000, 7, 20),
        },
        {
            "first_name": "Natalia",
            "last_name": "Mianowska",
            "date_of_birth": dt(2001, 7, 20),
        },
        {
            "first_name": "Szymon",
            "last_name": "Kadziak",
            "date_of_birth": dt(2002, 7, 20),
        },
        {
            "first_name": "Robert",
            "last_name": "Kubica",
            "date_of_birth": dt(1980, 2, 11),
        }
    ]

    author_collection = production.author
    authors_id = author_collection.insert_many(authors).inserted_ids

    books = [
        {
            "title": "MongoDb Advanced Tutortial",
            "authors": [authors_id[0]],
            "publish_date": dt.today(),
            "type": "Non-Fiction",
            "copies": 5,
        },
        {
            "title": "Python for Dummies",
            "authors": [authors_id[0]],
            "publish_date": dt(2022, 7, 12),
            "type": "Fiction",
            "copies": 4,
        },
        {
            "title": "Angular Tutor to Dev",
            "authors": [authors_id[1]],
            "publish_date": dt(2021, 7, 12),
            "type": "Non-Fiction",
            "copies": 111,
        },
        {
            "title": "XXX Advanced Tutortial",
            "authors": [authors_id[2]],
            "publish_date": dt.today(),
            "type": "Fiction",
            "copies": 15,
        },
        {
            "title": "YYY Formula Tutortial",
            "authors": [authors_id[3]],
            "publish_date": dt(2011, 7, 12),
            "type": "Non-Fiction",
            "copies": 9,
        }
    ]

    book_collection = production.book
    book_collection.insert_many(books)


# create_data()
#
# books_containing_a = (
#     production.book
#     .find({"title": {"$regex": "a{1}"}})
# )
# printer.pprint(list(books_containing_a))

# authors_and_books = production.author.aggregate([{
#     "$lookup": {
#         "from": "book",
#         "localField": "_id",
#         "foreignField": "authors",
#         "as": "books"
#     }
# }])
#
# pprint.pprint(list(authors_and_books))

authors_book_count = production.author.aggregate([
    {
        "$lookup": {
            "from": "book",
            "localField": "_id",
            "foreignField": "authors",
            "as": "books"
        }
    },
    {
        "$addFields": {
            "total_books": {"$size": "$books"}
        }
    },
    {
        "$project": {"first_name": 1, "last_name": 1, "total_books": 1, "_id": 0}
    }
])

pprint.pprint(list(authors_book_count))