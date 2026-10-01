def test_home(client):
    response = client.get("/")

    assert response.status_code == 200


def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_login_user(client):
    client.post(
        "/users/register",
        json={
            "username": "loginuser",
            "password": "password123"
        }
    )

    response = client.post(
        "/users/login",
        data={
            "username": "loginuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/users/register",
        json={
            "username": "wrongpassuser",
            "password": "password123"
        }
    )

    response = client.post(
        "/users/login",
        data={
            "username": "wrongpassuser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401