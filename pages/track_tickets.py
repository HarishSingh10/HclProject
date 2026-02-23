"""
Track Tickets page for users
"""
import streamlit as st
from utils import get_user_tickets, update_ticket
from datetime import datetime

def show_track_tickets_page():
    """Display user's tickets with tracking and status updates"""
    
    st.markdown("""
        <div class='animated-title' style='text-align: center; margin-bottom: 40px;'>
            <div style='display: inline-flex; align-items: center; justify-content: center; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        width: 80px; height: 80px; border-radius: 20px; margin-bottom: 20px;
                        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);'>
                <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 11L12 14L22 4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M21 12V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H16" 
                          stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <h1 style='color: white; font-size: 2.5rem; font-weight: 800; margin-bottom: 10px;'>My Tickets</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem;'>
                Track and manage your support tickets
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get user tickets
    tickets = get_user_tickets(st.session_state.username)
    
    if not tickets:
        st.markdown("""
            <div class='glass-card' style='text-align: center; padding: 80px 40px;'>
                <div style='font-size: 6rem; margin-bottom: 25px; opacity: 0.5;'>📭</div>
                <h2 style='color: #1f2937; margin-bottom: 15px; font-weight: 700;'>No Tickets Yet</h2>
                <p style='color: #6b7280; font-size: 1.1rem; line-height: 1.6;'>
                    You haven't raised any tickets yet.<br>
                    Click on "Raise Ticket" to create your first support request.
                </p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Statistics cards with modern design
    col1, col2, col3, col4 = st.columns(4)
    
    status_counts = {
        'Open': len([t for t in tickets if t['status'] == 'Open']),
        'In Progress': len([t for t in tickets if t['status'] == 'In Progress']),
        'Resolved': len([t for t in tickets if t['status'] == 'Resolved']),
        'Closed': len([t for t in tickets if t['status'] == 'Closed'])
    }
    
    with col1:
        st.markdown(f"""
            <div class='metric-card-modern glow'>
                <div class='metric-icon'>🔓</div>
                <div class='metric-value'>{status_counts['Open']}</div>
                <div class='metric-label'>Open</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='metric-card-modern glow'>
                <div class='metric-icon'>⚙️</div>
                <div class='metric-value'>{status_counts['In Progress']}</div>
                <div class='metric-label'>In Progress</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        border-radius: 15px; padding: 25px; color: white; text-align: center;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
                <div style='font-size: 2.5rem; font-weight: 700;'>{status_counts['Resolved']}</div>
                <div style='font-size: 1rem; opacity: 0.9; margin-top: 8px;'>Resolved</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%); 
                        border-radius: 15px; padding: 25px; color: white; text-align: center;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
                <div style='font-size: 2.5rem; font-weight: 700;'>{status_counts['Closed']}</div>
                <div style='font-size: 1rem; opacity: 0.9; margin-top: 8px;'>Closed</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Filter options
    col_filter1, col_filter2 = st.columns([2, 3])
    
    with col_filter1:
        status_filter = st.selectbox(
            "🔍 Filter by Status",
            ["All", "Open", "In Progress", "Resolved", "Closed"]
        )
    
    with col_filter2:
        sort_by = st.selectbox(
            "📅 Sort by",
            ["Newest First", "Oldest First", "Priority: High to Low"]
        )
    
    # Filter tickets
    filtered_tickets = tickets if status_filter == "All" else [t for t in tickets if t['status'] == status_filter]
    
    # Sort tickets
    if sort_by == "Newest First":
        filtered_tickets = sorted(filtered_tickets, key=lambda x: x['created_at'], reverse=True)
    elif sort_by == "Oldest First":
        filtered_tickets = sorted(filtered_tickets, key=lambda x: x['created_at'])
    else:  # Priority
        priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        filtered_tickets = sorted(filtered_tickets, key=lambda x: priority_order.get(x['priority'], 4))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display tickets
    if not filtered_tickets:
        st.info(f"No tickets found with status: {status_filter}")
    else:
        for ticket in filtered_tickets:
            # Status color mapping
            status_colors = {
                'Open': '#fbbf24',
                'In Progress': '#3b82f6',
                'Resolved': '#10b981',
                'Closed': '#6b7280'
            }
            
            priority_colors = {
                'Low': '#10b981',
                'Medium': '#fbbf24',
                'High': '#f97316',
                'Critical': '#ef4444'
            }
            
            status_color = status_colors.get(ticket['status'], '#6b7280')
            priority_color = priority_colors.get(ticket['priority'], '#6b7280')
            
            st.markdown(f"""
                <div style='background: white; border-radius: 20px; padding: 25px; margin-bottom: 20px;
                            box-shadow: 0 8px 16px rgba(0,0,0,0.1); border-left: 6px solid {status_color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                        <h3 style='color: #1f2937; margin: 0;'>Ticket #{ticket['id']}</h3>
                        <div>
                            <span style='background: {status_color}; color: white; padding: 6px 14px; 
                                         border-radius: 20px; font-weight: 600; font-size: 0.85rem; margin-right: 8px;'>
                                {ticket['status']}
                            </span>
                            <span style='background: {priority_color}; color: white; padding: 6px 14px; 
                                         border-radius: 20px; font-weight: 600; font-size: 0.85rem;'>
                                {ticket['priority']}
                            </span>
                        </div>
                    </div>
                    <div style='background: #f9fafb; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                        <p style='color: #374151; margin: 0; line-height: 1.6;'>{ticket['description']}</p>
                    </div>
                    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 15px;'>
                        <div>
                            <span style='color: #6b7280; font-size: 0.85rem;'>📂 Category:</span>
                            <span style='color: #1f2937; font-weight: 600; margin-left: 8px;'>{ticket['category']}</span>
                        </div>
                        <div>
                            <span style='color: #6b7280; font-size: 0.85rem;'>📅 Created:</span>
                            <span style='color: #1f2937; font-weight: 600; margin-left: 8px;'>{ticket['created_at']}</span>
                        </div>
                    </div>
            """, unsafe_allow_html=True)
            
            if ticket['resolution']:
                st.markdown(f"""
                    <div style='background: #d1fae5; padding: 15px; border-radius: 10px; border-left: 4px solid #10b981;'>
                        <p style='color: #065f46; margin: 0; font-weight: 600; margin-bottom: 8px;'>
                            ✅ Resolution:
                        </p>
                        <p style='color: #047857; margin: 0; line-height: 1.6;'>{ticket['resolution']}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Action button
            if ticket['status'] not in ['Closed', 'Resolved']:
                col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
                with col_btn2:
                    if st.button(f"✅ Mark Resolved", key=f"resolve_{ticket['id']}", use_container_width=True):
                        update_ticket(ticket['id'], status='Resolved')
                        st.success("Ticket marked as resolved!")
                        st.rerun()
