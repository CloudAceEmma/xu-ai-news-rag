import json

def test_register_success(client, init_database):
    """Test user registration success."""
    response = client.post('/api/auth/register', json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert response.get_json()['msg'] == "User created successfully"

def test_register_duplicate_username(client, init_database):
    """Test registering with a username that already exists."""
    client.post('/api/auth/register', json={
        "username": "testuser",
        "password": "testpassword"
    })
    response = client.post('/api/auth/register', json={
        "username": "testuser",
        "password": "anotherpassword"
    })
    assert response.status_code == 409
    assert response.get_json()['msg'] == "Username already exists"

def test_register_missing_fields(client, init_database):
    """Test registration with missing fields."""
    response = client.post('/api/auth/register', json={
        "username": "testuser"
    })
    assert response.status_code == 400
    assert response.get_json()['msg'] == "Username and password are required"

def test_login_success(client, init_database):
    """Test user login success."""
    # First, register a user
    client.post('/api/auth/register', json={
        "username": "testuser",
        "password": "testpassword"
    })
    # Then, try to log in
    response = client.post('/api/auth/login', json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_wrong_password(client, init_database):
    """Test login with an incorrect password."""
    client.post('/api/auth/register', json={
        "username": "testuser",
        "password": "testpassword"
    })
    response = client.post('/api/auth/login', json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.get_json()['msg'] == "Bad username or password"

def test_login_nonexistent_user(client, init_database):
    """Test login with a username that does not exist."""
    response = client.post('/api/auth/login', json={
        "username": "nonexistentuser",
        "password": "password"
    })
    assert response.status_code == 401
    assert response.get_json()['msg'] == "Bad username or password"
