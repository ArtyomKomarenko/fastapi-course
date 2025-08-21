from pydantic import BaseModel


class RoomPOST(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int


class RoomPATCH(BaseModel):
    hotel_id: int | None
    title: str | None
    description: str | None
    price: int | None
    quantity: int | None


class Room(BaseModel):
    id: int
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int
