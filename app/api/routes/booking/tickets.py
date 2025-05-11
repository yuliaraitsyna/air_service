from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketResponse
from app.core.database import get_db
from app.services.auth import get_current_user, require_role
from app.services.booking import create_ticket, get_ticket, get_tickets

router = APIRouter()

user_admin_annotated= Annotated[User, Depends(require_role(["admin"]))]

@router.get("/", response_model=List[TicketResponse])
def get_all_tickets(
    db: Session = Depends(get_db),
    user: dict = Depends(require_role(["admin"])),
    skip: int = 0,
    limit: int = 100
):
    return get_tickets(db, skip, limit)

@router.get("/me", response_model=List[TicketResponse])
def get_current_user_tickets(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tickets = (
        db.query(Ticket)
        .filter(Ticket.user_id == current_user["user_id"])
        .all()
    )
    
    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found for current user")

    return tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket_by_id(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if current_user["role"] != "admin" and ticket.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied: not your ticket")

    return ticket

@router.post("/buy", response_model=TicketResponse)
def buy_ticket(ticket_data: TicketCreate, current_user: Annotated[dict,  Depends(get_current_user)], db: Session = Depends(get_db)):
    try:
        return create_ticket(db, ticket_data, current_user["user_id"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket_by_id(
    ticket_id: int,
    updated_data: TicketCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_role(["admin"]))
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    for field, value in updated_data.dict().items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)
    return ticket

@router.delete("/{ticket_id}")
def delete_ticket_by_id(
    ticket_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_role(["admin"]))
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()
    return {"detail": f"Ticket {ticket_id} deleted successfully"}