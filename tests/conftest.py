
import pytest
import json
from app import create_app, db

@pytest.fixture()
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True  

    with app.app_context():
        db.create_all() 
        yield app
        db.drop_all()  

@pytest.fixture()
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """
    Generate a JWT token for testing by registering and logging in a user.
    """
    register_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post(
        "/auth/register", 
        data=json.dumps(register_data),
        content_type="application/json",
    )
    assert response.status_code == 201, "User registration failed"


    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post(
        "/auth/login",  
        data=json.dumps(login_data),
        content_type="application/json",
    )
    assert response.status_code == 200, "User login failed"

    response_data = response.json
    token = response_data.get("access_token")
    assert token, "Access token not found in login response"

    return {"Authorization": f"Bearer {token}"}