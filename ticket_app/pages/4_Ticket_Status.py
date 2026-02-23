import streamlit as st
import pandas as pd
from utils.api import api_client
from utils.auth import require_login

st.set_page_config(page_title="Ticket Status - IT Support Assistant", page_icon="📊", layout="wide")

require_login()

st.markdown("""
    <style>
    .card-container {
        background: linear-gradient(135deg, #1a1f2e 0%, #16192b 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a3f4f;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .card-title {
        color: #00d084;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Ticket Status")
st.markdown("Track and manage your support tickets")
st.divider()

with st.spinner("🔄 Loading tickets..."):
    try:
        response = api_client.get_user_tickets(token=st.session_state.auth_token)
        tickets = response.get("tickets", [])
        
        if not tickets:
            st.info("📭 No tickets found. Create one to get started!")
            if st.button("📝 Create New Ticket", use_container_width=True, type="primary"):
                st.switch_page("pages/2_Raise_Ticket.py")
        else:
            total_tickets = len(tickets)
            open_tickets = len([t for t in tickets if t.get("status") == "Open"])
            in_progress = len([t for t in tickets if t.get("status") == "In Progress"])
            resolved_tickets = len([t for t in tickets if t.get("status") == "Resolved"])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                with st.container():
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)
                    st.metric("📋 Total", total_tickets)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                with st.container():
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)
                    st.metric("🔴 Open", open_tickets)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                with st.container():
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)
                    st.metric("🟠 In Progress", in_progress)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                with st.container():
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)
                    st.metric("🟢 Resolved", resolved_tickets)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.divider()
            
            with st.container():
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">🔍 Filter Tickets</div>', unsafe_allow_html=True)
                
                status_filter = st.selectbox(
                    "Filter by Status",
                    options=["All", "Open", "In Progress", "Resolved"],
                    label_visibility="collapsed"
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            if status_filter != "All":
                filtered_tickets = [t for t in tickets if t.get("status") == status_filter]
            else:
                filtered_tickets = tickets
            
            if not filtered_tickets:
                st.info(f"📭 No {status_filter.lower()} tickets found")
            else:
                table_data = []
                for ticket in filtered_tickets:
                    status = ticket.get("status", "Unknown")
                    
                    if status == "Open":
                        status_display = "🔴 Open"
                    elif status == "In Progress":
                        status_display = "🟠 In Progress"
                    elif status == "Resolved":
                        status_display = "🟢 Resolved"
                    else:
                        status_display = f"⚪ {status}"
                    
                    table_data.append({
                        "Ticket ID": ticket.get("id", "N/A"),
                        "Category": ticket.get("category", "N/A"),
                        "Priority": ticket.get("priority", "N/A"),
                        "Status": status_display,
                        "Created": ticket.get("created_at", "N/A")[:10],
                    })
                
                with st.container():
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">📋 Your Tickets</div>', unsafe_allow_html=True)
                    
                    df = pd.DataFrame(table_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.divider()
                
                with st.container():
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">🔧 Ticket Actions</div>', unsafe_allow_html=True)
                    
                    selected_ticket_id = st.selectbox(
                        "Select a ticket",
                        options=[t.get("id") for t in filtered_tickets],
                        format_func=lambda x: f"{x} - {next((t.get('category') for t in filtered_tickets if t.get('id') == x), 'N/A')}",
                        label_visibility="collapsed"
                    )
                    
                    if selected_ticket_id:
                        selected_ticket = next((t for t in filtered_tickets if t.get("id") == selected_ticket_id), None)
                        
                        if selected_ticket:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Category", selected_ticket.get("category", "N/A"))
                            with col2:
                                st.metric("Priority", selected_ticket.get("priority", "N/A"))
                            with col3:
                                st.metric("Status", selected_ticket.get("status", "N/A"))
                            
                            st.markdown("**Description:**")
                            st.write(selected_ticket.get("description", "No description"))
                            
                            st.divider()
                            
                            new_status = st.selectbox(
                                "Update Status",
                                options=["Open", "In Progress", "Resolved"],
                                index=["Open", "In Progress", "Resolved"].index(selected_ticket.get("status", "Open")),
                                label_visibility="collapsed"
                            )
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("💾 Update Status", use_container_width=True, type="primary"):
                                    with st.spinner("📤 Updating..."):
                                        try:
                                            api_client.update_ticket_status(
                                                ticket_id=selected_ticket_id,
                                                status=new_status,
                                                token=st.session_state.auth_token
                                            )
                                            st.success("✅ Status updated!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Error: {str(e)}")
                            
                            with col2:
                                if st.button("🤖 View Suggestions", use_container_width=True):
                                    st.session_state.last_ticket_id = selected_ticket_id
                                    st.switch_page("pages/3_View_Suggestions.py")
                            
                            with col3:
                                if st.button("📝 New Ticket", use_container_width=True):
                                    st.switch_page("pages/2_Raise_Ticket.py")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error loading tickets: {str(e)}")
