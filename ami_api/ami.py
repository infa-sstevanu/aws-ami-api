import os
import functools
from botocore.config import Config
from flask import Blueprint, flash, g, request
from flask import current_app
from .libs.error_msg import request_cannot_empty
from .libs.aws import get_ami_aws

bp = Blueprint('ami', __name__, url_prefix='/')

cloud_session_expired = 'Cloud Session has expired'

@bp.route('/', methods=['GET'])
def index():
    return { "name":"ami_api", "description":"REST API to get an ami based on regions, products and/or services" }

@bp.route('/health', methods=['GET'])
def health():
    return { "status": "healthy" }

@bp.route('/ami', methods=['GET'])
def get_ami():
    current_app.logger.info(request.args)

    provider = request.args.get('provider', '')
    release = request.args.get('release', '')
    platform = request.args.get('os', '')
    types = request.args.get('type', '')
    limit = request.args.get('limit', 0)

    if not provider:
        return request_cannot_empty('provider')
    elif not release:
        return request_cannot_empty('release')
    elif not platform:
        return request_cannot_empty('os')

    if provider.lower() == 'aws':
        return get_ami_aws(release, platform, types, limit)
    else:
        return { "err_msg": "Provider '{}' is not available".format(provider) }
