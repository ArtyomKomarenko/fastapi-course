from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from app.database import async_session_maker
from app.repositories.hotels import HotelsRepository
from app.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, gt=0, description="Порядковый номер страницы")]
    per_page: Annotated[int | None, Query(None, gt=0, lt=100, description="Кол-во элементов на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(401, detail="Неверный токен")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService.decode_token(token)
    return data.get("user_id")


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def ensure_hotel_exists(hotel_id: int) -> int:
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Отель не найден")
        return hotel_id


HotelIdDep = Annotated[int, Depends(ensure_hotel_exists)]
