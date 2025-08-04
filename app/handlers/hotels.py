from fastapi import APIRouter, Query
from sqlalchemy import insert, select

from app.database import async_session_maker
from app.handlers.dependencies import PaginationDep
from app.models.hotels import HotelsOrm
from app.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(   # noqa: ANN201
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),  # noqa: FAST002
    location: str | None = Query(None, description="Локация отеля"),  # noqa: FAST002
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.like(f"%{title}%"))
        if location:
            query = query.filter(HotelsOrm.location.like(f"%{location}%"))
        query = query.limit(per_page).offset(per_page * (pagination.page - 1))
        result = await session.execute(query)
        return result.scalars().all()


@router.post("")
async def create_hotel(hotel_data: Hotel) -> dict:
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}")
def update_hotel_full(hotel_id: int, hotel_data: Hotel) -> dict:
    global hotels
    exists = False

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            exists = True
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name

    if not exists:
        return {"status": "Отель с указанным id не существует"}

    return {"status": "OK"}


@router.patch("/{hotel_id}")
def update_hotel_partial(hotel_id: int, hotel_data: HotelPATCH) -> dict:
    global hotels
    exists = False

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            exists = True
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name

    if not exists:
        return {"status": "Отель с указанным id не существует"}

    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int) -> dict:
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
