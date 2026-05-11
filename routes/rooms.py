from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_session
from models.room import Room

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


# Get all rooms
@router.get("/")
async def get_rooms(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Room).order_by(Room.room_number)
    )

    rooms = result.scalars().all()

    return rooms