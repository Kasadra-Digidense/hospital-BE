from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_session
from models.patient import Patient
from schemas.patient import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"])


# ➤ Create Patient
@router.post("/", response_model=PatientResponse)
async def create_patient(
    patient: PatientCreate,
    db: AsyncSession = Depends(get_session)
):
    # check duplicate phone
    result = await db.execute(
        select(Patient).where(Patient.phone == patient.phone)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Phone already exists")

    new_patient = Patient(
        name=patient.name,
        phone=patient.phone,
        place=patient.place
    )

    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)

    return new_patient


# ➤ Get All Patients
@router.get("/", response_model=list[PatientResponse])
async def get_patients(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Patient))
    patients = result.scalars().all()
    return patients