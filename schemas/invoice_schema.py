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

    # bill_no: str

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











# # app/schemas/invoice_schema.py

# from pydantic import BaseModel
# from typing import List
# from datetime import date


# # =========================
# # ROOM CHARGES
# # =========================

# class RoomChargeSchema(BaseModel):
#     room: str
#     days: int
#     rate: float
#     amount: float


# # =========================
# # TREATMENT CHARGES
# # =========================

# class TreatmentChargeSchema(BaseModel):
#     treatment: str
#     qty: int
#     rate: float
#     amount: float


# # =========================
# # ADDITIONAL CHARGES
# # =========================

# class AdditionalChargeSchema(BaseModel):
#     type: str
#     amount: float


# # =========================
# # PAYMENTS
# # =========================

# class PaymentSchema(BaseModel):
#     method: str
#     amount: float


# # =========================
# # MAIN INVOICE
# # =========================

# class InvoiceCreateSchema(BaseModel):

#     patient_id: int

#     admission_date: date
#     discharge_date: date

#     consultant: str

#     room_type: str
#     room_number: str

#     bill_no: str

#     room_total: float
#     treatment_total: float
#     extra_total: float

#     gross_total: float
#     total_paid: float
#     balance: float

#     room_charges: List[RoomChargeSchema]

#     treatment_charges: List[TreatmentChargeSchema]

#     additional_charges: List[AdditionalChargeSchema]

#     payments: List[PaymentSchema]