from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: UserRole = "user"

class UserResponse(BaseModel):
    username: str
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str
