from pydantic import BaseModel


class Hotel(BaseModel):
    id: int
    title: str
    location: str


class HotelPOST(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None
