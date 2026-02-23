# 🛠️ IT Support Assistant - Streamlit Frontend

A professional, production-ready Streamlit application for IT ticket resolution with AI-powered suggestions. Built with role-based access control, multi-page navigation, and a modern UI.

## ✨ Features

- **🔐 Authentication & Authorization**
  - Secure login with JWT tokens
  - Role-based access control (User/Admin)
  - Session state management
  - Protected pages

- **📝 Ticket Management**
  - Create support tickets with category and priority
  - View ticket status and history
  - Real-time ticket tracking
  - Status filtering and search

- **🤖 AI-Powered Recommendations**
  - Get intelligent solutions for your issues
  - Similarity scoring for recommendations
  - Confidence-based ranking
  - Multiple solution suggestions

- **📊 Admin Dashboard**
  - System-wide analytics
  - Ticket statistics and metrics
  - Category and status distribution charts
  - Bulk ticket management
  - Advanced filtering options

- **🎨 Professional UI**
  - Clean, modern design
  - Responsive layout
  - Intuitive navigation
  - Color-coded status indicators
  - Loading spinners and feedback messages

## 📋 Project Structure

```
ticket_app/
├── app.py                          # Main app entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   ├── config.toml                # Streamlit configuration
│   └── secrets.toml               # API configuration
├── utils/
│   ├── api.py                     # API client for backend calls
│   └── auth.py                    # Authentication utilities
└── pages/
    ├── 1_Login.py                 # Login page
    ├── 2_Raise_Ticket.py          # Create ticket page
    ├── 3_View_Suggestions.py      # AI recommendations page
    ├── 4_Ticket_Status.py         # Ticket tracking page
    └── 5_Admin_Dashboard.py       # Admin analytics page
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda
- FastAPI backend running (see Backend Setup)

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd ticket_app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure backend URL:**
   Edit `.streamlit/secrets.toml`:
   ```toml
   backend_url = "http://localhost:8000"
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

The app will open at `http://localhost:8501`

## 🔑 Demo Credentials

**Regular User:**
- Email: `user@example.com`
- Password: `password123`

**Admin User:**
- Email: `admin@example.com`
- Password: `admin123`

## 📖 Page Guide

### 1️⃣ Login Page (`1_Login.py`)
- Centered login form
- Email and password input
- Error handling with user feedback
- Demo credentials display

### 2️⃣ Raise Ticket Page (`2_Raise_Ticket.py`)
- Create new support tickets
- Select category (Network, Login, Application, Hardware, Other)
- Set priority level (Low, Medium, High)
- Detailed description input
- Tips sidebar for better ticket writing
- Immediate redirect to suggestions

### 3️⃣ View Suggestions Page (`3_View_Suggestions.py`)
- AI-powered solution recommendations
- Top 3 suggestions with similarity scores
- Confidence-based color coding
- Mark tickets as resolved
- Quick navigation to other pages

### 4️⃣ Ticket Status Page (`4_Ticket_Status.py`)
- View all user tickets
- Filter by status (Open, In Progress, Resolved)
- Key metrics display
- Detailed ticket information
- Update ticket status
- Quick access to suggestions

### 5️⃣ Admin Dashboard (`5_Admin_Dashboard.py`)
- System-wide statistics
- Key performance metrics
- Analytics charts:
  - Tickets by category (bar chart)
  - Status distribution (pie chart)
  - Tickets over time (line chart)
- Advanced ticket filtering
- Bulk ticket management
- Admin-only access

## 🔌 API Integration

The app communicates with a FastAPI backend via REST APIs:

### Required Endpoints

```
POST   /login                    # User authentication
POST   /tickets                  # Create ticket
GET    /my-tickets              # Get user tickets
GET    /recommend/{ticket_id}   # Get AI recommendations
PATCH  /tickets/{id}            # Update ticket status
GET    /admin/stats             # Admin statistics
GET    /admin/tickets           # All tickets (admin)
```

### API Client (`utils/api.py`)

Centralized API client with:
- Automatic error handling
- Auth token management
- Request/response validation
- Connection error handling
- Timeout management

## 🔐 Authentication & Session Management

### Session State Variables

```python
st.session_state.logged_in      # Boolean: user logged in
st.session_state.user_id        # String: user ID
st.session_state.username       # String: username
st.session_state.role           # String: "user" or "admin"
st.session_state.auth_token     # String: JWT token
```

### Protected Pages

Use `require_login()` for user-only pages:
```python
from utils.auth import require_login
require_login()
```

Use `require_admin()` for admin-only pages:
```python
from utils.auth import require_admin
require_admin()
```

## 🎨 UI Components

### Metrics Display
```python
st.metric("Label", value, delta="optional")
```

### Status Color Coding
- 🔴 Open
- 🟠 In Progress
- 🟢 Resolved

### Cards & Containers
```python
with st.container():
    # Card content
```

### Loading States
```python
with st.spinner("Loading..."):
    # API call
```

## ⚙️ Configuration

### Backend URL
Edit `.streamlit/secrets.toml`:
```toml
backend_url = "http://localhost:8000"
```

### Streamlit Settings
Edit `.streamlit/config.toml`:
- Theme colors
- Font settings
- Server configuration
- Logger level

## 🐛 Error Handling

The app includes comprehensive error handling:
- API connection errors
- Authentication failures
- Invalid responses
- Network timeouts
- User-friendly error messages

## 📱 Responsive Design

- Wide layout mode for better space utilization
- Multi-column layouts for content organization
- Mobile-friendly components
- Adaptive spacing and sizing

## 🎯 Best Practices Implemented

✅ Session state management
✅ Role-based access control
✅ Modular code structure
✅ Centralized API client
✅ Error handling and validation
✅ Loading states and feedback
✅ Professional UI/UX
✅ Security best practices
✅ Code comments and documentation
✅ Reusable utility functions

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

1. **Using Streamlit Cloud:**
   - Push code to GitHub
   - Connect to Streamlit Cloud
   - Set secrets in cloud dashboard

2. **Using Docker:**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["streamlit", "run", "app.py"]
   ```

3. **Using Heroku/AWS/GCP:**
   - Set environment variables
   - Configure backend URL
   - Deploy container

## 📝 Environment Variables

Set in `.streamlit/secrets.toml` or environment:
- `backend_url`: FastAPI backend URL (default: http://localhost:8000)

## 🤝 Contributing

1. Follow the existing code structure
2. Add comments for complex logic
3. Test all pages before committing
4. Update README for new features

## 📄 License

This project is provided as-is for hackathon and educational purposes.

## 🆘 Troubleshooting

### Backend Connection Error
- Ensure FastAPI backend is running
- Check `backend_url` in `.streamlit/secrets.toml`
- Verify network connectivity

### Login Issues
- Check demo credentials
- Verify backend is responding
- Check browser console for errors

### Page Not Loading
- Clear browser cache
- Restart Streamlit app
- Check for Python errors in terminal

### Session Lost
- Browser cookies may be disabled
- Check session state in browser dev tools
- Ensure backend token is valid

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API response in browser dev tools
3. Check Streamlit logs in terminal
4. Verify backend is running and accessible

---

**Built with ❤️ for IT Support Excellence**
