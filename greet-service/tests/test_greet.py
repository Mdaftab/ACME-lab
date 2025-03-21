import json
import pytest
from greet.greet import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert data['status'] == 'healthy'

def test_initial_greeting(client):
    """Test the initial greeting without a user set."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, unknown stranger!' in response.data 