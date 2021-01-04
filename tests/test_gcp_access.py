from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def test_gcp_access():
    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('compute', 'v1', credentials=credentials)

    project = 'infa-iicsqa-productionimages'

    request = service.images().list(project=project)

    response = request.execute()

    assert type(response) == dict

