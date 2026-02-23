from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import RoleEnum, CategoryEnum, PriorityEnum, StatusEnum

# Users
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.user
    department: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum
    department: str
    created_at: datetime

    class Config:
        from_attributes = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Resolutions
class ResolutionCreate(BaseModel):
    ticket_id: int
    resolution_text: str

class ResolutionResponse(BaseModel):
    id: int
    ticket_id: int
    resolution_text: str
    resolved_date: datetime

    class Config:
        from_attributes = True

# Tickets
class TicketCreate(BaseModel):
    description: str
    category: CategoryEnum
    priority: PriorityEnum = PriorityEnum.Low

class TicketResponse(BaseModel):
    id: int
    user_id: int
    description: str
    category: CategoryEnum
    priority: PriorityEnum
    status: StatusEnum
    created_date: datetime
    resolution: Optional[ResolutionResponse] = None

    class Config:
        from_attributes = True

# NLP similarity response
class NLPSimilarityResponse(BaseModel):
    ticket_id: int
    similarity_score: float
    description: str
    resolution_text: str
