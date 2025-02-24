from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum
from datetime import datetime, timezone
import uuid
from database import Base

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