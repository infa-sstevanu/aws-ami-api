from flask import current_app
from tinydb import Query
from .db import init_db
from .error_msg import cannot_connect_cloud, limit_param_must_be_integer
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
            regions = image['storageLocations']
            family = image['family']
            try:
                image_type, os = family.split('-')
            except Exception as e:
                log.info(e)

            name = image['name']
            creation_date = image['creationTimestamp']

            log.info("{}, {}".format(ami_id, name))

            ami_details = {
                "id": ami_id,
                "regions": regions,
                "name": name,
                "type": image_type,
                "os": os,
                "family": family,
                "creation_date": creation_date,
                "project": project
            }

            if not gcp_table.search(Images.id == ami_id):
                gcp_table.insert(ami_details)
            else:
                gcp_table.update(ami_details, Images.id == ami_id)

        request = service.images().list_next(previous_request=request, previous_response=response)
    

def get_ami_gcp(release, platform, types=None, limit=None):
    gcp_images = gcp_table.all()
    gcp_images = sorted(gcp_images, key=lambda x: x['creation_date'], reverse=True)
    result = gcp_images
    
    if db.search(Status.gcp_conn_status == 0):
        return cannot_connect_cloud("gcp")

    try:
        if limit:
            result = result[:int(limit)]
    except ValueError as e:
        current_app.logger.info(e)
        return limit_param_must_be_integer()

    return { 'ami_images': result }