import pytest
from pymongo import MongoClient

from database.conect import accidents_db
from repository.csv_repository import init_accidents


@pytest.fixture(scope="function")
def mongodb_client():
   client = MongoClient('mongodb://localhost:27017')
   yield client
   client.close()


@pytest.fixture(scope="function")
def accidents_db_test(mongodb_client):
   db_name = 'accidents_db_test'
   db = mongodb_client[db_name]
   yield db
   mongodb_client.drop_database(db_name)


@pytest.fixture(scope="function")
def init_test_data(accidents_db_test):
   if accidents_db['drivers'].count_documents({}) == 0:
       init_accidents()


   for collection_name in accidents_db.list_collection_names():
       accidents_db_test[collection_name].drop()
       accidents_db_test[collection_name].insert_many(accidents_db[collection_name].find())


   yield accidents_db_test


   # Clean up test data after each test
   for collection_name in accidents_db_test.list_collection_names():
       accidents_db_test[collection_name].drop()