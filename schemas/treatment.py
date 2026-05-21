from pydantic import BaseModel


class TreatmentCreate(BaseModel):
    item_name: str
    price: float


class TreatmentUpdate(BaseModel):
    item_name: str
    price: float


class TreatmentResponse(BaseModel):
    id: int
    item_name: str
    price: float

    class Config:
        from_attributes = True