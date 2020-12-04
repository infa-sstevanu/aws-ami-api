import os
import boto3
import functools
from botocore.config import Config
from flask import Blueprint, flash, g, redirect, request, session, url_for

bp = Blueprint('ami', __name__, url_prefix='/')

invalid_tags_msg = 'invalid_tags_filters'

@bp.route('/', methods=['GET'])
def index():
    return { "name":"ami-api", "description":"REST API to get an ami based on regions, products and/or services" }

@bp.route('/ami', methods=['GET'])
def get_ami():
    region = request.args.get('region','us-west-2')
    tags = request.args.get('tags','')

    filters = []
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
        print(filters)
    except Exception as e:
        pass

    aws_config = Config(region_name=region)
    client = boto3.client('ec2', config=aws_config)

    try:
        resp = client.describe_images(Owners=['self'], Filters=filters, DryRun=False)
        images = []

        for image in resp['Images']:
            images.append(image['ImageId'])

        return { "images_ids": images }

    except Exception as e:
        return { 'msg': invalid_tags_msg }

    return {}
