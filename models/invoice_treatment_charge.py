# app/models/invoice_treatment_charge.py

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class InvoiceTreatmentCharge(Base):
    __tablename__ = "invoice_treatment_charges"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(Integer, ForeignKey("invoices.id"))

    treatment_id = Column(Integer, ForeignKey("treatments.id"))

    qty = Column(Integer)

    rate = Column(Float)

    amount = Column(Float)

    invoice = relationship("Invoice", back_populates="treatment_charges")