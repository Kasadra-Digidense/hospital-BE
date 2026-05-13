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
    charge_type: str
    amount: float


class PaymentSchema(BaseModel):
    method: str
    amount: float


class InvoiceCreateSchema(BaseModel):
    patient_id: int

    admission_date: date
    discharge_date: date

    consultant: str

    room_type: str
    room_number: str

    room_charges: List[RoomChargeSchema]

    treatment_charges: List[TreatmentChargeSchema]

    additional_charges: List[AdditionalChargeSchema]

    payments: List[PaymentSchema]