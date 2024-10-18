

# Test for successful registration
def test_register_success(client):  # Use the existing client fixture
    response = client.post("/register", json={"username": "newuser", "password": "password123"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}


# Test for registration with duplicate username
def test_register_duplicate_username(client):  # Use the existing client fixture
    # First, register a user
    client.post("/register", json={"username": "duplicateuser", "password": "password123"})

    # Try to register the same user again
    response = client.post("/register", json={"username": "duplicateuser", "password": "newpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


# Test for registration with missing username
def test_register_missing_username(client):  # Use the existing client fixture
    response = client.post("/register", json={"password": "password123"})
    assert response.status_code == 422  # Unprocessable Entity
    assert "username" in response.json()["detail"][0]["loc"]


# Test for registration with missing password
def test_register_missing_password(client):  # Use the existing client fixture
    response = client.post("/register", json={"username": "missingpassworduser"})
    assert response.status_code == 422  # Unprocessable Entity
    assert "password" in response.json()["detail"][0]["loc"]
