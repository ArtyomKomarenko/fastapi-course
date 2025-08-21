# ruff: noqa: ARG001
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.database import async_session_maker
from app.handlers.dependencies import HotelIdDep
from app.repositories.rooms import RoomsRepository
from app.schemas.rooms import RoomPATCH, RoomPOST

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel(hotel_id: HotelIdDep):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: HotelIdDep, room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if not room:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Комната не найдена")
        return room


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: HotelIdDep, room_data: RoomPOST):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room_full(hotel_id: HotelIdDep, room_id: int, room_data: RoomPOST):
    async with async_session_maker() as session:
        to_edit = await RoomsRepository(session).get_one_or_none(id=room_id)
        if not to_edit:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Комната не найдена")
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room_partial(hotel_id: HotelIdDep, room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        to_edit = await RoomsRepository(session).get_one_or_none(id=room_id)
        if not to_edit:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Комната не найдена")
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: HotelIdDep, room_id: int):
    async with async_session_maker() as session:
        to_delete = await RoomsRepository(session).get_one_or_none(id=room_id)
        if not to_delete:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Комната не найдена")
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}
