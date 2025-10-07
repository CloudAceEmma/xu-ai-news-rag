import pytest
from backend.app import create_app
from backend.models import db, User
from backend.config import Config

test_config = Config()
test_config.TESTING = True

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test module."""
    test_config = Config()
    test_config.TESTING = True
    test_config.JWT_SECRET_KEY = "test-secret-key"
    test_config.LLM_URL = "http://test-llm-url"
    test_config.EMBEDDING_URL = "http://test-embedding-url"
    test_config.RERANKING_URL = "http://test-reranking-url"
    app = create_app(test_config)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    """Clear all data for each test function."""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

@pytest.fixture(scope='function')
def auth_token(client, init_database):
    """Get an auth token for a test user."""
    # Register a test user
    register_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    client.post('/api/auth/register', json=register_data)

    # Login to get token
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post('/api/auth/login', json=login_data)
    return response.get_json()['access_token']
