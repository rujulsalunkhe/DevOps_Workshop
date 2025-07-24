import pytest
import json
import tempfile
import os
from app import app
from app.models import init_db

@pytest.fixture
def client():
    # Create a temporary database for testing
    db_fd, app.config['DATABASE_PATH'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE_PATH'])

def test_welcome_endpoint(client):
    """Test the welcome endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'version' in data
    assert 'endpoints' in data

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'status' in data
    assert 'timestamp' in data
    assert 'services' in data

def test_users_get_endpoint(client):
    """Test getting all users"""
    response = client.get('/api/v1/users')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'users' in data
    assert 'count' in data
    assert isinstance(data['users'], list)

def test_users_post_endpoint(client):
    """Test creating a new user"""
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    
    response = client.post('/api/v1/users', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'user_id' in data

def test_users_post_invalid_data(client):
    """Test creating user with invalid data"""
    user_data = {
        'name': '',
        'email': 'invalid-email'
    }
    
    response = client.post('/api/v1/users',
                          data=json.dumps(user_data),
                          content_type='application/json')
    assert response.status_code == 400

def test_get_user_by_id(client):
    """Test getting user by ID"""
    # First create a user
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    
    create_response = client.post('/api/v1/users',
                                 data=json.dumps(user_data),
                                 content_type='application/json')
    user_id = json.loads(create_response.data)['user_id']
    
    # Then get the user
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'user' in data
    assert data['user']['name'] == 'Test User'

def test_get_nonexistent_user(client):
    """Test getting a user that doesn't exist"""
    response = client.get('/api/v1/users/999')
    assert response.status_code == 404

def test_info_endpoint(client):
    """Test the info endpoint"""
    response = client.get('/api/v1/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'application' in data
    assert 'system' in data
    assert 'features' in data

def test_docs_endpoint(client):
    """Test the API documentation endpoint"""
    response = client.get('/api/v1/docs')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'openapi' in data
    assert 'info' in data
    assert 'paths' in data

def test_404_handler(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
