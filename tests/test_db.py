from tinydb import TinyDB, Query
from os import path, remove

DB_NAME = 'test_db.json'

class DB:
    def __init__(self):
        self.db = TinyDB(DB_NAME)
        self.query = Query()
    
    def query_data(self, id):
        return self.db.search(self.query.id == id)
    
    def insert_data(self, data):
        self.db.insert(data)

    def update_data(self, id, data):
        self.db.update(data, self.query.id == id)

test_db = DB()

def test_can_create_db():
    assert path.exists(DB_NAME) == True

def test_can_insert_data():
    test_db.insert_data({'id':1, 'data': 'test_data'})
    assert type(test_db.query_data(1)) == list

def test_can_update_data():
    test_db.update_data(1, {'data': 'test_update_data'})
    result = test_db.query_data(1)
    assert result[0]['data'] == 'test_update_data'

def test_can_delete_db():
    remove(DB_NAME)
    assert path.exists(DB_NAME) == False