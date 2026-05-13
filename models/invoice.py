# # app/models/invoice.py


# models/invoice.py
# models/invoice.py

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from models.base import Base


class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, nullable=False)

    admission_date = Column(Date, nullable=False)
    discharge_date = Column(Date, nullable=False)

    consultant = Column(String, nullable=False)


    bill_no = Column(String, nullable=False)

    room_total = Column(Float, default=0)
    treatment_total = Column(Float, default=0)
    extra_total = Column(Float, default=0)

    gross_total = Column(Float, default=0)
    total_paid = Column(Float, default=0)
    balance = Column(Float, default=0)

    # RELATIONSHIPS
    room_charges = relationship(
        "InvoiceRoomCharge",
        back_populates="invoice",
        cascade="all, delete"
    )

    treatment_charges = relationship(
        "InvoiceTreatmentCharge",
        back_populates="invoice",
        cascade="all, delete"
    )

    additional_charges = relationship(
        "InvoiceAdditionalCharge",
        back_populates="invoice",
        cascade="all, delete"
    )

    payments = relationship(
        "InvoicePayment",
        back_populates="invoice",
        cascade="all, delete"
    )











# from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
# from sqlalchemy.orm import relationship
# from database import Base


# class Invoice(Base):
#     __tablename__ = "invoices"

#     id = Column(Integer, primary_key=True, index=True)

#     patient_id = Column(Integer, ForeignKey("patients.id"))

#     bill_no = Column(String, unique=True)

#     admission_date = Column(Date)
#     discharge_date = Column(Date)

#     consultant = Column(String)

#     room_type = Column(String)
#     room_number = Column(String)

#     gross_total = Column(Float, default=0)
#     paid_total = Column(Float, default=0)
#     balance_total = Column(Float, default=0)

#     room_charges = relationship(
#         "InvoiceRoomCharge",
#         back_populates="invoice",
#         cascade="all, delete"
#     )

#     treatment_charges = relationship(
#         "InvoiceTreatmentCharge",
#         back_populates="invoice",
#         cascade="all, delete"
#     )

#     additional_charges = relationship(
#         "InvoiceAdditionalCharge",
#         back_populates="invoice",
#         cascade="all, delete"
#     )

#     payments = relationship(
#         "InvoicePayment",
#         back_populates="invoice",
#         cascade="all, delete"
#     )