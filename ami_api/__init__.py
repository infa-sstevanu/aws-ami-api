import os
import threading
from time import sleep
from flask import Flask

delay_time = 180 # 3 minutes

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    def aws_ami():
        while True:
            from .libs.aws import get_all_aws_ami
            get_all_aws_ami(app.logger)
            sleep(delay_time)
    
    aws_enabled = ""
    gcp_enabled =  ""
    azure_enabled = ""

    try:
        aws_enabled = os.environ['AWS_ENABLED']
        gcp_enabled = os.environ['GCP_ENABLED']
        azure_enabled = os.environ['AZURE_ENABLED']
    except Exception as e:
        print("Environment variable {} is not set".format(e))

    # Threading for the aws ami
    if aws_enabled.lower() == 'true':
        print("Start the aws thread")
        aws_cron = threading.Thread(target=aws_ami)
        aws_cron.start()

    def gcp_ami():
        while True:
            from .libs.gcp import get_all_gcp_ami
            get_all_gcp_ami(app.logger)
            sleep(delay_time)
    
    # Threading for the gcp ami
    if gcp_enabled.lower() == 'true':
        print("Start the gcp thread")
        gcp_cron = threading.Thread(target=gcp_ami)
        gcp_cron.start()

    def azure_ami():
        while True:
            from .libs.azure import get_all_azure_ami
            get_all_azure_ami(app.logger)
            sleep(delay_time)
    
    # Threading for the gcp ami
    if azure_enabled.lower() == 'true':
        print("Start the azure thread")
        azure_cron = threading.Thread(target=azure_ami)
        azure_cron.start()

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
