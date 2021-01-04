import os
import tempfile

import pytest

from ami_api import create_app

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
    })

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_hello(client):
    response = client.get('/health')
    assert response.status_code == 200


