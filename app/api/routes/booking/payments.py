from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
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

@router.post(
    "/", 
    response_model=PaymentResponse,
    summary="Create a new payment",
    description="""
Create a new payment record.  
Anyone can create a payment — authorization is not required.
"""
)
def create_payment_endpoint(payment: PaymentCreate, db: db_annotated):
    return create_payment(db, payment)

@router.get(
    "/{payment_id}", 
    response_model=PaymentResponse,
    summary="Get payment by ID",
    description="Retrieve a specific payment by its ID. Returns 404 if not found."
)
def read_payment(payment_id: int, db: db_annotated):
    db_payment = get_payment(db, payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get(
    "/", 
    response_model=list[PaymentResponse],
    summary="Retrieve all payments",
    description="""
Get a paginated list of all payments.  
Use `skip` and `limit` query parameters for pagination.
"""
)
def read_payments(db: db_annotated, skip: int = 0, limit: int = 10):
    return get_payments(db, skip, limit)

@router.put(
    "/{payment_id}", 
    response_model=PaymentResponse,
    summary="Update a payment",
    description="""
Update a payment by its ID.  
Only users with the `admin` role are authorized to perform this action.  
Returns 404 if the payment does not exist.
"""
)
def update_payment_endpoint(payment_id: int, payment: PaymentUpdate, db: db_annotated, user: user_admin_annotated):
    updated = update_payment(db, payment_id, payment)
    if updated is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated

@router.delete(
    "/{payment_id}", 
    response_model=PaymentResponse,
    summary="Delete a payment",
    description="""
Delete a payment by its ID.  
Only users with the `admin` role are authorized to perform this action.  
Returns 404 if the payment does not exist.
"""
)
def delete_payment_endpoint(payment_id: int, db: db_annotated, user: user_admin_annotated):
    deleted = delete_payment(db, payment_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return deleted