from tinydb import Query
from .db import init_db
from .error_msg import cannot_connect_cloud
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

db, Status = init_db()
Images = Query()
gcp_table = db.table('gcp')

def get_all_gcp_ami(log):
    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('compute', 'v1', credentials=credentials)

    project = 'infa-iicsqa-productionimages'

    request = service.images().list(project=project)

    while request is not None:
        response = request.execute()

        for image in response['items']:
            ami_id = image['id']
            locations = image['storageLocations']
            family = image['family']
            name = image['name']
            creation_date = image['creationTimestamp']

            log.info("{}, {}".format(ami_id, name))

            ami_details = {
                "id": ami_id,
                "locations": locations,
                "os": family,
                "name": name,
                "creation_date": creation_date,
                "project": project
            }
            if not gcp_table.search(Images.id == ami_id):
                gcp_table.insert(ami_details)

        request = service.images().list_next(previous_request=request, previous_response=response)
    


