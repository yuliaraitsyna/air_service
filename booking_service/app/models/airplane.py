from sqlalchemy import CheckConstraint, Column, Integer, String
from booking_service.app.core.database import Base


class Airplane(Base):
    __tablename__ = "airplanes"
    
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint("capacity > 0", name='check_capacity'),
    )