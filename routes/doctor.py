# routes/doctor.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_session

from models.doctor import Doctor

from schemas.doctor_schema import (
    DoctorCreateSchema,
    DoctorUpdateSchema,
    DoctorResponseSchema
)

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


# =========================
# CREATE DOCTOR
# =========================
@router.post("/", response_model=DoctorResponseSchema)
async def create_doctor(
    payload: DoctorCreateSchema,
    db: AsyncSession = Depends(get_session)
):

    doctor = Doctor(
        doctor_name=payload.doctor_name
    )

    db.add(doctor)

    await db.commit()

    await db.refresh(doctor)

    return doctor


# =========================
# GET ALL DOCTORS
# =========================
@router.get("/", response_model=list[DoctorResponseSchema])
async def get_doctors(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Doctor)
    )

    doctors = result.scalars().all()

    return doctors


# =========================
# UPDATE DOCTOR
# =========================
@router.patch("/{doctor_id}", response_model=DoctorResponseSchema)
async def update_doctor(
    doctor_id: int,
    payload: DoctorUpdateSchema,
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Doctor).where(Doctor.id == doctor_id)
    )

    doctor = result.scalar_one_or_none()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.doctor_name = payload.doctor_name

    await db.commit()

    await db.refresh(doctor)

    return doctor


# =========================
# DELETE DOCTOR
# =========================
@router.delete("/{doctor_id}")
async def delete_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Doctor).where(Doctor.id == doctor_id)
    )

    doctor = result.scalar_one_or_none()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    await db.delete(doctor)

    await db.commit()

    return {
        "message": "Doctor deleted successfully"
    }   