from pydantic import BaseModel

class PatientCreate(BaseModel):
    name: str
    phone: str
    place: str

class PatientResponse(BaseModel):
    id: int
    name: str
    phone: str
    place: str

    class Config:
        from_attributes = True