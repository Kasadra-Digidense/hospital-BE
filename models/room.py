from sqlalchemy import Column, Integer, String, Float
from models.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    room_group = Column(String, nullable=False)

    room_number = Column(String, nullable=False, unique=True)

    rate = Column(Float, nullable=False)