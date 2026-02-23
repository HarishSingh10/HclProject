"""
Utility functions for data management
"""
import json
import os
from datetime import datetime

# Data files
TICKETS_FILE = 'tickets.json'
RESOLUTIONS_FILE = 'resolutions.json'
USERS_FILE = 'users.json'

def init_data_files():
    """Initialize data files if they don't exist"""
    if not os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(RESOLUTIONS_FILE):
        with open(RESOLUTIONS_FILE, 'w') as f:
            json.dump([
                {
                    "category": "Network",
                    "issue": "Cannot connect to WiFi",
                    "resolution": "1. Restart your router by unplugging it for 30 seconds\n2. Forget the WiFi network on your device\n3. Reconnect by entering the password again\n4. If issue persists, check if other devices can connect"
                },
                {
                    "category": "Network",
                    "issue": "Slow internet connection",
                    "resolution": "1. Run a speed test to confirm slow speeds\n2. Restart your router\n3. Check for bandwidth-heavy applications\n4. Move closer to the router or use ethernet cable"
                },
                {
                    "category": "Hardware",
                    "issue": "Laptop not charging",
                    "resolution": "1. Check if power adapter LED is on\n2. Inspect charging cable for damage\n3. Try a different power outlet\n4. Remove battery and reconnect (if removable)\n5. Contact IT if issue persists"
                },
                {
                    "category": "Hardware",
                    "issue": "Keyboard not working",
                    "resolution": "1. Check if keyboard is properly connected\n2. Try different USB port\n3. Restart your computer\n4. Update keyboard drivers\n5. Test with external keyboard"
                },
                {
                    "category": "Software",
                    "issue": "Application crashes",
                    "resolution": "1. Close and restart the application\n2. Clear application cache and temporary files\n3. Check for software updates\n4. Reinstall the application\n5. Check system requirements"
                },
                {
                    "category": "Software",
                    "issue": "Cannot install software",
                    "resolution": "1. Check if you have admin rights\n2. Verify system requirements\n3. Disable antivirus temporarily\n4. Clear Windows Update cache\n5. Contact IT for installation assistance"
                },
                {
                    "category": "Access",
                    "issue": "Forgot password",
                    "resolution": "1. Use 'Forgot Password' link on login page\n2. Check email for reset link\n3. Contact IT helpdesk for manual reset\n4. Verify your identity with security questions"
                },
                {
                    "category": "Access",
                    "issue": "Account locked",
                    "resolution": "1. Wait 30 minutes for automatic unlock\n2. Contact IT helpdesk for immediate unlock\n3. Verify you're using correct credentials\n4. Check if account needs reactivation"
                },
                {
                    "category": "Other",
                    "issue": "Printer not working",
                    "resolution": "1. Check if printer is powered on\n2. Verify printer connection (USB/Network)\n3. Clear print queue\n4. Restart print spooler service\n5. Reinstall printer drivers"
                }
            ], f)
    
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({
                "admin": {"password": "admin123", "type": "admin", "email": "admin@company.com"},
                "user": {"password": "user123", "type": "user", "email": "user@company.com"}
            }, f)

def load_tickets():
    """Load tickets from JSON file"""
    with open(TICKETS_FILE, 'r') as f:
        return json.load(f)

def save_tickets(tickets):
    """Save tickets to JSON file"""
    with open(TICKETS_FILE, 'w') as f:
        json.dump(tickets, f, indent=2)

def load_resolutions():
    """Load resolutions from JSON file"""
    with open(RESOLUTIONS_FILE, 'r') as f:
        return json.load(f)

def save_resolutions(resolutions):
    """Save resolutions to JSON file"""
    with open(RESOLUTIONS_FILE, 'w') as f:
        json.dump(resolutions, f, indent=2)

def load_users():
    """Load users from JSON file"""
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_suggestions(description, category):
    """Get top 3 suggested resolutions using NLP engine"""
    try:
        # Try to use NLP engine
        import sys
        sys.path.append('backend')
        from nlp_engine import get_nlp_recommendations
        
        suggestions = get_nlp_recommendations(description, category, RESOLUTIONS_FILE)
        return suggestions
    except Exception as e:
        # Fallback to simple matching
        resolutions = load_resolutions()
        suggestions = []
        
        description_lower = description.lower()
        
        for res in resolutions:
            score = 0
            
            # Exact category match gets highest priority
            if res['category'].lower() == category.lower():
                score += 10
            
            # Check for keyword matches in description
            issue_words = res['issue'].lower().split()
            for word in issue_words:
                if len(word) > 3 and word in description_lower:
                    score += 5
            
            # Check if description contains issue or vice versa
            if res['issue'].lower() in description_lower:
                score += 8
            elif description_lower in res['issue'].lower():
                score += 6
            
            if score > 0:
                suggestions.append((score, res))
        
        # Sort by score and return top 3
        suggestions.sort(reverse=True, key=lambda x: x[0])
        return [sug[1] for sug in suggestions[:3]]

def get_ticket_stats():
    """Get ticket statistics"""
    tickets = load_tickets()
    
    stats = {
        'total': len(tickets),
        'open': len([t for t in tickets if t['status'] == 'Open']),
        'in_progress': len([t for t in tickets if t['status'] == 'In Progress']),
        'resolved': len([t for t in tickets if t['status'] == 'Resolved']),
        'closed': len([t for t in tickets if t['status'] == 'Closed'])
    }
    
    return stats

def create_ticket(username, description, category, priority):
    """Create a new ticket"""
    tickets = load_tickets()
    ticket_id = max([t['id'] for t in tickets], default=0) + 1
    
    new_ticket = {
        "id": ticket_id,
        "username": username,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "Open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resolution": None
    }
    
    tickets.append(new_ticket)
    save_tickets(tickets)
    
    return ticket_id

def update_ticket(ticket_id, status=None, resolution=None):
    """Update ticket status and/or resolution"""
    tickets = load_tickets()
    
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            if status:
                ticket['status'] = status
            if resolution:
                ticket['resolution'] = resolution
            ticket['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    
    save_tickets(tickets)

def get_user_tickets(username):
    """Get all tickets for a specific user"""
    tickets = load_tickets()
    return [t for t in tickets if t['username'] == username]

def authenticate_user(username, password):
    """Authenticate user credentials"""
    users = load_users()
    
    if username in users and users[username]['password'] == password:
        return True, users[username]['type']
    
    return False, None

def register_user(username, password, email):
    """Register a new user"""
    users = load_users()
    
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        "password": password,
        "type": "user",
        "email": email
    }
    save_users(users)
    
    return True, "Account created successfully"
