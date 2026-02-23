from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas, auth
from database import get_db
from nlp_engine import generate_ai_resolution

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=dict)
def raise_ticket(
    ticket: schemas.TicketCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Prepare the new ticket
    db_ticket = models.Ticket(
        user_id=current_user.id,
        description=ticket.description,
        category=ticket.category,
        priority=ticket.priority
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    # NLP Engine Processing
    historical_resolutions = db.query(models.Resolution).all()
    
    historical_tickets_data = []
    # Join tickets and resolutions where ticket is resolved
    for res in historical_resolutions:
        ticket_ref = db.query(models.Ticket).filter(models.Ticket.id == res.ticket_id).first()
        if ticket_ref:
            historical_tickets_data.append({
                "id": ticket_ref.id,
                "description": ticket_ref.description,
                "resolution_text": res.resolution_text
            })
            
    # Generate an AI-provided resolution right away
    ai_resolution_text = generate_ai_resolution(
        ticket.description,
        historical_tickets_data
    )
    
    # Save the AI resolution so it permanently appears in the ticket history!
    new_res = models.Resolution(
        ticket_id=db_ticket.id,
        resolution_text=ai_resolution_text
    )
    db.add(new_res)
    # the ticket is kept Open intentionally so it's tracked, but they have an AI suggestion applied
    db.commit()
    db.refresh(db_ticket)
    
    return {
        "ticket": schemas.TicketResponse.model_validate(db_ticket),
        "ai_resolution": ai_resolution_text
    }

@router.get("/user/{user_id}", response_model=List[schemas.TicketResponse])
def get_user_tickets(
    user_id: int, 
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id and current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not authorized to view these tickets")
        
    tickets = db.query(models.Ticket).filter(models.Ticket.user_id == user_id).all()
    return tickets

@router.put("/{id}/resolve", response_model=schemas.TicketResponse)
def resolve_ticket(
    id: int,
    resolution_text: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    if ticket.user_id != current_user.id and current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not authorized to resolve this ticket")

    if ticket.status == models.StatusEnum.Resolved:
        raise HTTPException(status_code=400, detail="Ticket already resolved")

    ticket.status = models.StatusEnum.Resolved
    
    # Check if a resolution exists, if not create one OR update current AI one with user one
    if not ticket.resolution:
        new_res = models.Resolution(
            ticket_id=ticket.id,
            resolution_text=resolution_text
        )
        db.add(new_res)
    else:
        ticket.resolution.resolution_text = resolution_text
        
    db.commit()
    db.refresh(ticket)
    return ticket

@router.put("/{id}/escalate", response_model=schemas.TicketResponse)
def escalate_ticket(
    id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    if ticket.user_id != current_user.id and current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not authorized to escalate this ticket")

    ticket.priority = models.PriorityEnum.High
    ticket.status = models.StatusEnum.Open
    
    escalation_message = "🚧 [ESCALATED] User issue is not resolved. Send this ticket to Data Engineer."
    if not ticket.resolution:
        new_res = models.Resolution(
            ticket_id=ticket.id,
            resolution_text=escalation_message
        )
        db.add(new_res)
    else:
        ticket.resolution.resolution_text = escalation_message + "\n\nPrevious notes: " + ticket.resolution.resolution_text
        
    db.commit()
    db.refresh(ticket)
    return ticket
