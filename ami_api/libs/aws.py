import re
import boto3
from botocore.config import Config
from flask import current_app, g
from tinydb import Query
from .db import init_db

db = init_db()
Images = Query()
aws_table = db.table('aws')

def filter_ami_image(ami_image, release, platform, types=None):
    platform_list = ["CENTOS", "REDHAT", "RHEL"]

    release = release.upper()
    platform = platform.upper()
    types = types.upper() or None

    if release not in ami_image['release']:
        return False
    if types and types != ami_image['type']:
        return False
    if platform == ami_image['os']:
        return True   
    if platform=='RHEL' and re.match(r'[a-zA-Z]+', ami_image['os']).group() in platform_list:
        return True
    if re.match(r'[a-zA-Z]+', platform).group() in platform_list:
        if re.match(r'[a-zA-Z]+', ami_image['os']).group() not in platform_list:
            return False
        if re.match(r'[a-zA-Z]+', platform).group() not in ami_image['os']:
            return False
    return True

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
                    "ami_id": ami_id, 
                    "ami_name": ami_name,
                    "creation_date": ami_creation_date }
                
                log.info("{} {}".format(ami_id, ami_name))

                if not aws_table.search(Images.ami_id == ami_id):
                    aws_table.insert(ami_details)
        except Exception as e:
            log.info(e)

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

    return { 'images': result }