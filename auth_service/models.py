import uuid

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum
from datetime import datetime, timezone
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Role(PyEnum):
    admin = "admin"
    passenger = "passenger"
    
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    role = Column(Enum(Role, native_enum=False), default=Role.passenger.value)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    
    
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    refresh_token = Column(String(255), nullable=False)
    expiration = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="refresh_tokens")