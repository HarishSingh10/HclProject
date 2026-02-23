from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

import models, schemas, auth
from database import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(
    current_admin=Depends(auth.get_current_active_admin),
    db: Session = Depends(get_db)
):
    users = db.query(models.User).all()
    return users

@router.get("/tickets", response_model=List[schemas.TicketResponse])
def get_all_tickets(
    # Only admins can access
    current_admin=Depends(auth.get_current_active_admin),
    db: Session = Depends(get_db)
):
    tickets = db.query(models.Ticket).all()
    return tickets

@router.post("/tickets", response_model=dict)
def admin_raise_ticket(
    user_id: int,
    ticket: schemas.TicketCreate,
    current_admin=Depends(auth.get_current_active_admin),
    db: Session = Depends(get_db)
):
    # Prepare the new ticket for a specific user
    db_ticket = models.Ticket(
        user_id=user_id,
        description=ticket.description,
        category=ticket.category,
        priority=ticket.priority
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    return {
        "ticket": schemas.TicketResponse.model_validate(db_ticket),
        "ai_resolution": ""
    }

@router.put("/tickets/{id}/status", response_model=schemas.TicketResponse)
def update_ticket_status(
    id: int,
    status: models.StatusEnum,
    current_admin=Depends(auth.get_current_active_admin),
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    ticket.status = status
    db.commit()
    db.refresh(ticket)
    return ticket

@router.post("/resolution", response_model=schemas.ResolutionResponse)
def add_resolution(
    resolution: schemas.ResolutionCreate,
    current_admin=Depends(auth.get_current_active_admin),
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == resolution.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    if ticket.resolution:
        raise HTTPException(status_code=400, detail="Ticket already has a resolution")
        
    db_res = models.Resolution(
        ticket_id=ticket.id,
        resolution_text=resolution.resolution_text
    )
    db.add(db_res)
    ticket.status = models.StatusEnum.Resolved
    db.commit()
    db.refresh(db_res)
    return db_res

@router.get("/analytics")
def get_analytics(
    current_admin=Depends(auth.get_current_active_admin),
    db: Session = Depends(get_db)
):
    total_tickets = db.query(models.Ticket).count()
    
    # Most common category
    common_category = db.query(
        models.Ticket.category, 
        func.count(models.Ticket.category).label("count")
    ).group_by(models.Ticket.category).order_by(func.count(models.Ticket.category).desc()).first()
    
    category_name = common_category.category.value if common_category else None
    
    # Average resolution time
    # Needs a join to get resolution_date - created_date
    resolved_tickets = db.query(models.Ticket, models.Resolution).join(
        models.Resolution, models.Ticket.id == models.Resolution.ticket_id
    ).all()
    
    avg_hours = 0
    if resolved_tickets:
        total_time = sum(
            (res.resolved_date - tkt.created_date).total_seconds() 
            for tkt, res in resolved_tickets
        )
        avg_hours = (total_time / len(resolved_tickets)) / 3600
        
    return {
        "total_tickets": total_tickets,
        "most_common_category": category_name,
        "average_resolution_time_hours": round(avg_hours, 2)
    }
