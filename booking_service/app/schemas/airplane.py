from pydantic import BaseModel, field_validator, Optional

class AirplaneBase(BaseModel):
    model: str
    capacity: int

    class Config:
        orm_mode = True

