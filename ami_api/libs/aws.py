import re
import boto3
from botocore.config import Config
from flask import current_app, g
from tinydb import Query
from .db import init_db
from .error_msg import cloud_session_expired

db = init_db()
Images = Query()
aws_table = db.table('aws')

platforms = {
    "rhel": ["rhel", "redhat"],
    "redhat": ["rhel", "redhat"],
    "centos": ["centos"]
}

def filter_ami_image(ami_image, release, platform, types=None):
    release = release.upper()
    platform = re.match(r'[a-zA-Z]+', platform.lower()).group()
    types = types.upper() or None

    if release not in ami_image['release']:
        return False
    if types and types != ami_image['type']:
        return False
    if platform == ami_image['os']:
        return True   
    
    ami_platform = ami_image['name'].split('-')[2]
    ami_platform = re.match(r'[a-zA-Z]+', ami_platform.lower()).group()
    if platform in platforms[ami_platform]:
        return True
    return False

def extract_aws_ami_tags(tags):
    release = ""
    platform = ""
    for tag in tags:
        if tag['Key'] == 'RELEASE':
            release = tag['Value']
        if tag['Key'] == 'OS':
            platform = tag['Value']
    result = [release, platform]
    return result

def get_all_aws_ami(log):
    regions = []

    aws_config = Config(region_name='us-west-2')
    ec2 = boto3.client('ec2', config=aws_config)
    resp = ec2.describe_regions()
    
    for region in resp['Regions']:
        regions.append(region['RegionName'])
    
    for region in regions:
        aws_config = Config(region_name=region)
        client = boto3.client('ec2', config=aws_config)

        try:
            resp = client.describe_images(Filters=[{ "Name":"tag-key", "Values":["RELEASE"] }], DryRun=False)
            for ami_image in resp['Images']:
                ami_id = ami_image['ImageId'] or ""
                ami_name = ami_image['Name'] or ""
                ami_creation_date = ami_image['CreationDate'] or ""
                ami_type = ami_name.split('-')[1].upper() or ""
                release, ami_platform = extract_aws_ami_tags(ami_image['Tags']) or ["", ""]
                ami_details = {
                    "release": release,
                    "type": ami_type, 
                    "region": region,
                    "os": ami_platform,
                    "id": ami_id, 
                    "name": ami_name,
                    "creation_date": ami_creation_date }
                
                log.info("{} {}".format(ami_id, ami_name))

                if not aws_table.search(Images.ami_id == ami_id):
                    aws_table.insert(ami_details)
        except Exception as e:
            log.info(e)
            return cloud_session_expired()

def get_ami_aws(release, platform, types=None, limit=None):
    aws_images = aws_table.all()
    aws_images = sorted(aws_images, key=lambda x: x['creation_date'], reverse=True)
    result = []

    for ami_image in aws_images:
        if filter_ami_image(ami_image, release, platform, types):
            result.append(ami_image)

    try:
        if limit:
            result = result[:int(limit)]
    except ValueError as e:
        current_app.logger.info(e)
        return { 'err_msg': 'limit value is not integer' }

    return { 'ami_images': result }