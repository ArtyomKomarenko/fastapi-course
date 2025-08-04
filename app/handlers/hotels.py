from fastapi import APIRouter, Query

from app.database import async_session_maker
from app.handlers.dependencies import PaginationDep
from app.repositories.hotels import HotelsRepository
from app.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),  # noqa: FAST002
    location: str | None = Query(None, description="Локация отеля"),  # noqa: FAST002
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.post("")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


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
