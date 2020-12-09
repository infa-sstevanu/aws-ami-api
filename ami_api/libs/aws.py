import boto3
from botocore.config import Config
from flask import current_app
from tinydb import Query
from .db import init_db

db = init_db()
Images = Query()
aws_table = db.table('aws')

def filter_image(image, release, platform=None, types=None):
    for tag in image['Tags']:
        if tag['Key'] == 'RELEASE' and release in tag['Value']:
            return True
    return False

def get_all_aws_ami():
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
            for image in resp['Images']:
                ami_id = image['ImageId']
                ami_name = image['Name']
                ami_type = ami_name.split('-')[1].upper()
                print(ami_id, ami_name)
                ami_details = { 
                    "type": ami_type, 
                    "region": region,
                    "ami_id": ami_id, 
                    "ami_name": ami_name }
                if not aws_table.search(Images.ami_id == ami_id):
                    aws_table.insert(ami_details)

        except Exception as e:
            current_app.logger.info(e)

def get_ami_aws(release, platform=None, types=None):
    aws_images = aws_table.search(Images.type == 'INFA')
    return { 'images': aws_images }