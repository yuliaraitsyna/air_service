from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Date
from booking_service.app.core.database import Base

class Passenger(Base):
    __tablename__ = "passengers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    passport_number = Column(String(100), unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)

