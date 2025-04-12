from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String
from booking_service.app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    
    __table_args__ = (
        CheckConstraint("type IN ('card', 'cash', 'transfer')", name='check_payment_type'),
        CheckConstraint("status IN ('pending', 'completed', 'failed')", name='check_payment_status'),
    )