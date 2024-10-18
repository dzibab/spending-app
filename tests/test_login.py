
def test_login_success(client, create_user):
    response = client.post(
        "/login",
        json={"username": create_user.username, "password": "password123"},
    )
    print(response.json())  # Add this line to print the response content
    assert response.status_code == 200
    assert "message" in response.json()
