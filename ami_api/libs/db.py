from tinydb import TinyDB, Query
import click
from flask import current_app

def init_db():
    db = TinyDB('db.json')
    return db
