from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import get_session
from models.patient import Patient
from schemas.patient import PatientCreate, PatientResponse

from datetime import datetime
import random

router = APIRouter(prefix="/patients", tags=["Patients"])

################################
## Create MRD Number Generator
###############################
async def generate_mrd(db: AsyncSession):

    result = await db.execute(
        select(Patient).order_by(Patient.id.desc())
    )

    last_patient = result.scalars().first()

    if not last_patient:
        return "22001"

    last_mrd = int(last_patient.mrd_number)

    new_mrd = last_mrd + 1

    return str(new_mrd)

################################
## Create IP Number Generator
###############################
async def generate_ip_number(db: AsyncSession):

    result = await db.execute(
        select(Patient).order_by(Patient.id.desc())
    )

    last_patient = result.scalars().first()

    current_year = datetime.now().year

    if not last_patient or not last_patient.ip_number:
        return f"{current_year}/1"

    try:
        last_ip = last_patient.ip_number

        last_serial = int(last_ip.split("/")[-1])

        new_serial = last_serial + 1

        return f"{current_year}/{new_serial}"

    except:
        return f"{current_year}/1"
    

# ➤ Create Patient
@router.post("/", response_model=PatientResponse)
async def create_patient(
    patient: PatientCreate,
    db: AsyncSession = Depends(get_session)
):
    generated_ip = await generate_ip_number(db)
    generated_mrd = await generate_mrd(db)
    
    new_patient = Patient(
        # ── Personal ──
        name=patient.name,
        gender=patient.gender,
        age=patient.age,

        phone=patient.phone,
        alt_phone=patient.altPhone,

        email=patient.email,

        # ── Address ──
        house_name=patient.address.houseName,
        street=patient.address.street,

        city=patient.address.city,
        district=patient.address.district,
        state=patient.address.state,

        country=patient.address.country,

        pincode=patient.address.pincode,

        # ── Hospital ──
        place=patient.place,
        ip_number=generated_ip,
        mrd_number=generated_mrd,
      
        registration_date=patient.registrationDate,
    )

    db.add(new_patient)

    await db.commit()

    await db.refresh(new_patient)

    return {
        "id": new_patient.id,

        "name": new_patient.name,
        "gender": new_patient.gender,
        "age": new_patient.age,

        "phone": new_patient.phone,
        "altPhone": new_patient.alt_phone,

        "email": new_patient.email,

        "place": new_patient.place,
        "ipNumber": new_patient.ip_number,
        "mrdNumber": new_patient.mrd_number,

        "registrationDate": new_patient.registration_date,

        "address": {
            "houseName": new_patient.house_name,
            "street": new_patient.street,
            "city": new_patient.city,
            "district": new_patient.district,
            "state": new_patient.state,
            "country": new_patient.country,
            "pincode": new_patient.pincode,
        }
    }


# ➤ Get All Patients
@router.get("/", response_model=list[PatientResponse])
async def get_patients(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(select(Patient))

    patients = result.scalars().all()

    response = []

    for patient in patients:
        response.append({
            "id": patient.id,

            "name": patient.name,
            "gender": patient.gender,
            "age": patient.age,

            "phone": patient.phone,
            "altPhone": patient.alt_phone,

            "email": patient.email,

            "place": patient.place,

            "mrdNumber": patient.mrd_number,
            "ipNumber": patient.ip_number,
            "registrationDate": patient.registration_date,

            "address": {
                "houseName": patient.house_name,
                "street": patient.street,

                "city": patient.city,
                "district": patient.district,
                "state": patient.state,

                "country": patient.country,

                "pincode": patient.pincode,
            }
        })

    return response