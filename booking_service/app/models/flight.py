from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, ForeignKey, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from booking_service.app.core.database import Base

class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, index=True)
    airplane_id = Column(Integer, ForeignKey("airplanes.id"), nullable=False)
    from_airport_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    to_airport_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    
    airplane = relationship("Airplane")
    from_airport = relationship("Airport", foreign_keys=[from_airport_id])
    to_airport = relationship("Airport", foreign_keys=[to_airport_id])
    
    __table_args__ = (
        CheckConstraint("arrival_time > departure_time", name='check_flight_times'),
        CheckConstraint("from_airport_id <> to_airport_id", name='check_different_airports'),
    )