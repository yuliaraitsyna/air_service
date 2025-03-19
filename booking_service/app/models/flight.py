from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, DECIMAL
from app.models.base import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String(20), unique=True, nullable=False)
    departure_airport_id = Column(Integer, ForeignKey("airports.id", ondelete="CASCADE"), nullable=False)
    arrival_airport_id = Column(Integer, ForeignKey("airports.id", ondelete="CASCADE"), nullable=False)
    departure_time = Column(TIMESTAMP, nullable=False)
    arrival_time = Column(TIMESTAMP, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    total_seats = Column(Integer, nullable=False)
