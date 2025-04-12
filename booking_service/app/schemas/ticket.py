from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class TicketBase(BaseModel):
    passenger_id: int
    payment_id: Optional[int] = None
    flight_id: int
    pricing_rule_id: Optional[int] = None
    seat_number: int
    with_luggage: bool = False
    price: float
    booked_at: date
    status: str

    @field_validator('seat_number')
    def check_seat_number(cls, value):
        if value <= 0:
            raise ValueError("Seat number must be greater than 0")
        return value
    
    @field_validator('price')
    def check_price(cls, value):
        if value < 0:
            raise ValueError("Price must be greater than or equal to 0")
        return value

    @field_validator('status')
    def check_status(cls, value):
        if value not in ['booked', 'canceled', 'checked-in']:
            raise ValueError("Status must be one of 'booked', 'canceled', or 'checked-in'")
        return value

    class Config:
        orm_mode = True

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    passenger_id: Optional[int] = None
    payment_id: Optional[int] = None
    flight_id: Optional[int] = None
    pricing_rule_id: Optional[int] = None
    seat_number: Optional[int] = None
    with_luggage: Optional[bool] = None
    price: Optional[float] = None
    booked_at: Optional[date] = None
    status: Optional[str] = None

    @field_validator('seat_number')
    def check_seat_number(cls, value):
        if value and value <= 0:
            raise ValueError("Seat number must be greater than 0")
        return value
    
    @field_validator('price')
    def check_price(cls, value):
        if value is not None and value < 0:
            raise ValueError("Price must be greater than or equal to 0")
        return value

    @field_validator('status')
    def check_status(cls, value):
        if value and value not in ['booked', 'canceled', 'checked-in']:
            raise ValueError("Status must be one of 'booked', 'canceled', or 'checked-in'")
        return value

    class Config:
        orm_mode = True

class TicketResponse(TicketBase):
    id: int

    class Config:
        orm_mode = True
