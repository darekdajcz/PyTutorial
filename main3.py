from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://daarekdajcz:{password}@pythonclaster.9nprnvx.mongodb.net/?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(connection_string)

dbs = client.list_database_names()
computerDB = client.computerDB
computer_collection = computerDB.computer

printer = pprint.PrettyPrinter()

indexes = computer_collection.index_information()
printer.pprint(indexes)


# computer_collection.create_index([(" Category", "text")])

# def find_in_collection():
#     from bson.objectid import ObjectId
#     _id = ObjectId('656b1aa66220f0eb99d58dc2')
#     darek = computer_collection.find({" Category": "HISTORY"})
#     printer.pprint(list(darek))
#
#
# find_in_collection()

# def find_in_by_index_collection():
#     computer_collection.drop_index(' Value_text')
#     computer_collection.create_index([(" Category", "text")])
#
#     results = computer_collection.find({"$text": {"$search": "HISTORY"}})
#
#     printer.pprint(list(results))
#
#
# find_in_by_index_collection()
#
# def find_in_by_index_collection_with_text_score():
#     results = (computer_collection
#                .find(
#         {"$text": {"$search": "HISTORY"}},
#         {"score": {"$meta": "textScore"}})
#                .sort([("score",
#                        {"$meta": "textScore"}
#                        )]))
#
#     printer.pprint(list(results))
#
#
# find_in_by_index_collection_with_text_score()

def find_in_by_index_collection_with_fuzzy():
    query = {
        "$text": {
            "$search": "History",
            "$caseSensitive": False,
            "$diacriticSensitive": False
        }
    }

    results = computer_collection.find(query)
    printer.pprint(list(results))


find_in_by_index_collection_with_fuzzy()
