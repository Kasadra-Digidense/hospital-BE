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
    
############################################################
# ➤ C r e a t e    P a t i e n t
############################################################

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

############################################################
# ➤ G e t   A l l   P a t i e n t s
############################################################
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


############################################################
## P A T C H   A P I
############################################################

from schemas.patient import PatientUpdate


@router.patch("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Patient).where(Patient.id == patient_id)
    )

    db_patient = result.scalar_one_or_none()

    if not db_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    data = patient.model_dump(exclude_unset=True)

    # Personal
    if "name" in data:
        db_patient.name = data["name"]

    if "gender" in data:
        db_patient.gender = data["gender"]

    if "age" in data:
        db_patient.age = data["age"]

    if "phone" in data:
        db_patient.phone = data["phone"]

    if "altPhone" in data:
        db_patient.alt_phone = data["altPhone"]

    if "email" in data:
        db_patient.email = data["email"]

    if "place" in data:
        db_patient.place = data["place"]

    if "registrationDate" in data:
        db_patient.registration_date = data["registrationDate"]

    # Address
    if "address" in data:

        address = data["address"]

        if "houseName" in address:
            db_patient.house_name = address["houseName"]

        if "street" in address:
            db_patient.street = address["street"]

        if "city" in address:
            db_patient.city = address["city"]

        if "district" in address:
            db_patient.district = address["district"]

        if "state" in address:
            db_patient.state = address["state"]

        if "country" in address:
            db_patient.country = address["country"]

        if "pincode" in address:
            db_patient.pincode = address["pincode"]

    await db.commit()

    await db.refresh(db_patient)

    return {
        "id": db_patient.id,
        "name": db_patient.name,
        "gender": db_patient.gender,
        "age": db_patient.age,
        "phone": db_patient.phone,
        "altPhone": db_patient.alt_phone,
        "email": db_patient.email,
        "place": db_patient.place,
        "mrdNumber": db_patient.mrd_number,
        "ipNumber": db_patient.ip_number,
        "registrationDate": db_patient.registration_date,
        "address": {
            "houseName": db_patient.house_name,
            "street": db_patient.street,
            "city": db_patient.city,
            "district": db_patient.district,
            "state": db_patient.state,
            "country": db_patient.country,
            "pincode": db_patient.pincode,
        }
    }

############################################################
## D E L E T E     A P I
############################################################

@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Patient).where(Patient.id == patient_id)
    )

    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    await db.delete(patient)

    await db.commit()

    return {
        "success": True,
        "message": "Patient deleted successfully"
    }