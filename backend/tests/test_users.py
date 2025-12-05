def test_create_user(client):
    user = {
         "username": "testuser",
        "email": "test@example.com",
        "password": "secret123"
    }
    response = client.post("/users/", json=user)

    assert response.status_code == 201
    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_user_no_username(client):
    user = {
        "username": "",
        "email": "test@example.com",
        "password": "secret123"
    }
    response = client.post("/users/", json=user)

    assert response.status_code == 422

def test_create_user_without_password(client):
    # create two users first
    user = {
        "username": "alice",
        "email": "alice@example.de"
    }
    response = client.post("/users/", json=user)

    assert response.status_code == 422  # Unprocessable Entity due to missing password

def test_create_two_user_with_same_username(client):
    # create two users first
    user1 = {
        "username": "bob",
        "email": "alice@example.com",
        "password": "password123"
    }
    user2 = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "password123"
    }

    # create users
    response1 = client.post("/users/", json=user1)
    response2 = client.post("/users/", json=user2)

    assert response1.status_code == 201
    assert response2.status_code == 400  # Bad Request due to duplicate username
    assert response2.json()["detail"] == "Username already taken"

def test_get_users(client):
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

def test_get_user(client):
    user = {
        "username": "charlie",
        "email": "test@test.de",
        "password": "password123"
    }
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    created = response.json()
    user_id = created["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200

    user = response.json()
    assert user["id"] == user_id
    assert user["username"] == "charlie"
    assert user["email"] == "test@test.de"
    assert "created_at" in user
    assert "updated_at" in user

def test_get_nonexistent_user(client):
    # get user with an ID that does not exist
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_update_user(client):
    # create a user first
    user = {
        "username": "dave",
        "email": "test@test.de",
        "password": "password123"
    }
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    # get the created user's ID
    created = response.json()
    user_id = created["id"]

    # update the user
    update_data = {
        "username": "dave_updated",
        "email": "test@test.de",
        "password": "password123"
    }
    response = client.patch(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200


def test_update_user_with_empty_username(client):
    # create a user first
    user = {
        "username": "dave",
        "email": "test@test.de",
        "password": "password123"
    }
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    # get the created user's ID
    created = response.json()
    user_id = created["id"]

    # update the user
    update_data = {
        "username": "",
        "email": "test@test.de",
        "password": "password123"
    }
    response = client.patch(f"/users/{user_id}", json=update_data)
    assert response.status_code == 422

