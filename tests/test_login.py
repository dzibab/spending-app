
def test_login_success(client, create_user):
    response = client.post(
        "/login",
        json={"username": create_user.username, "password": "password123"},
    )  # Use plain password
    assert response.status_code == 200
    assert "message" in response.json()  # Update to check for "message" instead of "access_token"
