def create_user_and_get_token(client, username):
    password = "password123"

    client.post(
        "/users/register",
        json={
            "username": username,
            "password": password
        }
    )

    response = client.post(
        "/users/login",
        data={
            "username": username,
            "password": password
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_create_task(client):
    headers = create_user_and_get_token(
        client,
        "createuser"
    )

    response = client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "completed": False,
            "priority": "high"
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn FastAPI"


def test_get_tasks(client):
    headers = create_user_and_get_token(
        client,
        "getuser"
    )

    client.post(
        "/tasks/",
        json={
            "title": "First task",
            "completed": False,
            "priority": "medium"
        },
        headers=headers
    )

    response = client.get(
        "/tasks/",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_task(client):
    headers = create_user_and_get_token(
        client,
        "updateuser"
    )

    create_response = client.post(
        "/tasks/",
        json={
            "title": "Old title",
            "completed": False,
            "priority": "low"
        },
        headers=headers
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "completed": True
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["completed"] is True


def test_delete_task(client):
    headers = create_user_and_get_token(
        client,
        "deleteuser"
    )

    create_response = client.post(
        "/tasks/",
        json={
            "title": "Delete me",
            "completed": False,
            "priority": "medium"
        },
        headers=headers
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers=headers
    )

    assert response.status_code == 200


def test_user_cannot_access_another_users_task(client):
    owner_headers = create_user_and_get_token(
        client,
        "owner"
    )

    other_headers = create_user_and_get_token(
        client,
        "other"
    )

    create_response = client.post(
        "/tasks/",
        json={
            "title": "Private task",
            "completed": False,
            "priority": "high"
        },
        headers=owner_headers
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers=other_headers
    )

    assert response.status_code == 404