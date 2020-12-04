import os
import boto3
import functools
from botocore.config import Config
from flask import Blueprint, flash, g, redirect, request, session, url_for

bp = Blueprint('ami', __name__, url_prefix='/ami')

@bp.route('/', methods=['GET'])
def get_ami_id(region='us-west-2'):
    aws_config = Config(region_name=region)
    client = boto3.client('ec2', config=aws_config)

    try:
        resp = client.describe_images(Owners=['self'], DryRun=False)
        images = []

        for image in resp['Images']:
            images.append(image['ImageId'])
        
        return { "images_ids": images } 
        
    except Exception as e:
        raise e

    return {}
