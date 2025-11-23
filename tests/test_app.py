import pytest
from unittest.mock import patch, MagicMock
from back.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_login_success(client):
    mock_create = MagicMock(return_value="fake-session-id")

    with patch("app.SQLServices.create_session", mock_create):
        with patch("app.ADMIN_USER", "admin"):
            with patch("app.ADMIN_PW", "123"):
                with patch("app.BACKEND_KEY", "secret-key"):
                    response = client.post("/login", json={
                        "username": "admin",
                        "password": "123"
                    })

    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert data["session_id"] == "fake-session-id"


def test_login_invalid_credentials(client):
    response = client.post("/login", json={
        "username": "wrong",
        "password": "nope"
    })

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials"


def test_profile_missing_session(client):
    response = client.get("/profile")
    assert response.status_code == 401
    assert response.get_json()["error"] == "Missing session"


def test_profile_valid_session(client):
    mock_validate = MagicMock(return_value=(True, "admin"))

    with patch("app.SQLServices.validate_session", mock_validate):
        response = client.get("/profile", headers={"X-Session-ID": "abc"})

    assert response.status_code == 200
    assert "Welcome admin" in response.get_json()["message"]


def test_profile_invalid_session(client):
    mock_validate = MagicMock(return_value=(False, None))

    with patch("app.SQLServices.validate_session", mock_validate):
        response = client.get("/profile", headers={"X-Session-ID": "abc"})

    assert response.status_code == 401
    assert response.get_json()["error"] == "Session expired or invalid"
