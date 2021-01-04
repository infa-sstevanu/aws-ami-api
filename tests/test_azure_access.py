import os

from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient

def test_azure_access():
    credential = AzureCliCredential()

    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

    compute_client = ComputeManagementClient(credential, subscription_id)

    resource_group_name = "CloudTrust-UBI"
    gallery_name = "ctimagegallery"

    gallery_images = compute_client.gallery_images.list_by_gallery(resource_group_name, gallery_name)

    assert type(gallery_images.next().id) == str