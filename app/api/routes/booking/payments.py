from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking import (
    create_payment, get_payment, get_payments, update_payment, delete_payment,
)

from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate
from app.models.user import User
from app.services.auth import require_role

router = APIRouter()

db_annotated = Annotated[Session, Depends(get_db)]
user_admin_annotated = Annotated[User, Depends(require_role(["admin"]))]

@router.post("/payments/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: db_annotated):
    return create_payment(db, payment)

@router.get("/payments/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, db: db_annotated):
    db_payment = get_payment(db, payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/payments/", response_model=list[PaymentResponse])
def read_payments(db: db_annotated, skip: int = 0, limit: int = 10):
    return get_payments(db, skip, limit)

@router.put("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentUpdate, db: db_annotated, user: user_admin_annotated):
    updated = update_payment(db, payment_id, payment)
    if updated is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated

@router.delete("/payments/{payment_id}", response_model=PaymentResponse)
def delete_payment(payment_id: int, db: db_annotated, user: user_admin_annotated):
    deleted = delete_payment(db, payment_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return deleted