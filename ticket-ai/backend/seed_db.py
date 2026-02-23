import os
import random
from datetime import datetime, timedelta
from database import engine, SessionLocal
import models
import auth

# Sample data
categories = [models.CategoryEnum.Login, models.CategoryEnum.Network, models.CategoryEnum.Application, models.CategoryEnum.Access]
priorities = [models.PriorityEnum.Low, models.PriorityEnum.Medium, models.PriorityEnum.High]

# Tickets and corresponding resolutions
historical_data = [
    ("Cannot connect to the office VPN", models.CategoryEnum.Network, "User instructed to update Cisco AnyConnect client and reboot."),
    ("Forgot my email password", models.CategoryEnum.Login, "Password reset link sent to secondary email and confirmed working."),
    ("Outlook keeps crashing on launch", models.CategoryEnum.Application, "Cleared Outlook cache and repaired Office installation."),
    ("Need access to the finance shared drive", models.CategoryEnum.Access, "Granted read/write access to finance drive following approval from manager."),
    ("WiFi is dropping frequently in meeting room A", models.CategoryEnum.Network, "Restarted access point in meeting room A and updated firmware."),
    ("Account locked after multiple failed attempts", models.CategoryEnum.Login, "Unlocked AD account and verified user identity."),
    ("Excel freezes when opening large macro file", models.CategoryEnum.Application, "Disabled hardware graphics acceleration in Excel settings."),
    ("Requesting license for Microsoft Visio", models.CategoryEnum.Access, "Assigned Visio license in Office 365 admin portal."),
    ("Cannot print to the network printer on 2nd floor", models.CategoryEnum.Network, "Reinstalled print drivers and restarted print spooler service."),
    ("Unable to log in to the CRM portal", models.CategoryEnum.Login, "Cleared browser cookies and cache. User logged in successfully."),
    ("Teams is not detecting my headset microphone", models.CategoryEnum.Application, "Updated audio drivers and selected correct input device in Teams settings."),
    ("Need admin rights for installing software", models.CategoryEnum.Access, "Provided temporary local admin rights for 2 hours."),
    ("VPN connection gets disconnected every 5 minutes", models.CategoryEnum.Network, "Changed VPN protocol from UDP to TCP."),
    ("Two-factor authentication is not sending SMS", models.CategoryEnum.Login, "Switched user to Authenticator app instead of SMS."),
    ("Adobe Acrobat Reader is asking for a serial key", models.CategoryEnum.Application, "Signed user out and back in with enterprise ID."),
    ("New employee needs access to GitHub organization", models.CategoryEnum.Access, "Sent GitHub invite and added to relevant teams."),
    ("Laptop is unable to find any wireless networks", models.CategoryEnum.Network, "Re-enabled WiFi adapter in Device Manager and updated driver."),
    ("Password expired and cannot change it remotely", models.CategoryEnum.Login, "Reset password via admin portal and forced change at next login."),
    ("Blue screen error when opening SAP GUI", models.CategoryEnum.Application, "Reinstalled SAP GUI patch level 5."),
    ("Requesting access to AWS production environment", models.CategoryEnum.Access, "Escalated to cloud ops. Access provisioned via IAM role.")
]

# Generate more synthetic data to reach ~50 records
extended_data = []
for i in range(30):
    sample = random.choice(historical_data)
    extended_data.append((
        f"{sample[0]} (Instance {i})",
        sample[1],
        sample[2]
    ))
historical_data.extend(extended_data)

def seed():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if users exist
        admin_user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
        if not admin_user:
            admin_user = models.User(
                name="Admin User",
                email="admin@example.com",
                hashed_password=auth.get_password_hash("admin123"),
                role=models.RoleEnum.admin,
                department="IT"
            )
            db.add(admin_user)
            
        test_user = db.query(models.User).filter(models.User.email == "user@example.com").first()
        if not test_user:
            test_user = models.User(
                name="Test User",
                email="user@example.com",
                hashed_password=auth.get_password_hash("user123"),
                role=models.RoleEnum.user,
                department="Engineering"
            )
            db.add(test_user)
            
        db.commit()
        
        # Check if tickets exist
        if db.query(models.Ticket).count() == 0:
            user_id = test_user.id if test_user else 1
            
            for desc, cat, res_txt in historical_data:
                # Randomize past dates
                days_ago = random.randint(1, 60)
                created_date = datetime.utcnow() - timedelta(days=days_ago)
                resolved_date = created_date + timedelta(hours=random.randint(1, 48))
                
                ticket = models.Ticket(
                    user_id=user_id,
                    description=desc,
                    category=cat,
                    priority=random.choice(priorities),
                    status=models.StatusEnum.Resolved,
                    created_date=created_date
                )
                db.add(ticket)
                db.flush() # To get ticket.id
                
                resolution = models.Resolution(
                    ticket_id=ticket.id,
                    resolution_text=res_txt,
                    resolved_date=resolved_date
                )
                db.add(resolution)
            
            db.commit()
            print(f"Successfully seeded database with {len(historical_data)} historical tickets.")
        else:
            print("Database already contains tickets. Skipping seed.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
