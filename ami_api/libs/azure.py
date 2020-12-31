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
images = compute_client.images.list()
try:
    while images:
        print(images.next())
except Exception as e:
    print(e)
