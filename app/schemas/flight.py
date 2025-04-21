from pydantic import BaseModel, field_validator, model_validator, validator
from typing import Optional
from datetime import datetime, timezone

from app.schemas.airplane import AirplaneResponse
from app.schemas.airport import AirportResponse

class FlightBase(BaseModel):
    airplane_id: int
    from_airport_id: int
    to_airport_id: int
    departure_time: datetime
    arrival_time: datetime

    @model_validator(mode="before")
    def check_different_airports(cls, values):
        from_airport_id = values.get('from_airport_id')
        to_airport_id = values.get('to_airport_id')
        
        if from_airport_id == to_airport_id:
            raise ValueError("From and To airports must be different.")
        
        return values

    @model_validator(mode='before')
    def check_arrival_after_departure(cls, values):
        departure_time = values.get('departure_time')
        arrival_time = values.get('arrival_time')

        if departure_time and arrival_time:
            if arrival_time <= departure_time:
                raise ValueError("Arrival time must be after departure time.")
        
        return values

    class Config:
        from_attributes = True


class FlightCreate(FlightBase):
    departure_time: datetime
    arrival_time: datetime

    @model_validator(mode='before')
    def check_fields(cls, values):
        departure_time = values.get('departure_time')
        arrival_time = values.get('arrival_time')

        if isinstance(departure_time, str):
            departure_time = datetime.fromisoformat(departure_time)

        if isinstance(arrival_time, str):
            arrival_time = datetime.fromisoformat(arrival_time)

        if departure_time and departure_time <= datetime.now(timezone.utc):
            raise ValueError("Departure time must be in the future.")
        
        if arrival_time and departure_time and arrival_time <= departure_time:
            raise ValueError("Arrival time must be after departure time.")

        return values


class FlightUpdate(BaseModel):
    airplane_id: Optional[int] = None
    from_airport_id: Optional[int] = None
    to_airport_id: Optional[int] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None

    @field_validator('departure_time')
    @classmethod
    def check_departure_time(cls, v: Optional[datetime], values: dict) -> Optional[datetime]:
        if isinstance(v, str):
            v = datetime.fromisoformat(v)

        if v and v <= datetime.now(timezone.utc):
            raise ValueError("Departure time must be in the future.")
        return v

    @field_validator('arrival_time')
    @classmethod
    def check_arrival_time(cls, v: Optional[datetime], values: dict) -> Optional[datetime]:
        if isinstance(v, str):
            v = datetime.fromisoformat(v)

        if v and 'departure_time' in values and values['departure_time'] and v <= values['departure_time']:
            raise ValueError("Arrival time must be after departure time.")
        return v

    @field_validator('from_airport_id')
    @classmethod
    def check_different_airports(cls, v: Optional[int], values: dict) -> Optional[int]:
        if v and 'to_airport_id' in values and values['to_airport_id'] and v == values['to_airport_id']:
            raise ValueError("From and To airports cannot be the same.")
        return v

    class Config:
        from_attributes = True


class FlightDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True


class FlightResponse(BaseModel):
    id: int
    airplane: AirplaneResponse
    from_airport: AirportResponse
    to_airport: AirportResponse
    departure_time: datetime
    arrival_time: datetime

    class Config:
        from_attributes = True
