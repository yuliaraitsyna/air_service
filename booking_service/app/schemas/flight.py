from pydantic import BaseModel
from datetime import datetime

class FlightBase(BaseModel):
    flight_number: str
    departure_airport_id: int
    arrival_airport_id: int
    departure_time: datetime
    arrival_time: datetime
    price: float
    total_seats: int

class FlightResponse(FlightBase):
    id: int

    class Config:
        from_attributes = True
