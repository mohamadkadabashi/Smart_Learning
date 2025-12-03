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
    assert "created_at" in data
    assert "updated_at" in data


def test_read_users(client):
    # create two users first
    user1 = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    }
    user2 = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "password123"
    }

    # create users
    r1 = client.post("/users/", json=user1)
    r2 = client.post("/users/", json=user2)

    assert r1.status_code == 201
    assert r2.status_code == 201

    # read users
    response = client.get("/users/")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    usernames = [u["username"] for u in data]
    emails = [u["email"] for u in data]

    assert "alice" in usernames
    assert "bob" in usernames
    assert "alice@example.com" in emails
    assert "bob@example.com" in emails

    # check that each user has id, created_at, updated_at
    for user in data:
        assert "id" in user
        assert "created_at" in user
        assert "updated_at" in user

def test_read_users(client):
    # Create two users first
    user1 = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    }
    user2 = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "password123"
    }
    # create users
    r1 = client.post("/users/", json=user1)
    r2 = client.post("/users/", json=user2)

    assert r1.status_code == 201
    assert r2.status_code == 201

    # Read users
    response = client.get("/users/")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    # check usernames and emails
    usernames = [u["username"] for u in data]
    emails = [u["email"] for u in data]

    assert "alice" in usernames
    assert "bob" in usernames
    assert "alice@example.com" in emails
    assert "bob@example.com" in emails

    # check that each user has id, created_at, updated_at
    for user in data:
        assert "id" in user
        assert "created_at" in user
        assert "updated_at" in user

