from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query

from app.database import async_session_maker
from app.handlers.dependencies import PaginationDep
from app.repositories.hotels import HotelsRepository
from app.schemas.hotels import HotelPATCH, HotelPOST

router = APIRouter(prefix="/hotels", tags=["Hotels"])


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


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        return hotel


@router.post("")
async def create_hotel(hotel_data: HotelPOST):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel_full(hotel_id: int, hotel_data: HotelPOST):
    async with async_session_maker() as session:
        to_edit = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if not to_edit:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def update_hotel_partial(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        to_edit = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if not to_edit:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        to_delete = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if not to_delete:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
