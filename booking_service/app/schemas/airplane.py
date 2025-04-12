from pydantic import BaseModel, field_validator
from typing import Optional

class AirplaneBase(BaseModel):
    model: str
    capacity: int

    class Config:
        orm_mode = True

class AirplaneCreate(AirplaneBase):
    @field_validator('capacity')
    def check_capacity(cls, capacity):
        if capacity <= 0:
            raise ValueError('Capacity must be greater than 0')
        return capacity

class AirplaneUpdate(BaseModel):
    model: Optional[str] = None
    capacity: Optional[int] = None
    
    @field_validator('capacity')
    def check_capacity(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Capacity must be greater than 0')
        return v

class AirplaneDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True

class AirplaneResponse(AirplaneBase):
    id: int
    model: str
    capacity: int

    class Config:
        orm_mode = True