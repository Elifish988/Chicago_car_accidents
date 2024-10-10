from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
accidents_db = client['accidents_db']


accidents = accidents_db['accidents']
injuries = accidents_db['injuries']
