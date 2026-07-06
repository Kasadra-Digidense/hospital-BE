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
    ipNumber: str | None = None
    mrdNumber: str
    registrationDate: str

    address: AddressSchema

    class Config:
        from_attributes = True

class AddressUpdate(BaseModel):
    houseName: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None


class PatientUpdate(BaseModel):

    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None

    phone: Optional[str] = None
    altPhone: Optional[str] = None

    email: Optional[str] = None

    place: Optional[str] = None

    registrationDate: Optional[str] = None

    address: Optional[AddressUpdate] = None