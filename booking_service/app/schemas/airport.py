from pydantic import BaseModel

class AirportBase(BaseModel):
    name: str
    code: str
    city: str
    country: str