import functools
from flask import Blueprint, flash, g, redirect, request, session, url_for

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return { "name":"ami-api", "description":"REST API to get an ami-id based on regions, products and/or services" } 

