from pydantic import BaseModel
from datetime import datetime

class BookingBase(BaseModel):
    user_id: int
    flight_id: int
    booking_status: str

class BookingResponse(BookingBase):
    id: int
    booking_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
