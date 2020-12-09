import os
import threading
from .libs.aws import get_all_aws_ami
from time import sleep
from flask import Flask, g
from logging.config import dictConfig

delay_time = 180 # 3 minutes
    
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Start the threading to retrieve ami images
    with app.app_context():
        def aws_ami():
            while True:
                get_all_aws_ami(app.logger)
                sleep(delay_time)
        aws_cron = threading.Thread(target=aws_ami)
        aws_cron.start()

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
