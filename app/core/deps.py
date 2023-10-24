from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.future import select

from app.core.settings import settings
from app.db.session import get_session, Session
from app.models.user import UserModel
from app.schemas.schema_auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.app_v1_prefix}/users/login")


async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> UserModel:
    """Decodifica o token JWT e retorna os dados do usuário"""

    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm], options={"verify_aud": False})
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data: TokenData = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    async with db as session:
        query = select(UserModel).where(UserModel.email == token_data.username)
        user = await session.execute(query)
        user: UserModel = user.scalars().unique().one_or_none()

        if user is None:
            raise credentials_exception

        return user
