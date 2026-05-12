# models/invoice.py

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    bill_no = Column(String, unique=True)

    patient_id = Column(Integer, ForeignKey("patients.id"))

    admission_date = Column(Date)
    discharge_date = Column(Date)

    consultant = Column(String)

    room_type = Column(String)
    room_number = Column(String)

    gross_total = Column(Float, default=0)
    paid_total = Column(Float, default=0)
    balance_total = Column(Float, default=0)

    patient = relationship("Patient")

    room_charges = relationship("InvoiceRoomCharge",back_populates="invoice", cascade="all, delete")

    treatment_charges = relationship("InvoiceTreatmentCharge",back_populates="invoice",cascade="all, delete")

    additional_charges = relationship("InvoiceAdditionalCharge",back_populates="invoice",cascade="all, delete")

    payments = relationship("InvoicePayment",back_populates="invoice",cascade="all, delete")