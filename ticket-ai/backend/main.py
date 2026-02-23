from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import users, tickets, admin

# Create tables logic
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IT Ticket Resolution AI")

# Set up CORS middleware to allow Streamlit frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to IT Ticket Resolution AI"}
