from sqlalchemy import Boolean, CheckConstraint, Column, Date, Float, ForeignKey, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    seat_number = Column(Integer, nullable=False)
    with_luggage = Column(Boolean, nullable=False, default=False)
    price = Column(Float, nullable=False)
    booked_at = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    passenger = relationship("Passenger")
    flight = relationship("Flight")
    user = relationship("User")
    
    __table_args__ = (
        CheckConstraint("seat_number > 0", name='check_seat_number'),
        CheckConstraint("price >= 0", name='check_price'),
        CheckConstraint("status IN ('booked', 'canceled', 'checked-in')", name='check_ticket_status'),
    )