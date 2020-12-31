import os
import functools
from botocore.config import Config
from flask import Blueprint, flash, g, request
from flask import current_app
from .libs.error_msg import request_cannot_empty
from .libs.aws import get_ami_aws
from .libs.gcp import get_ami_gcp
from .lib.azure import get_ami_azure
from prometheus_client import CollectorRegistry, Counter, generate_latest, multiprocess, Histogram

REQUEST_LATENCY = Histogram(__name__.replace('.', '_') + '_request_latency_seconds', 'Flask Request Latency')
REQUEST_COUNTER = Counter(__name__.replace('.', '_') + '_request_counter', 'Flask Request Counter', ['method', 'endpoint'])

bp = Blueprint('ami', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    REQUEST_COUNTER.labels('get', '/').inc()
    return { "name":"ami_api", "description":"REST API to get an ami based on regions, products and/or services" }

@bp.route('/health', methods=['GET'])
def health():
    REQUEST_COUNTER.labels('get', '/health').inc()
    return { "status": "healthy" }

@bp.route('/metrics', methods=['GET'])
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return generate_latest(registry), 200

@REQUEST_LATENCY.time()
@bp.route('/ami', methods=['GET'])
def get_ami():
    REQUEST_COUNTER.labels('get', '/ami').inc()
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
    elif provider.lower() == 'gcp':
        return get_ami_gcp(release, platform, types, limit)
    elif provider.lower() == 'azure':
        return get_ami_azure(release, platform, types, limit)
    else:
        return { "err_msg": "Provider '{}' is not available".format(provider) }
