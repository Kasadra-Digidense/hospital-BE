# models/invoice_additional_charge.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class InvoiceAdditionalCharge(Base):

    __tablename__ = "invoice_additional_charges"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(Integer, ForeignKey("invoices.id"))

    charge_type = Column(String)
    amount = Column(Float)

    invoice = relationship(
        "Invoice",
        back_populates="additional_charges"
    )