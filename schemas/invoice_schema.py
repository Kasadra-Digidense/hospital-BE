# app/schemas/invoice_schema.py

from pydantic import BaseModel
from typing import List
from datetime import date


class RoomChargeSchema(BaseModel):
    room_id: int
    days: int
    rate: float
    amount: float


class TreatmentChargeSchema(BaseModel):
    treatment_id: int
    qty: int
    rate: float
    amount: float


class AdditionalChargeSchema(BaseModel):
    type: str
    quantity: int
    unit_price: float
    total: float


class PaymentSchema(BaseModel):
    method: str
    amount: float


class InvoiceCreateSchema(BaseModel):

    patient_id: int

    admission_date: date
    discharge_date: date

    consultant: str

    advance_amount: float
    discount: float 

    room_total: float
    treatment_total: float
    extra_total: float

    gross_total: float
    total_paid: float
    balance: float

    room_charges: List[RoomChargeSchema]

    treatment_charges: List[TreatmentChargeSchema]

    additional_charges: List[AdditionalChargeSchema]

    payments: List[PaymentSchema]
