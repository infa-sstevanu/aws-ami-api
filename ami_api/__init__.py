import os
import threading
from time import sleep
from .libs.aws import get_all_aws_ami
from flask import Flask
from logging.config import dictConfig

delay_time = 180 # 3 minutes
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

def aws_ami():
    while True:
        get_all_aws_ami()
        sleep(delay_time)

# Start the threading to retrieve ami images
aws_cron = threading.Thread(target=aws_ami)
aws_cron.start()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import ami
    app.register_blueprint(ami.bp)

    return app
