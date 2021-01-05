from flask import current_app
from tinydb import Query
from .db import init_db
from .error_msg import cannot_connect_cloud, limit_param_must_be_integer
from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
import re
import os

db, Status = init_db()
Images = Query()
azure_table = db.table('azure')

def refine_query_result(azure_image, release, image_os, types=None):
    release = re.search(r'[0-9]+', release).group()
    if release.lower() not in azure_image['release'].lower():
        return False
    
    operating_systems = [
        ['centos'],
        ['redhat', 'rhel']
    ]

    image_os = re.search(r'[a-z]+', image_os).group()
    azure_image_os = re.search(r'[a-z]+', azure_image['os']).group()

    for operating_system in operating_systems:
        if image_os in operating_system and azure_image_os not in operating_system:
            return False
            
    if types:
        if types not in azure_image['type']:
            return False
    return True

def get_all_azure_ami(log):
    credential = AzureCliCredential()

    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

    compute_client = ComputeManagementClient(credential, subscription_id)

    resource_group_name = "CloudTrust-UBI"
    gallery_name = "ctimagegallery"

    gallery_images = compute_client.gallery_images.list_by_gallery(resource_group_name, gallery_name)
    gallery_image_names = []

    try:
        while gallery_images:
            gallery_image_name = gallery_images.next().id.split('/')[::-1][0]
            gallery_image_names.append(gallery_image_name)
    except Exception as e:
        log.info(e)

    for gallery_image_name in gallery_image_names:
        gallery_image_versions = compute_client.gallery_image_versions.list_by_gallery_image(
            resource_group_name, 
            gallery_name, 
            gallery_image_name
        )
        try:
            while gallery_image_versions:
                gallery_image_version_name = gallery_image_versions.next().name
                gallery_image_properties = compute_client.gallery_image_versions.get(
                    resource_group_name,
                    gallery_name,
                    gallery_image_name,
                    gallery_image_version_name
                )
                regions = [region.name for region in gallery_image_properties.publishing_profile.target_regions]
                image_name = gallery_image_properties.storage_profile.source.id.split('/')[::-1][0].lower()
                image_detail = image_name.split('-')

                if len(image_detail) == 4:
                    image_type = image_detail[1].lower()
                    image_os = image_detail[2]
                else:
                    image_type = image_detail[0].lower()
                    if "centos" in image_name:
                        image_os = "centos"
                    elif "redhat" in image_name or "rhel" in image_name: 
                        image_os = "rhel"
                    else:
                        image_os = "unknown"

                release = gallery_image_properties.name
                gallery_link = gallery_image_properties.id
                published_date = gallery_image_properties.publishing_profile.published_date
                published_date = published_date.strftime('%Y-%m-%dT%H:%M:%S.%f-%z')
                
                ami_details = {
                    "published_date": published_date,
                    "regions": regions,
                    "release": release,
                    "name": image_name,
                    "type": image_type,
                    "os": image_os,
                    "gallery_link": gallery_link
                }

                if not azure_table.search(Images.gallery_link == gallery_link):
                    azure_table.insert(ami_details)
                else:
                    azure_table.update(ami_details, Images.gallery_link == gallery_link)

        except Exception as e:
            log.info(e)

def get_ami_azure(release, platform, types=None, limit=None):
    azure_images = azure_table.all()
    azure_images = sorted(azure_images, key=lambda x: x['published_date'], reverse=True)
    result = []
    
    if db.search(Status.azure_conn_status == 0):
        return cannot_connect_cloud("azure")

    for azure_image in azure_images:
        if refine_query_result(azure_image, release, platform, types):
            result.append(azure_image)

    try:
        if limit:
            result = result[:int(limit)]
    except ValueError as e:
        current_app.logger.info(e)
        return limit_param_must_be_integer()

    return { 'ami_images': result }