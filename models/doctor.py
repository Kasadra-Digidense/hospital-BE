# models/doctor.py

from sqlalchemy import Column, Integer, String
from models.base import Base


class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    doctor_name = Column(String, nullable=False)