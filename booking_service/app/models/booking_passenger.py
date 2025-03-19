from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base

class BookingPassenger(Base):
    __tablename__ = "booking_passengers"

    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), primary_key=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id", ondelete="CASCADE"), primary_key=True)
