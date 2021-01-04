import boto3

from botocore.config import Config

aws_config = Config(region_name='us-west-2')
client = boto3.client('ec2', config=aws_config)

def test_aws_access():
    resp = client.describe_images(Owners=['self'], Filters=[], DryRun=False)
    assert type(resp) == dict