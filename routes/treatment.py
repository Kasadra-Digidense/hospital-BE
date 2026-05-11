from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_session
from models.treatment import Treatment

router = APIRouter(
    prefix="/treatments",
    tags=["Treatments"]
)


# Get all treatments
@router.get("/")
async def get_treatments(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Treatment).order_by(Treatment.item_name)
    )

    treatments = result.scalars().all()

    return treatments