from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    user_id: int
    type: str
    date: datetime
    status: str

    class Config:
        orm_mode = True
        
class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    user_id: Optional[int] = None
    type: Optional[str] = None
    date: Optional[datetime] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True

class PaymentResponse(PaymentBase):
    id: int

    class Config:
        orm_mode = True
