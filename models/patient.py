from sqlalchemy import Column, Integer, String
from models.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    # ── Personal Information ──
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    phone = Column(String, nullable=False)
    alt_phone = Column(String, nullable=True)

    email = Column(String, nullable=True)

    # ── Address Information ──
    house_name = Column(String, nullable=True)
    street = Column(String, nullable=True)

    city = Column(String, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)

    country = Column(String, nullable=True)

    pincode = Column(String, nullable=True)

    # ── Hospital Information ──
    place = Column(String, nullable=True)
    mrd_number = Column(String, nullable=False, unique=True)
    ip_number = Column(String, nullable=True, unique=True)
    registration_date = Column(String, nullable=False)