from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_session
from models.treatment import Treatment
from schemas.treatment import (
    TreatmentCreate,
    TreatmentUpdate,
    TreatmentResponse
)

router = APIRouter(
    prefix="/treatments",
    tags=["Treatments"]
)


# -----------------------------------
# GET ALL ACTIVE TREATMENTS
# -----------------------------------
@router.get("/", response_model=list[TreatmentResponse])
async def get_treatments(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Treatment)
        .where(Treatment.is_active == True)
    )

    treatments = result.scalars().all()

    return treatments


# -----------------------------------
# GET TREATMENT BY ID
# -----------------------------------
# @router.get("/{treatment_id}", response_model=TreatmentResponse)
# async def get_treatment_by_id(
#     treatment_id: int,
#     db: AsyncSession = Depends(get_session)
# ):

#     result = await db.execute(
#         select(Treatment).where(Treatment.id == treatment_id)
#     )

#     treatment = result.scalar_one_or_none()

#     if not treatment:
#         raise HTTPException(
#             status_code=404,
#             detail="Treatment not found"
#         )

#     return treatment


# -----------------------------------
# CREATE TREATMENT
# -----------------------------------
@router.post("/", response_model=TreatmentResponse)
async def create_treatment(
    treatment_data: TreatmentCreate,
    db: AsyncSession = Depends(get_session)
):

    # Check duplicate item_name
    result = await db.execute(
        select(Treatment).where(
            Treatment.item_name == treatment_data.item_name
        )
    )

    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Treatment already exists"
        )

    new_treatment = Treatment(
        item_name=treatment_data.item_name,
        price=treatment_data.price
    )

    db.add(new_treatment)

    await db.commit()
    await db.refresh(new_treatment)

    return new_treatment


# -----------------------------------
# UPDATE TREATMENT
# -----------------------------------
@router.put("/{treatment_id}", response_model=TreatmentResponse)
async def update_treatment(
    treatment_id: int,
    treatment_data: TreatmentUpdate,
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Treatment).where(Treatment.id == treatment_id)
    )

    treatment = result.scalar_one_or_none()

    if not treatment:
        raise HTTPException(
            status_code=404,
            detail="Treatment not found"
        )

    treatment.item_name = treatment_data.item_name
    treatment.price = treatment_data.price

    await db.commit()
    await db.refresh(treatment)

    return treatment

# -----------------------------------
# SOFT DELETE TREATMENT
# -----------------------------------
@router.delete("/{treatment_id}")
async def delete_treatment(
    treatment_id: int,
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Treatment).where(Treatment.id == treatment_id)
    )

    treatment = result.scalar_one_or_none()

    if not treatment:
        raise HTTPException(
            status_code=404,
            detail="Treatment not found"
        )

    # Soft delete
    treatment.is_active = False

    await db.commit()

    return {
        "message": "Treatment deleted successfully"
    }