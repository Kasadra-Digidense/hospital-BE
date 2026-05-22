from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_session
from models.treatment import Treatment
from schemas.treatment_schema import (
    TreatmentCreateSchema,
    TreatmentUpdateSchema,
    TreatmentResponseSchema
)

router = APIRouter(
    prefix="/treatments",
    tags=["Treatments"]
)


# Get all treatments
@router.get("/", response_model=list[TreatmentResponseSchema])
async def get_treatments(
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Treatment).order_by(Treatment.item_name)
    )
    treatments = result.scalars().all()
    return treatments


# Create a treatment
@router.post("/", response_model=TreatmentResponseSchema)
async def create_treatment(
    payload: TreatmentCreateSchema,
    db: AsyncSession = Depends(get_session)
):
    existing_result = await db.execute(
        select(Treatment).where(Treatment.item_name == payload.item_name)
    )
    existing = existing_result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Treatment with this name already exists"
        )

    treatment = Treatment(
        item_name=payload.item_name,
        price=payload.price
    )
    db.add(treatment)
    await db.commit()
    await db.refresh(treatment)
    return treatment


# Update a treatment
@router.patch("/{treatment_id}", response_model=TreatmentResponseSchema)
async def update_treatment(
    treatment_id: int,
    payload: TreatmentUpdateSchema,
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
    
    if payload.item_name != treatment.item_name:
        collision_result = await db.execute(
            select(Treatment).where(Treatment.item_name == payload.item_name)
        )
        if collision_result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Treatment with this name already exists"
            )

    treatment.item_name = payload.item_name
    treatment.price = payload.price

    await db.commit()
    await db.refresh(treatment)
    return treatment


# Delete a treatment
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

    await db.delete(treatment)
    await db.commit()
    return {
        "message": "Treatment deleted successfully"
    }