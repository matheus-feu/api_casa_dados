from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from app.core.deps import get_session, get_current_user
from app.core.oauth2 import authenticate_user, create_access_token
from app.core.security import get_password_hash
from app.core.settings import settings
from app.exceptions.exception_auth import NotAuthenticatedException
from app.models.user import UserModel
from app.schemas.schema_user import UserSchemaCreate, UserBaseSchema

router = APIRouter()


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    """POST - login, rota para autenticar o usuário e retornar o token de acesso"""

    user = await authenticate_user(email=user_credentials.username, password=user_credentials.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorreto.')

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return JSONResponse(content={"access_token": access_token}, status_code=status.HTTP_200_OK)


@router.get("/me", response_model=UserBaseSchema, status_code=status.HTTP_200_OK, summary="User online")
def get_authenticated_user(current_user: UserModel = Depends(get_current_user)):
    """GET - me, rota para retornar o usuário autenticado"""
    return current_user


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserBaseSchema, summary="Signup")
async def create_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    """POST - signup, rota para criar/cadastrar um novo usuário e enviar um email de confirmação"""

    db_user: UserModel = UserModel(**user.dict())
    db_user.password = get_password_hash(db_user.password)

    async with db as session:
        try:
            session.add(db_user)
            await session.commit()

            return db_user
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um usuário com este email cadastrado.')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/', summary="Users", response_model=List[UserBaseSchema], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    """GET - Usuários, rota para retornar todos os usuários"""

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Não autenticado')

    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserBaseSchema] = result.scalars().unique().all()

        if not users:
            return JSONResponse({'detail': 'Nenhum usuário cadastrado'}, status_code=status.HTTP_200_OK)

        return users


@router.get('/online', summary="Logged in user", response_model=UserBaseSchema, status_code=status.HTTP_200_OK)
async def logged_user(logged_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    """GET - Usuário online, rota para retornar o usuário logado"""

    if not logged_user:
        raise NotAuthenticatedException()

    async with db as session:
        query = select(UserModel).filter(UserModel.email == logged_user.email)
        result = await session.execute(query)
        user: UserModel = result.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, summary="Delete User")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session),
                      current_user: UserModel = Depends(get_current_user)):
    """DELETE - Usuário, rota para deletar um usuário"""

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Não autenticado')

    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_delete: UserModel = result.scalars().unique().one_or_none()

        if user_delete:
            await session.delete(user_delete)
            await session.commit()

            return user_delete
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
