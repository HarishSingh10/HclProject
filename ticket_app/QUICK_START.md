# ⚡ Quick Start Guide

Get the IT Support Assistant running in 5 minutes.

## 1️⃣ Prerequisites
- Python 3.8+
- FastAPI backend running on `http://localhost:8000`

## 2️⃣ Install & Run

```bash
# Navigate to project
cd ticket_app

# Create virtual environment
python -m venv venv

# Activate (Windows: venv\Scripts\activate)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

## 3️⃣ Open Browser
```
http://localhost:8501
```

## 4️⃣ Login with Demo Credentials

**User Account:**
- Email: `user@example.com`
- Password: `password123`

**Admin Account:**
- Email: `admin@example.com`
- Password: `admin123`

## 5️⃣ Explore Features

### 📝 Raise Ticket
1. Click "Raise Ticket" in navigation
2. Describe your issue
3. Select category and priority
4. Click "Submit Ticket"

### 🤖 View Suggestions
1. Click "View Suggestions"
2. Enter ticket ID or use last created
3. View AI recommendations
4. Mark as resolved if helpful

### 📊 Ticket Status
1. Click "Ticket Status"
2. View all your tickets
3. Filter by status
4. Update ticket status

### 📈 Admin Dashboard (Admin Only)
1. Login as admin
2. Click "Admin Dashboard"
3. View system statistics
4. Manage all tickets

---

## 🔧 Configuration

Edit `.streamlit/secrets.toml`:
```toml
backend_url = "http://localhost:8000"
```

---

## 📁 Project Structure

```
ticket_app/
├── app.py                    # Main app
├── requirements.txt          # Dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit config
│   └── secrets.toml         # API config
├── utils/
│   ├── api.py               # API client
│   └── auth.py              # Auth utilities
└── pages/
    ├── 1_Login.py           # Login
    ├── 2_Raise_Ticket.py    # Create ticket
    ├── 3_View_Suggestions.py # AI recommendations
    ├── 4_Ticket_Status.py   # Track tickets
    └── 5_Admin_Dashboard.py # Admin panel
```

---

## 🚀 Next Steps

1. ✅ App is running
2. ✅ You're logged in
3. 📝 Create a test ticket
4. 🤖 View recommendations
5. 📊 Check ticket status
6. 📈 View admin dashboard (if admin)

---

## 🆘 Troubleshooting

### "Cannot connect to backend"
- Ensure FastAPI backend is running on port 8000
- Check `backend_url` in `.streamlit/secrets.toml`

### "Login failed"
- Verify demo credentials
- Check backend is responding
- Check browser console for errors

### "Page not loading"
- Clear browser cache (Ctrl+Shift+Delete)
- Restart Streamlit app
- Check terminal for Python errors

---

## 📚 Full Documentation

- **Setup Guide:** `SETUP_GUIDE.md`
- **Backend Spec:** `BACKEND_SPEC.md`
- **Deployment:** `DEPLOYMENT.md`
- **README:** `README.md`

---

## 💡 Tips

- Use wide layout for better space
- Emojis help with visual navigation
- Color-coded status makes tracking easy
- Admin dashboard shows system health
- Session persists within browser tab

---

## 🎯 Demo Workflow

1. **Login** → Use user@example.com
2. **Raise Ticket** → Describe a network issue
3. **View Suggestions** → See AI recommendations
4. **Mark Resolved** → Complete the ticket
5. **Check Status** → View ticket history
6. **Admin View** → Login as admin to see dashboard

---

**Ready to go! 🚀**

For detailed information, see the full documentation files.
