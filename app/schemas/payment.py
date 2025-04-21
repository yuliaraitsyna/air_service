from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class PaymentType(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentBase(BaseModel):
    user_id: int
    type: PaymentType
    amount: float = Field(gt=0)
    status: PaymentStatus = PaymentStatus.PENDING

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    user_id: Optional[int] = None
    type: Optional[PaymentType] = None
    amount: Optional[float] = Field(default=None, gt=0)
    status: Optional[PaymentStatus] = None

class PaymentResponse(PaymentBase):
    id: int

    class Config:
        orm_mode = True
