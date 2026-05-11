from sqlalchemy import Column, Integer, String, Float
from models.base import Base


class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)