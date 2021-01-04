from flask import current_app

def request_cannot_empty(str):
    err_msg = "`{}` param cannot be empty!".format(str)
    current_app.logger.info(err_msg)
    return { "error_msg": err_msg }

def cannot_connect_cloud(provider):
    err_msg = "Cannot connect to cloud provider {}".format(provider)
    return { "error_msg": err_msg }

def limit_param_must_be_integer():
    err_msg = "limit param must be integer"
    return { "error_msg": err_msg }