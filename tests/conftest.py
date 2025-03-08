import pytest
import jwt
import datetime

from app import create_app, db

@pytest.fixture()
def app():
    app = create_app()
    
    with app.app_context():
        db.create_all()
    
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers():
    """Generate a fake JWT token for testing."""
    payload = {
        "user_id": 1,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1-hour expiry
    }
    token = jwt.encode(payload, "your_secret_key", algorithm="HS256")

    return {"Authorization": f"Bearer {token}"}
