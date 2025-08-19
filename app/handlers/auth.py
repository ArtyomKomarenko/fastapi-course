from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from starlette.responses import Response

from app.database import async_session_maker
from app.repositories.users import UsersRepository
from app.schemas.users import UserAdd, UserCredentials, UserRequestAdd
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(user_data: UserRequestAdd):
    hashed_password = AuthService.get_password_hash(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    try:
        async with async_session_maker() as session:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
    except IntegrityError:
        return HTTPException(400, f"Пользователь с email {user_data.email} уже существует")
    return {"status": "OK"}


@router.post("/login")
async def login_user(credentials: UserCredentials, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=credentials.email)
        if not user:
            raise HTTPException(401, "Неверный email или пароль")
        if not AuthService.verify_password(credentials.password, user.hashed_password):
            raise HTTPException(401, "Неверный email или пароль")
        access_token = AuthService.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
