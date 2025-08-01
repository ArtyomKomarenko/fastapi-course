from fastapi import APIRouter, Query

from app.handlers.dependencies import PaginationDep
from app.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Айдишник"),  # noqa: FAST002
    title: str | None = Query(None, description="Название отеля"),  # noqa: FAST002
) -> list:
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[(pagination.page - 1) * pagination.per_page : pagination.page * pagination.per_page]


@router.post("")
def create_hotel(hotel_data: Hotel) -> dict:
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name,
        },
    )
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
