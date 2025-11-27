import pytest
from unittest.mock import patch, MagicMock
from app import app
import jwt
from datetime import datetime, timedelta, timezone


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
    with patch("app.ADMIN_USER", "admin"):
        with patch("app.ADMIN_PW", "123"):
            response = client.post("/login", json={
                "username": "wrong",
                "password": "nope"
            })

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials"


def test_profile_missing_token(client):
    response = client.get("/profile")
    assert response.status_code == 401
    assert response.get_json()["error"] == "Missing token"


def test_profile_invalid_jwt(client):
    with patch("app.BACKEND_KEY", "secret-key"):
        response = client.get("/profile", headers={
            "Authorization": "Bearer invalid.jwt.token"
        })

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid token"


def test_profile_session_not_found(client):
    token = jwt.encode({"user": "admin"}, "secret-key", algorithm="HS256")

    with patch("app.BACKEND_KEY", "secret-key"):
        with patch("app.SQLServices.get_session_by_token",
                   MagicMock(return_value=(None, None, None, None))):

            response = client.get("/profile", headers={
                "Authorization": f"Bearer {token}"
            })

    assert response.status_code == 401
    assert response.get_json()["error"] == "Missing token or session not found"


def test_profile_session_username_mismatch(client):
    token = jwt.encode({"user": "admin"}, "secret-key", algorithm="HS256")

    with patch("app.BACKEND_KEY", "secret-key"):
        with patch("app.SQLServices.get_session_by_token",
                   MagicMock(return_value=("sess1", "bob", datetime.now(timezone.utc), datetime.now(timezone.utc) + timedelta(hours=1)))):

            response = client.get("/profile", headers={
                "Authorization": f"Bearer {token}"
            })

    assert response.status_code == 401
    assert response.get_json()["error"] == "Missing token or session not found"


def test_profile_session_expired(client):
    token = jwt.encode({"user": "admin"}, "secret-key", algorithm="HS256")

    expired = datetime.now(timezone.utc) - timedelta(hours=1)

    with patch("app.BACKEND_KEY", "secret-key"):
        with patch("app.SQLServices.get_session_by_token",
                   MagicMock(return_value=("sess1", "admin", datetime.now(timezone.utc), expired))):

            response = client.get("/profile", headers={
                "Authorization": f"Bearer {token}"
            })

    assert response.status_code == 401
    assert response.get_json()["error"] == "Session expired"


def test_profile_success(client):
    created = datetime.now(timezone.utc) - timedelta(minutes=10)
    expires = datetime.now(timezone.utc) + timedelta(hours=1)
    token = jwt.encode({"user": "admin"}, "secret-key", algorithm="HS256")

    with patch("app.BACKEND_KEY", "secret-key"):
        with patch("app.gethostname", return_value="host123"):
            with patch("app.SQLServices.get_session_by_token",
                       MagicMock(return_value=("sess1", "admin", created, expires))):

                response = client.get("/profile", headers={
                    "Authorization": f"Bearer {token}"
                })

    data = response.get_json()
    assert response.status_code == 200
    assert data["username"] == "admin"
    assert data["hostname"] == "host123"
    assert data["session_id"] == "sess1"
    assert "login_time" in data
    assert data["message"] == "Welcome admin!"
