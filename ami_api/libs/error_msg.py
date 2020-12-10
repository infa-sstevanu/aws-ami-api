from flask import current_app

def request_cannot_empty(str):
    err_msg = "`{}` param cannot be empty!".format(str)
    current_app.logger.info(err_msg)
    return { 'error_msg': err_msg }

def cloud_session_expired():
    err_msg = 'Cloud Session has expired'
    return { 'error_msg': err_msg }