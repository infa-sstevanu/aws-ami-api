import os
import threading
from time import sleep
from flask import Flask, g
from logging.config import dictConfig

delay_time = 180 # 3 minutes

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    def aws_ami():
        while True:
            from .libs.aws import get_all_aws_ami
            get_all_aws_ami(app.logger)
            sleep(delay_time)
    
    # Threading for the aws ami
    aws_cron = threading.Thread(target=aws_ami)
    aws_cron.start()

    def gcp_ami():
        while True:
            from .libs.gcp import get_all_gcp_ami
            get_all_gcp_ami(app.logger)
            sleep(delay_time)
    
    # Threading for the gcp ami
    gcp_cron = threading.Thread(target=gcp_ami)
    gcp_cron.start()

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
