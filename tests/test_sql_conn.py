import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
from back.sql_conn import SQLServices


@pytest.fixture
def mock_conn():
    """Returns a mock SQLAlchemy connection."""
    conn = MagicMock()
    return conn


@pytest.fixture
def mock_engine(mock_conn):
    """Patches SQLServices.__ENGINE to use our mock connection."""
    with patch("sql_conn.SQLServices._SQLServices__ENGINE") as eng:
        eng.connect.return_value.__enter__.return_value = mock_conn
        yield eng


def test_check_password(mock_conn, mock_engine):
    mock_conn.execute.return_value.scalar.return_value = True
    assert SQLServices.check_password("user", "pw") is True


def test_check_password_too_long(mock_engine):
    result = SQLServices.check_password("x"*51, "pw")
    assert result is False


def test_create_session(mock_conn, mock_engine):
    mock_conn.execute.return_value = None
    mock_conn.commit.return_value = None

    session_id = SQLServices.create_session(
        username="admin",
        token="abc",
        ip_address="127.0.0.1",
        user_agent="pytest"
    )

    assert isinstance(session_id, str)
    assert len(session_id) > 0
    assert mock_conn.execute.called
    assert mock_conn.commit.called


def test_validate_session_valid(mock_conn, mock_engine):
    now = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    mock_conn.execute.return_value.fetchone.return_value = ("admin", now)

    is_valid, username = SQLServices.validate_session("abc")

    assert is_valid is True
    assert username == "admin"


def test_validate_session_expired(mock_conn, mock_engine):
    expired = datetime.now(tz=timezone.utc) - timedelta(hours=1)
    mock_conn.execute.return_value.fetchone.return_value = ("admin", expired)

    is_valid, username = SQLServices.validate_session("abc")

    assert is_valid is False
    assert username is None


def test_validate_session_not_found(mock_conn, mock_engine):
    mock_conn.execute.return_value.fetchone.return_value = None

    is_valid, username = SQLServices.validate_session("abc")

    assert is_valid is False
    assert username is None
