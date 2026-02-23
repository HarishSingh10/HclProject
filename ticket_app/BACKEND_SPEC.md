# 📋 Backend API Specification

Complete API specification for the FastAPI backend that the frontend expects.

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints except `/login` require Bearer token in Authorization header:
```
Authorization: Bearer {access_token}
```

---

## Endpoints

### 1. POST /login
**Description:** Authenticate user and get access token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user_id": "user_123",
  "username": "John Doe",
  "role": "user"
}
```

**Error (401):**
```json
{
  "detail": "Invalid credentials"
}
```

---

### 2. POST /tickets
**Description:** Create a new support ticket

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
  "description": "Cannot connect to VPN",
  "category": "Network",
  "priority": "High"
}
```

**Response (201):**
```json
{
  "ticket_id": "TICKET-001",
  "status": "Open",
  "created_at": "2024-02-23T10:30:00Z"
}
```

**Error (400):**
```json
{
  "detail": "Invalid category"
}
```

---

### 3. GET /my-tickets
**Description:** Get all tickets for current user

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `status` (optional): Filter by status (Open, In Progress, Resolved)
- `category` (optional): Filter by category
- `limit` (optional): Number of tickets to return (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Response (200):**
```json
{
  "tickets": [
    {
      "id": "TICKET-001",
      "description": "Cannot connect to VPN",
      "category": "Network",
      "priority": "High",
      "status": "Open",
      "created_at": "2024-02-23T10:30:00Z",
      "updated_at": "2024-02-23T10:30:00Z"
    },
    {
      "id": "TICKET-002",
      "description": "Forgot password",
      "category": "Login",
      "priority": "Medium",
      "status": "Resolved",
      "created_at": "2024-02-22T15:45:00Z",
      "updated_at": "2024-02-23T09:00:00Z"
    }
  ],
  "total": 2
}
```

---

### 4. GET /recommend/{ticket_id}
**Description:** Get AI-powered recommendations for a ticket

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `ticket_id` (required): Ticket ID

**Response (200):**
```json
{
  "ticket": {
    "id": "TICKET-001",
    "description": "Cannot connect to VPN",
    "category": "Network",
    "priority": "High",
    "status": "Open"
  },
  "recommendations": [
    {
      "rank": 1,
      "resolution_text": "Check your VPN client version. Update to the latest version from the company portal.",
      "similarity_score": 0.95,
      "source": "Knowledge Base",
      "confidence": "High"
    },
    {
      "rank": 2,
      "resolution_text": "Restart your computer and try connecting again. Clear VPN cache if available.",
      "similarity_score": 0.87,
      "source": "Previous Solutions",
      "confidence": "High"
    },
    {
      "rank": 3,
      "resolution_text": "Contact IT Support if the issue persists. Provide your system details.",
      "similarity_score": 0.72,
      "source": "Support Guidelines",
      "confidence": "Medium"
    }
  ]
}
```

**Error (404):**
```json
{
  "detail": "Ticket not found"
}
```

---

### 5. PATCH /tickets/{ticket_id}
**Description:** Update ticket status

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Path Parameters:**
- `ticket_id` (required): Ticket ID

**Request:**
```json
{
  "status": "Resolved"
}
```

**Valid Status Values:**
- `Open`
- `In Progress`
- `Resolved`

**Response (200):**
```json
{
  "id": "TICKET-001",
  "status": "Resolved",
  "updated_at": "2024-02-23T11:00:00Z"
}
```

**Error (404):**
```json
{
  "detail": "Ticket not found"
}
```

---

### 6. GET /admin/stats
**Description:** Get admin dashboard statistics (Admin only)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "stats": {
    "total_tickets": 150,
    "open_tickets": 45,
    "in_progress_tickets": 30,
    "resolved_tickets": 75,
    "tickets_today": 5,
    "open_percentage": 30,
    "resolution_rate": 50,
    "avg_resolution_time": 4.5,
    "tickets_by_category": {
      "Network": 45,
      "Login": 30,
      "Application": 50,
      "Hardware": 20,
      "Other": 5
    },
    "status_distribution": {
      "Open": 45,
      "In Progress": 30,
      "Resolved": 75
    },
    "tickets_over_time": {
      "2024-02-20": 10,
      "2024-02-21": 15,
      "2024-02-22": 20,
      "2024-02-23": 5
    }
  }
}
```

**Error (403):**
```json
{
  "detail": "Admin access required"
}
```

---

### 7. GET /admin/tickets
**Description:** Get all tickets for admin view (Admin only)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `status` (optional): Filter by status
- `category` (optional): Filter by category
- `priority` (optional): Filter by priority
- `limit` (optional): Number of tickets (default: 100)
- `offset` (optional): Pagination offset (default: 0)

**Response (200):**
```json
{
  "tickets": [
    {
      "id": "TICKET-001",
      "user_id": "user_123",
      "user_name": "John Doe",
      "description": "Cannot connect to VPN",
      "category": "Network",
      "priority": "High",
      "status": "Open",
      "created_at": "2024-02-23T10:30:00Z",
      "updated_at": "2024-02-23T10:30:00Z"
    }
  ],
  "total": 150
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Data Models

### User
```python
{
  "id": str,
  "email": str,
  "username": str,
  "role": str,  # "user" or "admin"
  "created_at": datetime
}
```

### Ticket
```python
{
  "id": str,
  "user_id": str,
  "description": str,
  "category": str,  # Network, Login, Application, Hardware, Other
  "priority": str,  # Low, Medium, High
  "status": str,    # Open, In Progress, Resolved
  "created_at": datetime,
  "updated_at": datetime
}
```

### Recommendation
```python
{
  "rank": int,
  "resolution_text": str,
  "similarity_score": float,  # 0.0 to 1.0
  "source": str,
  "confidence": str  # Low, Medium, High
}
```

---

## Rate Limiting

Recommended rate limits:
- `/login`: 5 requests per minute per IP
- `/tickets`: 10 requests per minute per user
- `/recommend`: 20 requests per minute per user
- `/admin/*`: 30 requests per minute per admin

---

## CORS Configuration

Required CORS headers:
```
Access-Control-Allow-Origin: http://localhost:8501
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

---

## Example FastAPI Implementation

```python
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="IT Support API")
security = HTTPBearer()

