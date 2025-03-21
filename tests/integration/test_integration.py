import json
import pytest
from greet.greet import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_set_and_get_name(client):
    """Test setting a name and retrieving it."""
    # First check initial state
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, unknown stranger!' in response.data
    
    # Set a name
    response = client.post('/', 
                          data=json.dumps({'name': 'Integration Test'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert b'Integration Test' in response.data
    
    # Check that the name is remembered
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, Integration Test!' in response.data 