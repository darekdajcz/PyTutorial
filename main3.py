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

# def find_in_collection():
#     from bson.objectid import ObjectId
#     _id = ObjectId('656b1aa66220f0eb99d58dc2')
#     darek = computer_collection.find_one({" Category": 'HISTORY'})
#     printer.pprint(darek)
#
#
# find_in_collection()