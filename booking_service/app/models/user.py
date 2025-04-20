from sqlalchemy import Column, Enum, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base
from app.schemas.user import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
