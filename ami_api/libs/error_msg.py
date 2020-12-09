from flask import current_app

def request_cannot_empty(str):
    err_msg = "{} cannot be empty!".format(str)
    current_app.logger.info(err_msg)
    return { 'error_msg': err_msg }