from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
import datetime
import enum

class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"

class CategoryEnum(str, enum.Enum):
    Login = "Login"
    Network = "Network"
    Application = "Application"
    Access = "Access"

class PriorityEnum(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class StatusEnum(str, enum.Enum):
    Open = "Open"
    In_Progress = "In Progress"
    Resolved = "Resolved"
    Closed = "Closed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    department = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    tickets = relationship("Ticket", back_populates="user")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(Text)
    category = Column(Enum(CategoryEnum))
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.Low)
    status = Column(Enum(StatusEnum), default=StatusEnum.Open)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="tickets")
    resolution = relationship("Resolution", back_populates="ticket", uselist=False)

class Resolution(Base):
    __tablename__ = "resolutions"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    resolution_text = Column(Text)
    resolved_date = Column(DateTime, default=datetime.datetime.utcnow)

    ticket = relationship("Ticket", back_populates="resolution")
