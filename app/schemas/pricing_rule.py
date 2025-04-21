from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class PricingRuleBase(BaseModel):
    name: str
    type: str
    fee: float

    @field_validator('type')
    def check_type(cls, value):
        if value not in ['base', 'luggage', 'priority']:
            raise ValueError("Type must be one of 'base', 'luggage', or 'priority'")
        return value

    @field_validator('fee')
    def check_fee(cls, value):
        if value < 0:
            raise ValueError('Fee must be greater than or equal to 0')
        return value

    class Config:
        orm_mode = True

class PricingRuleCreate(PricingRuleBase):
    pass

class PricingRuleUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    fee: Optional[float] = None

    @field_validator('type')
    def check_type(cls, value):
        if value and value not in ['base', 'luggage', 'priority']:
            raise ValueError("Type must be one of 'base', 'luggage', or 'priority'")
        return value

    @field_validator('fee')
    def check_fee(cls, value):
        if value is not None and value < 0:
            raise ValueError('Fee must be greater than or equal to 0')
        return value

    class Config:
        orm_mode = True

class PricingRuleResponse(PricingRuleBase):
    id: int

    class Config:
        orm_mode = True
