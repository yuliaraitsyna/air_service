from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class FlightBase(BaseModel):
    airplane_id: int
    from_airport_id: int
    to_airport_id: int
    departure_time: datetime
    arrival_time: datetime

    class Config:
        orm_mode = True

class FlightCreate(FlightBase):
    
    @field_validator('departure_time')
    def check_departure_time(cls, departure_time):
        if departure_time <= datetime.now():
            raise ValueError("Departure time must be in the future.")
        return departure_time

    @field_validator('arrival_time')
    def check_arrival_time(cls, arrival_time, values):
        if arrival_time <= values.get('departure_time'):
            raise ValueError("Arrival time must be after departure time.")
        return arrival_time

    @field_validator('from_airport_id', 'to_airport_id')
    def check_different_airports(cls, v, values, field):
        if field.name == 'from_airport_id' and v == values.get('to_airport_id'):
            raise ValueError("From and To airports cannot be the same.")
        return v

    class Config:
        orm_mode = True

class FlightUpdate(BaseModel):
    airplane_id: Optional[int] = None
    from_airport_id: Optional[int] = None
    to_airport_id: Optional[int] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None

    @field_validator('departure_time')
    def check_departure_time(cls, departure_time):
        if departure_time and departure_time <= datetime.now():
            raise ValueError("Departure time must be in the future.")
        return departure_time

    @field_validator('arrival_time')
    def check_arrival_time(cls, arrival_time, values):
        if arrival_time and arrival_time <= values.get('departure_time'):
            raise ValueError("Arrival time must be after departure time.")
        return arrival_time

    @field_validator('from_airport_id', 'to_airport_id')
    def check_different_airports(cls, v, values, field):
        if field.name == 'from_airport_id' and v == values.get('to_airport_id'):
            raise ValueError("From and To airports cannot be the same.")
        return v

    class Config:
        orm_mode = True

class FlightDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True
