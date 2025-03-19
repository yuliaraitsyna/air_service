from pydantic import BaseModel
from datetime import date

class PassengerBase(BaseModel):
    first_name: str
    last_name: str
    passport_number: str
    date_of_birth: date
    gender: str

class PassengerCreate(PassengerBase):
    user_id: int

class PassengerResponse(PassengerBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
