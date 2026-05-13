# routes/doctor.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_session

from models.doctor import Doctor

from schemas.doctor_schema import (
    DoctorCreateSchema,
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