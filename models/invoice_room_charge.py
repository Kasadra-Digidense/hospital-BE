# models/invoice_room_charge.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

class InvoiceRoomCharge(Base):
    __tablename__ = "invoice_room_charges"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(Integer, ForeignKey("invoices.id"))

    room_id = Column(Integer, ForeignKey("rooms.id"))

    days = Column(Integer)

    rate = Column(Float)

    amount = Column(Float)

    invoice = relationship(
        "Invoice",
        back_populates="room_charges"
    )

