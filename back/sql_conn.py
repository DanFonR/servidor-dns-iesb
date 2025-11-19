from sqlalchemy import text
from sqlalchemy.engine import create_engine, Engine
from os import getenv
from datetime import datetime, timedelta
from datetime import timezone
from uuid import uuid4

# DB_URL: postgresql+psycopg://USUARIO:SENHA@NOME_DO_CONTAINER:PORTA/BANCO
DB_URL: str | None = getenv("DB_URL")

UTC: timezone = timezone.utc

if not DB_URL:
    print("DB_URL vazia")
    exit(1)

class SQLServices:
    """
    Classe que fornece serviços de banco de dados. Não é instanciável e não pode
    ter subclasses.
    """

    __ENGINE: Engine = create_engine(DB_URL)

    def __new__(cls):
        raise TypeError("Class SQLServices cannot not be instantiated")

    def __init_subclass__(cls):
        raise TypeError("Class SQLServices cannot not be inherited from")

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

        with (cls.__ENGINE).connect() as conn:
            is_correct = bool(conn.execute(text(
                "SELECT (check_password(:username, :password))",
                {"username": username, "password": password}
            )).scalar())

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
                "INSERT INTO sessions (session_id, username, token, expires_at, ip_address, user_agent) "
                "VALUES (:session_id, :username, :token, :expires_at, :ip_address, :user_agent)"
            ), row)
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
                "SELECT username, expires_at FROM sessions WHERE session_id = :session_id"
            ), {"session_id": session_id}).fetchone()

        if not result:
            return False, None

        username, expires_at = result
        if expires_at < datetime.now(tz=UTC):
            return False, None

        return True, username
