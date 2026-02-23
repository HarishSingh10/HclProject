# 🚀 Setup Guide - IT Support Assistant

Complete step-by-step guide to get the application running.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)
- A FastAPI backend running (see Backend Setup section)

## Step 1: Environment Setup

### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## Step 2: Install Dependencies

```bash
# Navigate to project directory
cd ticket_app

# Install required packages
pip install -r requirements.txt
```

### What gets installed:
- **streamlit**: Web framework for the UI
- **requests**: HTTP client for API calls
- **pandas**: Data manipulation and tables
- **streamlit-option-menu**: Navigation menu
- **python-dotenv**: Environment variable management

## Step 3: Configure Backend URL

Edit `.streamlit/secrets.toml`:

```toml
# Backend API Configuration
backend_url = "http://localhost:8000"
```

**For different environments:**
- Local: `http://localhost:8000`
- Remote: `https://api.example.com`
- Docker: `http://backend:8000`

## Step 4: Run the Application

```bash
streamlit run app.py
```

The app will:
1. Start a local server
2. Open in your default browser at `http://localhost:8501`
3. Show the login page

## Step 5: Test with Demo Credentials

### User Account
- Email: `user@example.com`
- Password: `password123`

### Admin Account
- Email: `admin@example.com`
- Password: `admin123`

## Backend Setup (FastAPI)

The frontend requires a FastAPI backend. Here's the minimal setup:

### Required Endpoints

```python
# FastAPI backend example
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
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
    user_id: str

class RecommendationResponse(BaseModel):
    ticket: dict
    recommendations: List[dict]

class AdminStatsResponse(BaseModel):
    stats: dict

# Endpoints
@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # Implement authentication
    # Return token, user_id, username, role
    pass

@app.post("/tickets", response_model=dict)
async def create_ticket(ticket: TicketCreate, token: str = Depends(security)):
    # Create ticket
    # Return ticket_id
    pass

@app.get("/my-tickets")
async def get_user_tickets(token: str = Depends(security)):
    # Return user's tickets
    pass

@app.get("/recommend/{ticket_id}")
async def get_recommendations(ticket_id: str, token: str = Depends(security)):
    # Return AI recommendations
    pass

@app.patch("/tickets/{ticket_id}")
async def update_ticket(ticket_id: str, status: str, token: str = Depends(security)):
    # Update ticket status
    pass

@app.get("/admin/stats")
async def get_admin_stats(token: str = Depends(security)):
    # Return admin statistics
    pass

@app.get("/admin/tickets")
async def get_admin_tickets(token: str = Depends(security)):
    # Return all tickets for admin
    pass
```

### Running Backend Locally

```bash
# Install FastAPI
pip install fastapi uvicorn

# Run backend
uvicorn main:app --reload --port 8000
```

## Troubleshooting

### Issue: "Cannot connect to backend"

**Solution:**
1. Verify backend is running: `http://localhost:8000/docs`
2. Check `backend_url` in `.streamlit/secrets.toml`
3. Ensure no firewall blocking port 8000

### Issue: "Login failed"

**Solution:**
1. Verify backend is responding
2. Check demo credentials are correct
3. Check backend logs for errors
4. Ensure backend has user data

### Issue: "Page not found"

**Solution:**
1. Clear browser cache: Ctrl+Shift+Delete
2. Restart Streamlit: Stop and run `streamlit run app.py` again
3. Check for Python errors in terminal

### Issue: "Session lost after refresh"

**Solution:**
1. This is normal - Streamlit resets on refresh
2. Use browser back button instead of refresh
3. Session persists within the same browser tab

### Issue: "API returns 401 Unauthorized"

**Solution:**
1. Token may have expired - log in again
2. Check backend token validation
3. Verify auth header format in `utils/api.py`

## Development Tips

### Enable Debug Mode
Add to `.streamlit/config.toml`:
```toml
[logger]
level = "debug"
```

### View API Requests
Add to `utils/api.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test API Endpoints
Use Postman or curl:
```bash
# Test login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Hot Reload
Streamlit automatically reloads when you save files. Just edit and save!

## Production Deployment

### Using Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repository
5. Set secrets in cloud dashboard:
   ```
   backend_url = "https://api.example.com"
   ```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t ticket-app .
docker run -p 8501:8501 -e backend_url=http://backend:8000 ticket-app
```

### Using Heroku

1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set backend_url=https://your-backend.com
   git push heroku main
   ```

## Performance Optimization

### Caching API Calls
```python
@st.cache_data(ttl=300)
def get_cached_data():
    return api_client.get_user_tickets(token)
```

### Reducing Re-renders
Use `st.session_state` to persist data across reruns.

### Lazy Loading
Load data only when needed, not on page load.

## Security Checklist

- ✅ Never commit `.streamlit/secrets.toml` with real credentials
- ✅ Use HTTPS in production
- ✅ Validate all user inputs
- ✅ Store tokens securely
- ✅ Implement CORS properly on backend
- ✅ Use environment variables for sensitive data
- ✅ Implement rate limiting on backend
- ✅ Log security events

## Next Steps

1. ✅ Backend is running
2. ✅ Frontend is running
3. ✅ You can log in with demo credentials
4. ✅ Create a test ticket
5. ✅ View recommendations
6. ✅ Check admin dashboard (if admin)

## Support Resources

- Streamlit Docs: https://docs.streamlit.io
- FastAPI Docs: https://fastapi.tiangolo.com
- Python Requests: https://requests.readthedocs.io
- Pandas Docs: https://pandas.pydata.org/docs

---

**Happy coding! 🚀**
