from datetime import timedelta, datetime
from typing import Optional

from jose import jwt
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import verify_password
from app.core.settings import settings
from app.models.user import UserModel


async def authenticate_user(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    """Verifica se o email do usuário existe e a senha está correta e retorna um usuário"""

    async with db as session:
        query = select(UserModel).where(UserModel.email == email)
        user = await session.execute(query)
        user: UserModel = user.scalars().unique().one_or_none()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Cria um token JWT de acesso para o usuário realizar as requisições na API.
    Para saber mais sobre acesse: https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3"""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt
