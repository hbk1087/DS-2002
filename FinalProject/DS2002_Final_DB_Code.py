#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 17:56:52 2022

@author: neilhansaria
"""

import pandas as pd
import json
from pymongo import MongoClient



shows = pd.read_csv("Best Shows Netflix.csv", usecols = ["TITLE", "RELEASE_YEAR", "SCORE", "DURATION", "NUMBER_OF_SEASONS", "MAIN_PRODUCTION"])
movies = pd.read_csv("Best Movies Netflix.csv", usecols = ["TITLE", "RELEASE_YEAR", "SCORE", "DURATION", "MAIN_GENRE", "MAIN_PRODUCTION"])

shows["TYPE"] = "Show"
movies["TYPE"] = "Movie"

final = pd.concat([shows, movies])


# Import to mongoDB

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://hbk10871:DSISFUN@cluster0.4rxgntk.mongodb.net/test"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['DS2002Project2Final1']


dbname = get_database()
collection_name = dbname["Netflix"]

#df.to_dict(orient='records')

collection_name.insert_many(final.to_dict(orient='records'))







