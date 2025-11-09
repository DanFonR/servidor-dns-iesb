from sqlalchemy import text
from sqlalchemy.engine import create_engine, Engine
from os import getenv

# DB_URL: postgresql+psycopg://USUARIO:SENHA@NOME_DO_CONTAINER:PORTA/BANCO
DB_URL: str | None = getenv("DB_URL")

if not DB_URL:
    exit(1)

class SQLServices:
    """
    Classe que fornece serviços de banco de dados. Não é instanciável e não pode
    ter subclasses.
    """

    __ENGINE: Engine = create_engine(DB_URL)

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

        with (cls.__ENGINE).connect() as conn:
            is_correct = bool(conn.execute(text(
                "SELECT (check_password(:username, :password))",
                {"username": username, "password": password}
            )).scalar())

        return is_correct
