# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                              │
│                  (http://localhost:8501)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              STREAMLIT FRONTEND (Python)                     │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ app.py - Main Application                            │   │
│  │ • Page configuration                                 │   │
│  │ • Session state management                           │   │
│  │ • Sidebar navigation                                 │   │
│  │ • Multi-page routing                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Pages (Multi-page Application)                       │   │
│  │ ├─ 1_Login.py - Authentication                       │   │
│  │ ├─ 2_Raise_Ticket.py - Create tickets               │   │
│  │ ├─ 3_View_Suggestions.py - AI recommendations       │   │
│  │ ├─ 4_Ticket_Status.py - Track tickets               │   │
│  │ └─ 5_Admin_Dashboard.py - Admin analytics           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Utils (Utilities)                                    │   │
│  │ ├─ api.py - API Client                              │   │
│  │ │  • APIClient class                                │   │
│  │ │  • HTTP requests                                  │   │
│  │ │  • Error handling                                 │   │
│  │ │  • Token management                               │   │
│  │ └─ auth.py - Authentication                         │   │
│  │    • Login/logout                                   │   │
│  │    • Role-based access                              │   │
│  │    • Session helpers                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Configuration                                        │   │
│  │ ├─ .streamlit/config.toml - Streamlit settings      │   │
│  │ └─ .streamlit/secrets.toml - API configuration      │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ REST API (JSON)
                         │ HTTP/HTTPS
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND (Python)                        │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ API Endpoints                                        │   │
│  │ ├─ POST /login - Authentication                     │   │
│  │ ├─ POST /tickets - Create ticket                    │   │
│  │ ├─ GET /my-tickets - Get user tickets               │   │
│  │ ├─ GET /recommend/{id} - Get recommendations        │   │
│  │ ├─ PATCH /tickets/{id} - Update status              │   │
│  │ ├─ GET /admin/stats - Admin statistics              │   │
│  │ └─ GET /admin/tickets - All tickets                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Business Logic                                       │   │
│  │ ├─ Authentication & JWT                             │   │
│  │ ├─ Ticket management                                │   │
│  │ ├─ NLP recommendations                              │   │
│  │ └─ Analytics & reporting                            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Services                                             │   │
│  │ ├─ User service                                      │   │
│  │ ├─ Ticket service                                    │   │
│  │ ├─ Recommendation service (NLP)                      │   │
│  │ └─ Analytics service                                │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ SQL Queries
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              DATABASE (PostgreSQL)                           │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Tables                                               │   │
│  │ ├─ users                                             │   │
│  │ │  ├─ id, email, password_hash, username, role      │   │
│  │ │  └─ created_at, updated_at                        │   │
│  │ ├─ tickets                                           │   │
│  │ │  ├─ id, user_id, description, category, priority  │   │
│  │ │  ├─ status, created_at, updated_at                │   │
│  │ │  └─ resolved_at                                   │   │
│  │ └─ recommendations                                   │   │
│  │    ├─ id, ticket_id, resolution_text                │   │
│  │    ├─ similarity_score, source                       │   │
│  │    └─ created_at                                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Indexes                                              │   │
│  │ ├─ users.email (unique)                             │   │
│  │ ├─ tickets.user_id                                  │   │
│  │ ├─ tickets.status                                   │   │
│  │ └─ recommendations.ticket_id                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Authentication Flow
```
User Input (Email/Password)
    ↓
Streamlit Form
    ↓
API Client (utils/api.py)
    ↓
POST /login
    ↓
Backend Validation
    ↓
Database Query (users table)
    ↓
JWT Token Generation
    ↓
Response with Token
    ↓
Store in Session State
    ↓
Redirect to Dashboard
```

### Ticket Creation Flow
```
User Input (Description, Category, Priority)
    ↓
Streamlit Form Validation
    ↓
API Client (utils/api.py)
    ↓
POST /tickets (with auth token)
    ↓
Backend Validation
    ↓
Database Insert (tickets table)
    ↓
Return Ticket ID
    ↓
Streamlit Success Message
    ↓
Display Ticket Info
    ↓
Offer View Suggestions
```

### Recommendation Flow
```
Ticket ID Input
    ↓
API Client (utils/api.py)
    ↓
GET /recommend/{ticket_id}
    ↓
Backend Retrieves Ticket
    ↓
NLP Model Processes Description
    ↓
Find Similar Issues (Knowledge Base)
    ↓
Calculate Similarity Scores
    ↓
Rank by Score
    ↓
Return Top 3
    ↓
Streamlit Display
    ↓
Show with Confidence Levels
```

---

## Component Interaction

### Frontend Components
```
app.py (Main)
├── Sidebar
│   ├── User Info
│   ├── Role Badge
│   └── Logout Button
├── Navigation Menu
│   ├── Login
│   ├── Raise Ticket
│   ├── View Suggestions
│   ├── Ticket Status
│   └── Admin Dashboard (if admin)
└── Page Router
    └── Switch to selected page
```

### API Client Architecture
```
APIClient (utils/api.py)
├── __init__(base_url)
├── _get_headers(token)
├── _handle_response(response)
├── login(email, password)
├── create_ticket(description, category, priority, token)
├── get_recommendations(ticket_id, token)
├── get_user_tickets(token)
├── update_ticket_status(ticket_id, status, token)
├── get_admin_stats(token)
└── get_admin_tickets(token)
```

### Authentication Flow
```
Session State
├── logged_in (bool)
├── user_id (str)
├── username (str)
├── role (str)
├── auth_token (str)
└── last_ticket_id (str)

Auth Utilities (utils/auth.py)
├── require_login()
├── require_admin()
├── set_user_session()
└── clear_user_session()
```

---

## Page Architecture

### 1_Login.py
```
Centered Layout
├── Title
├── Form
│   ├── Email Input
│   ├── Password Input
│   └── Submit Button
├── Error Handling
├── Loading Spinner
└── Demo Credentials
```

### 2_Raise_Ticket.py
```
Two-Column Layout
├── Left Column (Form)
│   ├── Description Input
│   ├── Category Select
│   ├── Priority Select
│   ├── Submit Button
│   └── Clear Button
└── Right Column (Tips)
    └── Help Text
```

### 3_View_Suggestions.py
```
Main Layout
├── Ticket ID Input
├── Ticket Info Metrics
├── Recommendations
│   ├── Expander 1 (Best Match)
│   ├── Expander 2
│   └── Expander 3
├── Action Buttons
│   ├── Mark as Resolved
│   ├── New Ticket
│   └── View All Tickets
└── Loading States
```

### 4_Ticket_Status.py
```
Main Layout
├── Metrics Row
│   ├── Total Tickets
│   ├── Open
│   ├── In Progress
│   └── Resolved
├── Filter Section
│   └── Status Filter
├── Tickets Table
├── Ticket Details
│   ├── Info Metrics
│   ├── Description
│   ├── Status Update
│   └── Action Buttons
└── Loading States
```

### 5_Admin_Dashboard.py
```
Main Layout
├── Metrics Row
│   ├── Total Tickets
│   ├── Open Tickets
│   ├── Resolved Tickets
│   └── Avg Resolution Time
├── Charts Row
│   ├── Bar Chart (by Category)
│   ├── Pie Chart (Status Distribution)
│   └── Line Chart (Over Time)
├── Filter Section
│   ├── Status Filter
│   ├── Category Filter
│   └── Priority Filter
├── Tickets Table
├── Ticket Details
│   ├── Info Metrics
│   ├── Description
│   ├── Status Update
│   └── Refresh Button
└── Loading States
```

---

## Deployment Architecture

### Local Development
```
Developer Machine
├── Python Virtual Environment
├── Streamlit Server (port 8501)
├── FastAPI Backend (port 8000)
└── PostgreSQL Database (port 5432)
```

### Docker Deployment
```
Docker Host
├── Frontend Container
│   └── Streamlit App (port 8501)
├── Backend Container
│   └── FastAPI App (port 8000)
└── Database Container
    └── PostgreSQL (port 5432)
```

### Cloud Deployment (Streamlit Cloud)
```
Streamlit Cloud
├── Frontend (Streamlit)
└── Backend (External API)
    └── Database (External)
```

### AWS Deployment
```
AWS Infrastructure
├── App Runner / ECS
│   ├── Frontend (Streamlit)
│   └── Backend (FastAPI)
├── RDS
│   └── PostgreSQL Database
├── ALB
│   └── Load Balancer
└── CloudWatch
    └── Monitoring & Logging
```

---

## Security Architecture

```
Security Layers
├── Authentication
│   ├── JWT Tokens
│   ├── Password Hashing
│   └── Session Management
├── Authorization
│   ├── Role-Based Access Control
│   ├── Protected Pages
│   └── Admin-Only Endpoints
├── Data Protection
│   ├── HTTPS/TLS
│   ├── CORS Configuration
│   └── Input Validation
└── Infrastructure
    ├── Firewall Rules
    ├── VPC Configuration
    └── Security Groups
```

---

## Performance Architecture

```
Performance Optimization
├── Frontend
│   ├── Lazy Loading
│   ├── Caching
│   └── Efficient Rendering
├── API
│   ├── Connection Pooling
│   ├── Request Batching
│   └── Response Compression
├── Database
│   ├── Indexing
│   ├── Query Optimization
│   └── Connection Pooling
└── Infrastructure
    ├── CDN
    ├── Load Balancing
    └── Auto-Scaling
```

---

## Monitoring Architecture

```
Monitoring Stack
├── Application Monitoring
│   ├── Error Tracking (Sentry)
│   ├── Performance Monitoring (New Relic)
│   └── User Analytics
├── Infrastructure Monitoring
│   ├── CPU/Memory Usage
│   ├── Disk Usage
│   └── Network Usage
├── Logging
│   ├── Application Logs
│   ├── Access Logs
│   └── Error Logs
└── Alerting
    ├── Error Rate Alerts
    ├── Performance Alerts
    └── Uptime Alerts
```

---

## Technology Stack

```
Frontend
├── Streamlit (Web Framework)
├── Pandas (Data Manipulation)
├── Requests (HTTP Client)
└── Streamlit Option Menu (Navigation)

Backend
├── FastAPI (API Framework)
├── SQLAlchemy (ORM)
├── Pydantic (Data Validation)
└── JWT (Authentication)

Database
├── PostgreSQL (Primary)
├── Redis (Caching)
└── Elasticsearch (Search)

Deployment
├── Docker (Containerization)
├── Kubernetes (Orchestration)
├── Streamlit Cloud (Hosting)
└── AWS (Infrastructure)

Monitoring
├── Sentry (Error Tracking)
├── New Relic (APM)
├── CloudWatch (Logging)
└── Prometheus (Metrics)
```

---

**Last Updated:** February 23, 2024
