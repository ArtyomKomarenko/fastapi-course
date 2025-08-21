from sqlalchemy import select

from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepository
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self, hotel_id: int) -> list[Room]:
        query = select(RoomsOrm).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)

        return [Room.model_validate(room, from_attributes=True) for room in result.scalars().all()]
