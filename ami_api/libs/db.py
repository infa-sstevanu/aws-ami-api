from tinydb import TinyDB, Query
from flask import current_app

def init_db():
    db = TinyDB('db.json')
    Status = Query()
    if not db.search(Status.aws_conn_status >= 0):
        db.insert({ 'aws_conn_status': 1 })
    if not db.search(Status.gcp_conn_status >= 0):
        db.insert({ 'gcp_conn_status': 1 })
    if not db.search(Status.azure_conn_status >= 0):
        db.insert({ 'azure_conn_status': 1 })
    return [db, Status]
