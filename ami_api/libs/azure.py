from tinydb import Query
from .db import init_db
from .error_msg import cannot_connect_cloud
from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
import os

db, Status = init_db()
Images = Query()
azure_table = db.table('azure')

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
    print(e)

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
            target_regions = [region.name for region in gallery_image_properties.publishing_profile.target_regions]
            source_image = gallery_image_properties.storage_profile.source
            print(target_regions, source_image)

    except Exception as e:
        print(e)
