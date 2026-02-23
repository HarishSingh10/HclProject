import streamlit as st
import requests
import pandas as pd
import datetime
from datetime import timedelta
import plotly.express as px
import os

API_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.user_id = None
    st.session_state.email = None

if "new_ticket_data" not in st.session_state:
    st.session_state.new_ticket_data = None

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

# --- PAGE FUNCTIONS ---

def home_page():
    st.title("Why Choose Our System?")
    st.write("")
    st.write("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("⚡\n\n**Instant Solutions**\n\nGet top 3 suggested fixes instantly")
    with col2:
        st.success("📊\n\n**Track Progress**\n\nMonitor ticket status in real-time")
    with col3:
        st.warning("🎯\n\n**Smart Matching**\n\nAI-powered solution suggestions")
    with col4:
        st.error("🔒\n\n**Secure**\n\nYour data is safe with us")

def login_page():
    st.subheader("Login to Support Portal")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        res = requests.post(f"{API_URL}/login", data={"username": email, "password": password})
        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            import jwt
            decoded = jwt.decode(st.session_state.token, options={"verify_signature": False})
            st.session_state.role = decoded.get("role")
            st.session_state.user_id = decoded.get("id")
            st.session_state.email = decoded.get("sub")
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error(f"Invalid credentials. Server responded: {res.status_code}")

def signup_page():
    st.subheader("Create an Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("New Password", type="password")
    dept = st.text_input("Department")
    role = st.selectbox("Role", ["user", "admin"])
    
    if st.button("Sign Up"):
        payload = {"name": name, "email": email, "password": password, "department": dept, "role": role}
        res = requests.post(f"{API_URL}/signup", json=payload)
        if res.status_code == 200:
            st.success("Account created successfully! Please log in.")
        else:
            st.error("Error creating account.")

def logout_page():
    st.subheader("Are you sure you want to logout?")
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.role = None
        st.session_state.user_id = None
        st.session_state.email = None
        st.rerun()

def raise_ticket_page():
    st.subheader("Submit a New Issue")
    
    if st.session_state.new_ticket_data is None:
        desc = st.text_area("What issue are you facing?")
        cat = st.selectbox("Category", ["Login", "Network", "Application", "Access"])
        prio = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        if st.button("Submit Ticket"):
            if not desc:
                st.warning("Please provide a description.")
                return
                
            payload = {"description": desc, "category": cat, "priority": prio}
            res = requests.post(f"{API_URL}/tickets/", json=payload, headers=get_headers())
            
            if res.status_code == 200:
                st.session_state.new_ticket_data = res.json()
                st.rerun()
            else:
                st.error("Error creating ticket.")
    
    else:
        # Display the AI suggestions for the newly created ticket
        data = st.session_state.new_ticket_data
        st.success(f"Ticket #{data['ticket']['id']} generated successfully!")
        
        ai_res = data.get("ai_resolution", "")
        if ai_res:
            st.info("🤖 Our AI NLP Assistant has instantly suggested potential fixes:")
            import json
            try:
                suggestions = json.loads(ai_res)
                if not isinstance(suggestions, list):
                    suggestions = [str(suggestions)]
            except:
                suggestions = [ai_res]

            for i, s in enumerate(suggestions):
                st.write(f"{i+1}. {s}")
            
            st.write("---")
            selected_fix = st.selectbox("Did any of these fix your issue? Select which one:", ["None yet"] + suggestions)

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Yes, mark ticket #{data['ticket']['id']} as Resolved!", key=f"resolve_ai"):
                    if selected_fix != "None yet":
                        requests.put(f"{API_URL}/tickets/{data['ticket']['id']}/resolve?resolution_text=Selected AI Fix: {selected_fix}", headers=get_headers())
                        st.success("Ticket resolved successfully using AI suggestion! View it in Track Tickets.")
                        st.session_state.new_ticket_data = None
                        st.rerun()
                    else:
                        st.warning("Please select a specific point before resolving, or hit escalate.")
            with col2:
                if st.button(f"🚨 No, Escalate Issue", key=f"esc_ai"):
                    requests.put(f"{API_URL}/tickets/{data['ticket']['id']}/escalate", headers=get_headers())
                    st.success("Ticket escalated to Admin & Data Engineer. View it in Track Tickets.")
                    st.session_state.new_ticket_data = None
                    st.rerun()
        
        if st.button("⬅️ Back to Raise Another Ticket"):
            st.session_state.new_ticket_data = None
            st.rerun()

def track_tickets_page():
    st.subheader("Ticket History")
    res = requests.get(f"{API_URL}/tickets/user/{st.session_state.user_id}", headers=get_headers())
    if res.status_code == 200:
        tickets = res.json()
        if not tickets:
            st.write("No tickets requested.")
        else:
            for tkt in reversed(tickets):
                with st.expander(f"Ticket #{tkt['id']} - {tkt['category']} - {tkt['status']}"):
                    st.write(f"**Description:** {tkt['description']}")
                    st.write(f"**Priority:** {tkt['priority']}")
                    
                    if tkt['status'] not in ["Resolved", "Closed"]:
                        colA, colB = st.columns(2)
                        
                        options = []
                        if tkt.get("resolution"):
                            try:
                                import json
                                parsed = json.loads(tkt['resolution']['resolution_text'])
                                if isinstance(parsed, list):
                                    options = parsed
                            except:
                                pass

                        with colA:
                            if options:
                                res_text = st.selectbox("Select the AI resolution that fixed this:", ["Other (Type Below)"] + options, key=f"sel_{tkt['id']}")
                                custom_res = st.text_input("Or input custom resolution:", key=f"res_{tkt['id']}")
                                final_res = custom_res if res_text == "Other (Type Below)" else f"Selected AI Fix: {res_text}"
                            else:
                                final_res = st.text_input("If you fixed this, input the resolution:", key=f"res_{tkt['id']}")

                            if st.button("Mark as Resolved", key=f"mark_{tkt['id']}"):
                                if final_res and final_res != "Selected AI Fix: Other (Type Below)":
                                    requests.put(f"{API_URL}/tickets/{tkt['id']}/resolve?resolution_text={final_res}", headers=get_headers())
                                    st.rerun()
                        with colB:
                            st.write("")
                            st.write("")
                            if st.button("🚨 Escalate Issue (Not Resolved)", key=f"esc_{tkt['id']}"):
                                requests.put(f"{API_URL}/tickets/{tkt['id']}/escalate", headers=get_headers())
                                st.success("Ticket escalated successfully. An admin/data engineer will review it shortly.")
                                st.rerun()
                    
                    if tkt.get("resolution"):
                        res_txt = tkt['resolution']['resolution_text']
                        if "[ESCALATED]" in res_txt:
                            st.error(f"**Action Required / Escalation Notes:**\n\n {res_txt}")
                        else:
                            try:
                                import json
                                parsed = json.loads(res_txt)
                                if isinstance(parsed, list):
                                    st.info("**AI Suggested Fixes (Awaiting Resolution):**")
                                    for i, s in enumerate(parsed):
                                        st.write(f"{i+1}. {s}")
                                else:
                                    st.success(f"**Resolution Notes:** {res_txt}")
                            except:
                                st.success(f"**Resolution Notes:** {res_txt}")
    else:
        st.error("Error fetching tickets.")

def admin_dashboard_page():
    st.subheader("Manage Global Tickets")
    
    colA, colB = st.columns([2, 1])
    
    with colA:
        st.write("#### 🔍 Filter & Search")
        
        # Get users to build filter list
        user_res = requests.get(f"{API_URL}/admin/users", headers=get_headers())
        users_map = {}
        if user_res.status_code == 200:
            for u in user_res.json():
                users_map[u['id']] = f"{u['name']} ({u['email']})"
        
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            user_options = ["All Users"] + [f"{uid}: {uname}" for uid, uname in users_map.items()]
            selected_user = st.selectbox("Search by User", user_options)
            
        with f_col2:
            time_filter = st.selectbox("Time Range", ["All Time", "Last Hour", "Last 24 Hours", "Last 30 Days"])
            
    with colB:
        st.write("#### ➕ Quick Actions")
        with st.popover("Raise Ticket for User"):
            if not users_map:
                st.warning("No users available.")
            else:
                sel_u = st.selectbox("Select User", [f"{uid}: {uname}" for uid, uname in users_map.items()], key="pop_u")
                desc = st.text_area("Issue Description")
                cat = st.selectbox("Category", ["Login", "Network", "Application", "Access"], key="pop_c")
                prio = st.selectbox("Priority", ["Low", "Medium", "High"], key="pop_p")
                if st.button("Create Ticket", use_container_width=True):
                    uid = int(sel_u.split(":")[0])
                    payload = {"description": desc, "category": cat, "priority": prio}
                    requests.post(f"{API_URL}/admin/tickets?user_id={uid}", json=payload, headers=get_headers())
                    st.success("Ticket generated!")
                    st.rerun()

    st.divider()

    res = requests.get(f"{API_URL}/admin/tickets", headers=get_headers())
    if res.status_code == 200:
        tickets = res.json()
        if tickets:
            df = pd.DataFrame(tickets)
            df['created_date'] = pd.to_datetime(df['created_date'])
            
            # Apply user filter
            if selected_user != "All Users":
                sel_id = int(selected_user.split(":")[0])
                df = df[df['user_id'] == sel_id]
                
            # Apply time filter
            now = pd.to_datetime(datetime.datetime.utcnow())
            if time_filter == "Last Hour":
                df = df[df['created_date'] >= now - timedelta(hours=1)]
            elif time_filter == "Last 24 Hours":
                df = df[df['created_date'] >= now - timedelta(days=1)]
            elif time_filter == "Last 30 Days":
                df = df[df['created_date'] >= now - timedelta(days=30)]
            
            if df.empty:
                st.info("No tickets found matching the filters.")
            else:
                st.dataframe(
                    df[["id", "user_id", "category", "priority", "status", "created_date"]].sort_values("created_date", ascending=False).style.apply(
                        lambda x: ['background: #422222' if val == 'High' else '' for val in x], axis=1
                    ),
                    use_container_width=True
                )
            
            st.write("---")
            st.write("### 🛠️ Manage Specific Ticket")
            
            # Form to select and manage a ticket
            ticket_options = [f"#{t['id']} - {t['category']} ({t['status']})" for t in tickets if t['id'] in df['id'].values]
            selected_ticket_str = st.selectbox("Select Ticket to View/Update", [""] + ticket_options)
            
            if selected_ticket_str:
                selected_id = int(selected_ticket_str.replace("#", "").split(" - ")[0])
                
                # Find the ticket object
                tkt = next((t for t in tickets if t['id'] == selected_id), None)
                if tkt:
                    st.write(f"**Description:** {tkt['description']}")
                    
                    options = []
                    current_res_text = ""
                    if tkt.get("resolution"):
                        current_res_text = tkt['resolution']['resolution_text']
                        # Try parsing AI options
                        try:
                            import json
                            parsed = json.loads(current_res_text)
                            if isinstance(parsed, list):
                                options = parsed
                        except:
                            pass
                            
                    if "[ESCALATED]" in current_res_text:
                        st.error(f"**Escalation Notes:**\n\n {current_res_text}")
                    elif options:
                        st.info("**AI Suggested Fixes Available:**")
                        for i, s in enumerate(options):
                            st.write(f"{i+1}. {s}")
                    elif current_res_text:
                        st.success(f"**Current Resolution Notes:** {current_res_text}")
                    
                    st.write("#### Update Status & Resolution")
                    new_status = st.selectbox("Update Status", ["Open", "In Progress", "Resolved", "Closed"], index=["Open", "In Progress", "Resolved", "Closed"].index(tkt['status']) if tkt['status'] in ["Open", "In Progress", "Resolved", "Closed"] else 0)
                    
                    if options and tkt['status'] not in ["Resolved", "Closed"]:
                        res_select = st.selectbox("Select an AI resolution:", ["Keep Current/Other (Type Below)"] + options)
                    else:
                        res_select = "Keep Current/Other (Type Below)"
                        
                    custom_res = st.text_input("Custom Resolution Notes (Overrides Selection):")
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button("Apply Updates"):
                            # Update status first
                            status_r = requests.put(f"{API_URL}/admin/tickets/{selected_id}/status?status={new_status}", headers=get_headers())
                            
                            # Determine resolution text
                            final_res = None
                            if custom_res:
                                final_res = custom_res
                            elif res_select != "Keep Current/Other (Type Below)":
                                final_res = f"Selected AI Fix: {res_select}"
                                
                            success = True
                            if final_res:
                                # Resolve ticket sets the resolution text (Even if status isn't resolved, we can just use the endpoint to update text and status to resolved, wait, the resolve endpoint forces status to Resolved)
                                # Actually, we might need a separate way or just use the resolve endpoint if final_res is provided
                                if new_status == "Resolved":
                                    res_r = requests.put(f"{API_URL}/tickets/{selected_id}/resolve?resolution_text={final_res}", headers=get_headers())
                                    if res_r.status_code != 200:
                                        success = False
                                        st.error(res_r.json().get('detail', 'Error resolving ticket'))
                            
                            if success and status_r.status_code == 200:
                                st.success("Ticket updated successfully.")
                                st.rerun()
                            elif not success:
                                pass
                            else:
                                st.error("Failed to update status.")
    else:
        st.error("Error loading tickets.")

def admin_analytics_page():
    st.subheader("Admin Analytics Dashboard")
    res = requests.get(f"{API_URL}/admin/tickets", headers=get_headers())
    res_analytics = requests.get(f"{API_URL}/admin/analytics", headers=get_headers())
    
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: white;
        color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    div[data-testid="metric-container"] label {
        color: #666;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #1a5276;
        font-size: 32px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Defaults
    escalation_rate = "0.0%"
    total_tickets_month = 0
    if res.status_code == 200 and res.json():
        df_all = pd.DataFrame(res.json())
        df_all['created_date'] = pd.to_datetime(df_all['created_date'])
        
        # Calculate escalated
        escalated = df_all[df_all['priority'] == 'High'].shape[0]
        escalation_rate = f"{(escalated / df_all.shape[0]) * 100:.1f}%" if df_all.shape[0] > 0 else "0.0%"
        
        # Month
        now = pd.to_datetime(datetime.datetime.utcnow())
        total_tickets_month = df_all[df_all['created_date'] >= now - timedelta(days=30)].shape[0]
        
    if res_analytics.status_code == 200:
        data = res_analytics.json()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("AVG RESOLUTION TIME", f"{data.get('average_resolution_time_hours', 0.0)} Hrs")
        with c2:
            st.metric("ESCALATION RATE", escalation_rate)
        with c3:
            st.metric("TOTAL TICKETS (MONTH)", total_tickets_month)
        with c4:
            st.metric("MOST FREQUENT", data.get("most_common_category", "N/A"))
            
    st.write("---")
    
    if res.status_code == 200 and res.json():
        df = pd.DataFrame(res.json())
        
        c_left, c_right = st.columns([1,1])
        with c_left:
            st.write("### Most Common Issues")
            cat_count = df['category'].value_counts().reset_index()
            cat_count.columns = ['Category', 'Count']
            fig_bar = px.bar(cat_count, x='Category', y='Count', color_discrete_sequence=['#1a5276'])
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with c_right:
            st.write("### Ticket Status Distribution")
            status_count = df['status'].value_counts().reset_index()
            status_count.columns = ['Status', 'Count']
            color_map = {'Open': '#f39c12', 'Resolved': '#27ae60', 'In Progress': '#4285f4', 'Closed': '#5f6368', 'Escalated': '#e74c3c'}
            fig_pie = px.pie(status_count, values='Count', names='Status', hole=0.4, color='Status', color_discrete_map=color_map)
            fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.write("### Resolution Trend")
        df['date'] = pd.to_datetime(df['created_date']).dt.date
        date_count = df['date'].value_counts().sort_index().reset_index()
        date_count.columns = ['Date', 'Resolved Tickets']
        fig_line = px.line(date_count, x='Date', y='Resolved Tickets', markers=True, color_discrete_sequence=['#1a5276'])
        fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Not enough data to graph.")

def manage_resolutions_page():
    st.subheader("Add Official Resolutions")
    res_ticket_id = st.number_input("Enter Ticket ID to Add Resolution", min_value=1, step=1)
    resolve_text = st.text_area("Resolution Notes")
    if st.button("Add Official Resolution"):
        payload = {"ticket_id": res_ticket_id, "resolution_text": resolve_text}
        r = requests.post(f"{API_URL}/admin/resolution", json=payload, headers=get_headers())
        if r.status_code == 200:
            st.success("Resolution added.")
        else:
            st.error(r.json().get('detail', 'Error'))

# --- NAVIGATION ROUTING ---

if st.session_state.token is None:
    pg = st.navigation([
        st.Page(home_page, title="Home"),
        st.Page(login_page, title="Login"),
        st.Page(signup_page, title="Sign Up")
    ])
elif st.session_state.role == "admin":
    pg = st.navigation({
        "Admin Features": [
            st.Page(admin_dashboard_page, title="Admin Dashboard"),
            st.Page(admin_analytics_page, title="Admin Analytics"),
            st.Page(manage_resolutions_page, title="Manage Resolutions")
        ],
        "Account": [
            st.Page(logout_page, title="Logout")
        ]
    })
else:
    pg = st.navigation({
        "User Features": [
            st.Page(home_page, title="Home"),
            st.Page(raise_ticket_page, title="Raise Ticket"),
            st.Page(track_tickets_page, title="Track Tickets")
        ],
        "Account": [
            st.Page(logout_page, title="Logout")
        ]
    })

# Add overall title and sidebar info
st.sidebar.markdown("### IT Ticket AI")
if st.session_state.email:
    st.sidebar.caption(f"Logged in as: {st.session_state.email}")

pg.run()