# Models
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    user_id: str
    username: str
    role: str

class TicketCreate(BaseModel):
    description: str
    category: str
    priority: str

class TicketResponse(BaseModel):
    id: str
    description: str
    category: str
    priority: str
    status: str
    created_at: str
    updated_at: str

class TicketUpdate(BaseModel):
    status: str

# Endpoints
@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # Implement authentication logic
    # Validate email and password
    # Generate JWT token
    # Return user info and token
    pass

@app.post("/tickets")
async def create_ticket(
    ticket: TicketCreate,
    credentials: HTTPAuthCredentials = Depends(security)
):
    # Verify token
    # Create ticket in database
    # Return ticket_id
    pass

@app.get("/my-tickets")
async def get_user_tickets(
    credentials: HTTPAuthCredentials = Depends(security),
    status: Optional[str] = None,
    category: Optional[str] = None
):
    # Verify token
    # Get user from token
    # Query tickets for user
    # Apply filters
    # Return tickets
    pass

@app.get("/recommend/{ticket_id}")
async def get_recommendations(
    ticket_id: str,
    credentials: HTTPAuthCredentials = Depends(security)
):
    # Verify token
    # Get ticket
    # Run NLP model to find similar issues
    # Return recommendations
    pass

@app.patch("/tickets/{ticket_id}")
async def update_ticket(
    ticket_id: str,
    update: TicketUpdate,
    credentials: HTTPAuthCredentials = Depends(security)
):
    # Verify token
    # Update ticket status
    # Return updated ticket
    pass

@app.get("/admin/stats")
async def get_admin_stats(
    credentials: HTTPAuthCredentials = Depends(security)
):
    # Verify token and admin role
    # Calculate statistics
    # Return stats
    pass

@app.get("/admin/tickets")
async def get_admin_tickets(
    credentials: HTTPAuthCredentials = Depends(security),
    status: Optional[str] = None,
    category: Optional[str] = None
):
    # Verify token and admin role
    # Get all tickets
    # Apply filters
    # Return tickets
    pass
```

---

## Testing the API

### Using curl

```bash
# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Create ticket
curl -X POST http://localhost:8000/tickets \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description":"Issue","category":"Network","priority":"High"}'

# Get recommendations
curl -X GET http://localhost:8000/recommend/TICKET-001 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Using Postman

1. Import the API endpoints
2. Set `{{base_url}}` to `http://localhost:8000`
3. Set `{{token}}` after login
4. Test each endpoint

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- Similarity scores range from 0.0 to 1.0
- Ticket IDs are unique and immutable
- Status transitions: Open → In Progress → Resolved
- Admin endpoints require `role: "admin"`

---

**Last Updated:** February 23, 2024
