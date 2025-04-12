from pydantic import BaseModel

class AirportBase(BaseModel):
    name: str
    code: str
    city: str
    country: str
    
    class Config:
        orm_mode = True
    
from pydantic import BaseModel, field_validator, Optional

class AirportBase(BaseModel):
    name: str
    code: str
    city: str
    country: str
    
    class Config:
        orm_mode = True

class AirportCreate(AirportBase):
    @field_validator('code')
    def check_code(cls, code):
        if len(code) != 3:
            raise ValueError('Code must be 3 characters or fewer.')
        return code

class AirportUpdate(AirportBase):
    name: Optional[str] = None
    code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    
    @field_validator('code')
    def check_code(cls, code):
        if code is not None and len(code) > 3:
            raise ValueError('Code must be 3 characters or fewer.')
        return code

class AirportDelete(BaseModel):
    id: int
    
    class Config:
        orm_mode = True  
