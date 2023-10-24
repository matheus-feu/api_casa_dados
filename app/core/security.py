from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta, comparando a senha fornecida com a senha hash.
    A senha fornecida (em texto plano) é primeiro hash e, em seguida, comparada com a senha hash."""
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    """Retorna a senha hash."""
    return pwd_context.hash(password)
