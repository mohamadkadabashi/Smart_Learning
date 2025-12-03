# tests/test_users.py
def test_create_user(client):
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret123"
    })

    assert response.status_code == 201
    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

