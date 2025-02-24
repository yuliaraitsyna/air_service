from enum import Enum
from pydantic import BaseModel


class Role(Enum):
    admin = "admin"
    passenger = "passenger"
           
class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    role: Role
    
class UserResponse(BaseModel):
    id: str
    username: str
    name: str
    username: str
    role: Role