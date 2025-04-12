from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class PassengerBase(BaseModel):
    name: str
    surname: str
    passport_number: str
    birth_date: date
    
    @field_validator('birth_date')
    def check_birth_date(cls, birth_date):
        if birth_date > date.today():
            raise ValueError('Birth date cannot be in the future')
        return birth_date

    class Config:
        orm_mode = True

class PassengerCreate(PassengerBase):
    pass

class PassengerUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    passport_number: Optional[str] = None
    birth_date: Optional[date] = None
    
    @field_validator('birth_date')
    def check_birth_date(cls, birth_date):
        if birth_date and birth_date > date.today():
            raise ValueError('Birth date cannot be in the future')
        return birth_date

    class Config:
        orm_mode = True

class PassengerResponse(PassengerBase):
    id: int

    class Config:
        orm_mode = True
