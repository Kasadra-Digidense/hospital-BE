from pydantic import BaseModel

class TreatmentCreateSchema(BaseModel):
    item_name: str
    price: float

class TreatmentUpdateSchema(BaseModel):
    item_name: str
    price: float

class TreatmentResponseSchema(BaseModel):
    id: int
    item_name: str
    price: float

    class Config:
        from_attributes = True
