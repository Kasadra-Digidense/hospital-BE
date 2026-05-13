# schemas/doctor_schema.py

from pydantic import BaseModel


class DoctorCreateSchema(BaseModel):
    doctor_name: str


class DoctorResponseSchema(BaseModel):
    id: int
    doctor_name: str

    class Config:
        from_attributes = True