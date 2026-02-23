"""
FastAPI Backend - Main Application
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json
import os

app = FastAPI(title="IT Ticket Resolution System API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class User(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class Ticket(BaseModel):
    description: str
    category: str
    priority: str

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    resolution: Optional[str] = None

class Resolution(BaseModel):
    category: str
    issue: str
    resolution: str

# Database paths
DB_PATH = "../data"
os.makedirs(DB_PATH, exist_ok=True)

USERS_FILE = f"{DB_PATH}/users.json"
TICKETS_FILE = f"{DB_PATH}/tickets.json"
RESOLUTIONS_FILE = f"{DB_PATH}/resolutions.json"

# Initialize database files
def init_db():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({
                "admin": {"password": "admin123", "type": "admin", "email": "admin@company.com"},
                "user": {"password": "user123", "type": "user", "email": "user@company.com"}
            }, f)
    
    if not os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(RESOLUTIONS_FILE):
        with open(RESOLUTIONS_FILE, 'w') as f:
            json.dump([], f)

init_db()

# Authentication endpoints
@app.post("/api/auth/login")
async def login(user: User):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    if user.username in users and users[user.username]['password'] == user.password:
        return {
            "success": True,
            "user_type": users[user.username]['type'],
            "username": user.username
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/register")
async def register(user: User):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    users[user.username] = {
        "password": user.password,
        "type": "user",
        "email": user.email
    }
    
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return {"success": True, "message": "User registered successfully"}

# Ticket endpoints
@app.post("/api/tickets")
async def create_ticket(ticket: Ticket, username: str):
    with open(TICKETS_FILE, 'r') as f:
        tickets = json.load(f)
    
    ticket_id = max([t['id'] for t in tickets], default=0) + 1
    
    new_ticket = {
        "id": ticket_id,
        "username": username,
        "description": ticket.description,
        "category": ticket.category,
        "priority": ticket.priority,
        "status": "Open",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "resolution": None
    }
    
    tickets.append(new_ticket)
    
    with open(TICKETS_FILE, 'w') as f:
        json.dump(tickets, f, indent=2)
    
    return {"success": True, "ticket_id": ticket_id, "ticket": new_ticket}

@app.get("/api/tickets")
async def get_tickets(username: Optional[str] = None):
    with open(TICKETS_FILE, 'r') as f:
        tickets = json.load(f)
    
    if username:
        tickets = [t for t in tickets if t['username'] == username]
    
    return {"tickets": tickets}

@app.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    with open(TICKETS_FILE, 'r') as f:
        tickets = json.load(f)
    
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return ticket

@app.put("/api/tickets/{ticket_id}")
async def update_ticket(ticket_id: int, update: TicketUpdate):
    with open(TICKETS_FILE, 'r') as f:
        tickets = json.load(f)
    
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if update.status:
        ticket['status'] = update.status
    if update.resolution:
        ticket['resolution'] = update.resolution
    
    ticket['updated_at'] = datetime.now().isoformat()
    
    with open(TICKETS_FILE, 'w') as f:
        json.dump(tickets, f, indent=2)
    
    return {"success": True, "ticket": ticket}

# Resolution endpoints
@app.get("/api/resolutions")
async def get_resolutions():
    with open(RESOLUTIONS_FILE, 'r') as f:
        resolutions = json.load(f)
    return {"resolutions": resolutions}

@app.post("/api/resolutions")
async def add_resolution(resolution: Resolution):
    with open(RESOLUTIONS_FILE, 'r') as f:
        resolutions = json.load(f)
    
    resolutions.append(resolution.dict())
    
    with open(RESOLUTIONS_FILE, 'w') as f:
        json.dump(resolutions, f, indent=2)
    
    return {"success": True, "message": "Resolution added"}

# Analytics endpoints
@app.get("/api/analytics/stats")
async def get_stats():
    with open(TICKETS_FILE, 'r') as f:
        tickets = json.load(f)
    
    stats = {
        "total": len(tickets),
        "open": len([t for t in tickets if t['status'] == 'Open']),
        "in_progress": len([t for t in tickets if t['status'] == 'In Progress']),
        "resolved": len([t for t in tickets if t['status'] == 'Resolved']),
        "closed": len([t for t in tickets if t['status'] == 'Closed'])
    }
    
    return stats

@app.get("/")
async def root():
    return {"message": "IT Ticket Resolution System API", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
