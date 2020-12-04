import os
import boto3
import functools
from botocore.config import Config
from flask import Blueprint, flash, g, redirect, request, session, url_for
from flask import current_app

bp = Blueprint('ami', __name__, url_prefix='/')

invalid_tags_msg = 'invalid filter tags and/or limit value is not integer'

@bp.route('/', methods=['GET'])
def index():
    return { "name":"ami-api", "description":"REST API to get an ami based on regions, products and/or services" }

@bp.route('/ami', methods=['GET'])
def get_ami():
    current_app.logger.info(request.args)

    region = request.args.get('region','us-west-2')
    tags = request.args.get('tags','')
    latest = request.args.get('latest', False)
    limit = request.args.get('limit', 0)

    filters = []
    ami_images = []

    if tags:
        try:
            tags = tags.split(';')
            for tag in tags:
                key_value = tag.split(':')
                if len(key_value) == 2:
                    key = 'tag:{}'.format(key_value[0].upper())
                    values = [key_value[1]]
                    filters.append({ 'Name':key, 'Values':values })
                else:
                    return { 'msg': invalid_tags_msg }
        except Exception as e:
            current_app.logger.info(e)

    try:
        limit = int(limit)
    except ValueError as ve:
        current_app.logger.info(ve)
        return { 'msg': invalid_tags_msg }

    aws_config = Config(region_name=region)
    client = boto3.client('ec2', config=aws_config)

    try:
        resp = client.describe_images(Owners=['self'], Filters=filters, DryRun=False)

        for image in resp['Images']:
            ami_images.append(image)

        images = []
        if latest and latest != '0':
            ami_images = sorted(ami_images, key=lambda image: image['CreationDate'], reverse=True)
            for image in ami_images:
                images.append('{} {}'.format(image['ImageId'], image['CreationDate']))

        if limit:
            images = images[:limit]

        return { "images_ids": images }

    except Exception as e:
        current_app.logger.info(e)
        return { 'msg': invalid_tags_msg }

    return {}
