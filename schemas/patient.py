from pydantic import BaseModel, EmailStr
from typing import Optional


class AddressSchema(BaseModel):
    houseName: Optional[str] = None
    street: Optional[str] = None

    city: str
    district: str
    state: str

    country: Optional[str] = "India"

    pincode: Optional[str] = None


class PatientCreate(BaseModel):
    # ── Personal ──
    name: str
    gender: str
    age: int

    phone: str
    altPhone: Optional[str] = None

    email: Optional[EmailStr] = None

    # ── Address ──
    address: AddressSchema

    # ── Hospital ──
    place: str

   

    registrationDate: str


class PatientResponse(BaseModel):
    id: int

    name: str
    gender: str
    age: int

    phone: str
    altPhone: Optional[str]

    email: Optional[str]

    place: str

    mrdNumber: str
    registrationDate: str

    address: AddressSchema

    class Config:
        from_attributes = True