from pydantic import BaseModel

class BookingPassengerBase(BaseModel):
    booking_id: int
    passenger_id: int
