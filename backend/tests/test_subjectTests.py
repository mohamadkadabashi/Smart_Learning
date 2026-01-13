from models.subject_tests import SubjectTestQuestionType

token_header = {"Content-Type": "application/x-www-form-urlencoded"}

def test_read_subjectTests(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create subjects
    r2 = client.post("/subjects/", headers=headers, json={
        "name": "DBS",
        "user_id": 1
    })
    r3 = client.post("/subjects/", headers=headers, json={
        "name": "DBS2",
        "user_id": 1
    })

    assert r2.status_code == 201
    assert r3.status_code == 201

    # create subjectTests
    questionTyp_select = SubjectTestQuestionType.SINGLE_CHOICE.value
    r4 = client.post(f"/subjecttests/TEST/{questionTyp_select}", headers=headers, json={
        "name": "Aggregatsfunktionen",
        "subject_id": 1,
        "question_count": 8
    })
    questionTyp_select = SubjectTestQuestionType.MULTIPLE_CHOICE.value
    r5 = client.post(f"/subjecttests/TEST/{questionTyp_select}", headers=headers, json={
        "name": "Joins",
        "subject_id": 2,
        "question_count": 42
    })

    assert r4.status_code == 201
    assert r5.status_code == 201

    # read subjects
    response = client.get("/subjecttests/", headers=headers)
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    names = [u["name"] for u in data]
    assert "Aggregatsfunktionen" in names
    assert "Joins" in names

    subject_ids = [u["subject_id"] for u in data]
    assert 1 in subject_ids
    assert 2 in subject_ids

    question_types = [u["question_type"] for u in data]
    assert SubjectTestQuestionType.SINGLE_CHOICE in question_types
    assert SubjectTestQuestionType.MULTIPLE_CHOICE in question_types

    question_counts = [u["question_count"] for u in data]
    assert 8 in question_counts
    assert 42 in question_counts

    # check that each subject has id, created_at, updated_at
    for subject in data:
        assert "id" in subject
        assert "created_at" in subject
        assert "updated_at" in subject

def test_read_subjectTests_bySubject(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create subject
    r2 = client.post("/subjects/", headers=headers, json={
        "name": "DBS",
        "user_id": 1
    })

    assert r2.status_code == 201

    # create subjectTests
    questionTyp_select = SubjectTestQuestionType.SINGLE_CHOICE.value
    r4 = client.post(f"/subjecttests/TEST/{questionTyp_select}", headers=headers, json={
        "name": "Aggregatsfunktionen",
        "subject_id": 1,
        "question_count": 8
    })
    questionTyp_select = SubjectTestQuestionType.MULTIPLE_CHOICE.value
    r5 = client.post(f"/subjecttests/TEST/{questionTyp_select}", headers=headers, json={
        "name": "Joins",
        "subject_id": 1,
        "question_count": 42
    })

    assert r4.status_code == 201
    assert r5.status_code == 201

    # read subject
    subject = r2.json()
    subject_id = subject["id"]
    response = client.get(f"/subjecttests/bySubject/{subject_id}", headers=headers)
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    names = [u["name"] for u in data]
    assert "Aggregatsfunktionen" in names
    assert "Joins" in names

    subject_ids = [u["subject_id"] for u in data]
    assert 1 in subject_ids

    question_types = [u["question_type"] for u in data]
    assert SubjectTestQuestionType.SINGLE_CHOICE in question_types
    assert SubjectTestQuestionType.MULTIPLE_CHOICE in question_types

    question_counts = [u["question_count"] for u in data]
    assert 8 in question_counts
    assert 42 in question_counts

    # check that each subject has id, created_at, updated_at
    for subject in data:
        assert "id" in subject
        assert "created_at" in subject
        assert "updated_at" in subject

def test_read_subjectTests_bySubject_noexistent_subject_id(client):
    # create user for login
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    subject_id = 42
    response = client.get(f"/subjecttests/bySubject/{subject_id}", headers=headers)
    assert response.status_code == 404

def test_read_subject(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create subject
    r2 = client.post("/subjects/", headers=headers, json={
        "name": "DBS",
        "user_id": 1
    })

    assert r2.status_code == 201

    # create subjectTests
    questionTyp_select = SubjectTestQuestionType.SINGLE_CHOICE.value
    r3 = client.post(f"/subjecttests/TEST/{questionTyp_select}", headers=headers, json={
        "name": "Aggregatsfunktionen",
        "subject_id": 1,
        "question_count": 8
    })

    assert r3.status_code == 201

    # read subjectTest
    subjectTest_id = r3.json()["id"]
    response = client.get(f"/subjecttests/{subjectTest_id}", headers=headers)

    assert response.status_code == 200

    subjectTest = response.json()
    assert subjectTest["id"] == subjectTest_id
    assert subjectTest["name"] == "Aggregatsfunktionen"
    assert subjectTest["question_type"] == SubjectTestQuestionType.SINGLE_CHOICE
    assert subjectTest["question_count"] == 8
    assert subjectTest["subject_id"] == r2.json()["id"]
    assert "created_at" in subjectTest
    assert "updated_at" in subjectTest

def test_read_subjectTest_noexistent_id(client):
    # create user for login
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    subjectTest_id = 42
    response = client.get(f"/subjecttests/{subjectTest_id}", headers=headers)
    assert response.status_code == 404

def test_update_subjectTest(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create subject
    r2 = client.post("/subjects/", headers=headers, json={
        "name": "DBS",
        "user_id": 1
    })

    assert r2.status_code == 201

    # create subjectTests
    questionTyp_select = SubjectTestQuestionType.SINGLE_CHOICE.value
    r3 = client.post(f"/subjecttests/TEST/{questionTyp_select}", headers=headers, json={
        "name": "Aggregatsfunktionen",
        "subject_id": 1,
        "question_count": 8
    })

    assert r3.status_code == 201

    # update subjectTest
    subjectTest_id = r3.json()["id"]
    r4 = client.patch(f"/subjecttests/{subjectTest_id}", headers=headers, json={
        "name": "Joins"
    })

    assert r4.status_code == 200

    assert r4.json()["name"] == "Joins"

def test_update_subjectTest_noexistent_id(client):
    # create user for login
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # update subject
    subjectTest_id = 42
    r3 = client.patch(f"/subjecttests/{subjectTest_id}", headers=headers, json={
        "name": "Joins"
    })
    assert r3.status_code == 404

def test_update_subjectTest_name_subeject_id_combo_already_exists(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create subject
    r2 = client.post("/subjects/", headers=headers, json={
        "name": "DBS",
        "user_id": 1
    })

    assert r2.status_code == 201

    # create subjectTests
    questionTyp_select = SubjectTestQuestionType.SINGLE_CHOICE.value
    r3 = client.post(f"/subjecttests/TEST/{questionTyp_select}", headers=headers, json={
        "name": "Aggregatsfunktionen",
        "subject_id": 1,
        "question_count": 8
    })
    questionTyp_select = SubjectTestQuestionType.MULTIPLE_CHOICE.value
    r4 = client.post(f"/subjecttests/TEST/{questionTyp_select}", headers=headers, json={
        "name": "Joins",
        "subject_id": 1,
        "question_count": 42
    })

    assert r3.status_code == 201
    assert r4.status_code == 201

    # update subject
    subjectTest_id = r3.json()["id"]
    r5 = client.patch(f"/subjecttests/{subjectTest_id}", headers=headers, json={
        "name": "Joins"
    })

    assert r5.status_code == 409

def test_delete_subjectTest(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create subject
    r2 = client.post("/subjects/", headers=headers, json={
        "name": "DBS",
        "user_id": 1
    })

    assert r2.status_code == 201

    # create subjectTests
    questionTyp_select = SubjectTestQuestionType.SINGLE_CHOICE.value
    r3 = client.post(f"/subjecttests/TEST/{questionTyp_select}", headers=headers, json={
        "name": "Aggregatsfunktionen",
        "subject_id": 1,
        "question_count": 8
    })

    assert r3.status_code == 201

    # delete subject
    subjectTest_id = r3.json()["id"]
    r4 = client.delete(f"/subjecttests/{subjectTest_id}", headers=headers)

    assert r4.status_code == 204

def test_delete_subjectTest_noexistent_id(client):
    # create user for login
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # login as user to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # delete subject
    subjectTest_id = 42
    r1 = client.delete(f"/subjecttests/{subjectTest_id}", headers=headers)

    assert r1.status_code == 404
