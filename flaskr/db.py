import pymongo
import click
from flask import Flask, current_app, g
from . import create_app

conn_str = "mongodb://127.0.0.1/"

def init_db():
    #TODO: set up database, not just collections
    mongo = current_app.config["MONGO"]
    # clear existing data
    mongo.db.users.drop()
    mongo.db.miscInfo.drop()

    # create new collection and indices
    mongo.db.create_collection("users")
    mongo.db.users.create_index("id", unique=True)
    mongo.db.users.create_index("email", unique=True)
    print("Initialized user collection")
    mongo.db.create_collection("miscInfo")
    print("Adding nextCondition info...")
    mongo.db.miscInfo.insert_one({"nextCondition": 1})
    print("Initialized setup collection")
    print('Initialized the database.')
