from sqlalchemy import text
from sqlalchemy.engine import create_engine, Engine
from os import getenv
from datetime import datetime, timedelta
from datetime import timezone
from uuid import uuid4
import time

# DB_URL: postgresql+psycopg2://USUARIO:SENHA@NOME_DO_CONTAINER:PORTA/BANCO
DB_URL: str | None = getenv("DB_URL")

UTC: timezone = timezone.utc

if not DB_URL:
    exit(1)

def create_db_engine_with_retry(db_url: str, max_retries: int = 30, retry_delay: int = 2) -> Engine:
    """Tenta conectar ao banco com retry"""
    for attempt in range(max_retries):
        try:
            engine = create_engine(db_url)
            # Testa a conexão
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"✓ Database connected successfully on attempt {attempt + 1}")
            return engine
        except Exception as e:
            print(f"✗ Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    raise Exception(f"Failed to connect to database after {max_retries} attempts")

class SQLServices:
    """
    Classe que fornece serviços de banco de dados. Não é instanciável e não pode
    ter subclasses.
    """

    __ENGINE: Engine = create_db_engine_with_retry(DB_URL)

    def __new__(cls):
        raise TypeError(f"Class SQLServices cannot not be instantiated")

    def __init_subclass__(cls):
        raise TypeError(f"Class SQLServices cannot not be inherited from")

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        """
        Checa se a senha no banco de dados para um dado usuário é válida.

        Args:
            username (str):
                Nome de usuário
            password (str):
                Senha do usuário

        Returns:
            is_correct (bool):
                `True` se a senha for correta, `False` caso contrário
        """

        if len(username) > 50: return False

        is_correct: bool = False

        with cls.__ENGINE.connect() as conn:
            is_correct = bool(conn.execute(
                text("SELECT (check_password(:username, :password))"),
                {"username": username, "password": password}
            ).scalar())

        return is_correct

    @classmethod
    def create_session(cls, username: str, token: str, ip_address: str, user_agent: str) -> str:
        """
        Cria uma nova sessão no banco de dados.

        Returns:
            session_id (str): ID da sessão criada
        """

        session_id = str(uuid4())
        expires_at = datetime.now(tz=UTC) + timedelta(hours=1)
        row: dict[str, str | datetime] = {
                "session_id": session_id,
                "username": username,
                "token": token,
                "expires_at": expires_at,
                "ip_address": ip_address,
                "user_agent": user_agent
        }

        with (cls.__ENGINE).connect() as conn:
            conn.execute(text(
                "INSERT INTO browser_sessions (session_id, username, token, expires_at, ip_address, user_agent) "
                "VALUES (:session_id, :username, :token, :expires_at, :ip_address, :user_agent)"
            ), row)
            conn.commit()
            conn.commit()

        return session_id

    @classmethod
    def validate_session(cls, session_id: str) -> tuple[bool, str | None]:
        """
        Valida uma sessão no banco de dados.

        Returns:
            (is_valid, username): (True/False, username se válida)
        """
        with (cls.__ENGINE).connect() as conn:
            result = conn.execute(text(
                "SELECT username, expires_at FROM browser_sessions WHERE session_id = :session_id"
            ), {"session_id": session_id}).fetchone()

        if not result:
            return False, None

        username, expires_at = result
        if expires_at < datetime.now(tz=UTC):
            return False, None

        return True, username

    @classmethod
    def get_last_session(cls, username: str) -> tuple[str | None, datetime | None]:
        """
        Recupera a última sessão criada para um dado usuário.

        Returns:
            (session_id, created_at) ou (None, None) se não encontrada
        """
        with (cls.__ENGINE).connect() as conn:
            result = conn.execute(text(
                "SELECT session_id, created_at FROM browser_sessions WHERE username = :username "
                "ORDER BY created_at DESC LIMIT 1"
            ), {"username": username}).fetchone()

        if not result:
            return None, None

        session_id, created_at = result
        return session_id, created_at

    @classmethod
    def get_session_by_token(cls, token: str) -> tuple[str | None, str | None, datetime | None, datetime | None]:
        """
        Recupera sessão pelo token.

        Returns:
            (session_id, username, created_at, expires_at) ou (None, None, None, None)
        """
        with (cls.__ENGINE).connect() as conn:
            result = conn.execute(text(
                "SELECT session_id, username, created_at, expires_at FROM browser_sessions WHERE token = :token LIMIT 1"
            ), {"token": token}).fetchone()

        if not result:
            return None, None, None, None

        session_id, username, created_at, expires_at = result
        return session_id, username, created_at, expires_at
