def test_create_subject(client):
    # create user for subject
    r1 = client.post("/users/", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subject
    r2 = client.post("/subjects/", json={
        "name": "testSubject",
        "user_id": 1
    })

    assert r2.status_code == 201
    data = r2.json()

    assert data["name"] == "testSubject"
    assert data["user_id"] == 1
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_read_subjects(client):
    # create user for subject
    r1 = client.post("/users/", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subjects
    r2 = client.post("/subjects/", json={
        "name": "DBS",
        "user_id": 1
    })
    r3 = client.post("/subjects/", json={
        "name": "DBS2",
        "user_id": 1
    })

    assert r2.status_code == 201
    assert r3.status_code == 201

    # read subjects
    response = client.get("/subjects/")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    names = [u["name"] for u in data]

    assert "DBS" in names
    assert "DBS2" in names

    # check that each subject has id, created_at, updated_at
    for subject in data:
        assert "id" in subject
        assert "created_at" in subject
        assert "updated_at" in subject
