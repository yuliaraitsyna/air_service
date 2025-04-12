from sqlalchemy import CheckConstraint, Column, Float, Integer, String
from booking_service.app.core.database import Base


class PricingRule(Base):
    __tablename__ = "pricing_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    fee = Column(Float, nullable=False)
    
    __table_args__ = (
        CheckConstraint("type IN ('base', 'luggage', 'priority')", name='check_rule_type'),
        CheckConstraint("fee >= 0", name='check_fee'),
    )