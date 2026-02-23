"""
Admin Dashboard for managing all tickets
"""
import streamlit as st
from utils import load_tickets, update_ticket, get_ticket_stats
import pandas as pd

def show_admin_dashboard():
    """Display admin dashboard with all tickets and management options"""
    
    st.markdown("""
        <div class='animated-title' style='text-align: center; margin-bottom: 40px;'>
            <div style='display: inline-flex; align-items: center; justify-content: center; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        width: 80px; height: 80px; border-radius: 20px; margin-bottom: 20px;
                        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);'>
                <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 3H10C10.5304 3 11.0391 3.21071 11.4142 3.58579C11.7893 3.96086 12 4.46957 12 5V21C12 20.4696 11.7893 19.9609 11.4142 19.5858C11.0391 19.2107 10.5304 19 10 19H3V3Z" 
                          stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M21 3H14C13.4696 3 12.9609 3.21071 12.5858 3.58579C12.2107 3.96086 12 4.46957 12 5V21C12 20.4696 12.2107 19.9609 12.5858 19.5858C12.9609 19.2107 13.4696 19 14 19H21V3Z" 
                          stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <h1 style='color: white; font-size: 2.5rem; font-weight: 800; margin-bottom: 10px;'>Admin Dashboard</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem;'>
                Manage all support tickets and monitor system performance
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get statistics
    stats = get_ticket_stats()
    tickets = load_tickets()
    
    # Statistics cards with modern icons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
            <div class='metric-card-modern card-3d'>
                <div class='metric-icon'>📊</div>
                <div class='metric-value'>{stats['total']}</div>
                <div class='metric-label'>Total Tickets</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='metric-card-modern card-3d'>
                <div class='metric-icon'>🔓</div>
                <div class='metric-value'>{stats['open']}</div>
                <div class='metric-label'>Open</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='metric-card-modern card-3d'>
                <div class='metric-icon'>⚙️</div>
                <div class='metric-value'>{stats['in_progress']}</div>
                <div class='metric-label'>In Progress</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='metric-card-modern card-3d'>
                <div class='metric-icon'>✅</div>
                <div class='metric-value'>{stats['resolved']}</div>
                <div class='metric-label'>Resolved</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%); 
                        border-radius: 15px; padding: 25px; color: white; text-align: center;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
                <div style='font-size: 3rem; margin-bottom: 10px;'>🔒</div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{stats['closed']}</div>
                <div style='font-size: 0.95rem; opacity: 0.9; margin-top: 8px;'>Closed</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Filter and search options
    col_filter1, col_filter2, col_filter3 = st.columns([2, 2, 2])
    
    with col_filter1:
        status_filter = st.selectbox(
            "🔍 Filter by Status",
            ["All", "Open", "In Progress", "Resolved", "Closed"]
        )
    
    with col_filter2:
        category_filter = st.selectbox(
            "📂 Filter by Category",
            ["All", "Network", "Hardware", "Software", "Access", "Other"]
        )
    
    with col_filter3:
        priority_filter = st.selectbox(
            "⚡ Filter by Priority",
            ["All", "Critical", "High", "Medium", "Low"]
        )
    
    # Apply filters
    filtered_tickets = tickets
    
    if status_filter != "All":
        filtered_tickets = [t for t in filtered_tickets if t['status'] == status_filter]
    
    if category_filter != "All":
        filtered_tickets = [t for t in filtered_tickets if t['category'] == category_filter]
    
    if priority_filter != "All":
        filtered_tickets = [t for t in filtered_tickets if t['priority'] == priority_filter]
    
    # Sort by newest first
    filtered_tickets = sorted(filtered_tickets, key=lambda x: x['created_at'], reverse=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### 📋 Tickets ({len(filtered_tickets)} found)")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display tickets
    if not filtered_tickets:
        st.info("No tickets found matching the selected filters.")
    else:
        for ticket in filtered_tickets:
            # Color mappings
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
            
            with st.expander(f"🎫 Ticket #{ticket['id']} - {ticket['username']} - {ticket['status']}", expanded=False):
                st.markdown(f"""
                    <div style='background: #f9fafb; border-radius: 15px; padding: 20px; margin-bottom: 15px;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                            <div>
                                <span style='background: {status_color}; color: white; padding: 6px 14px; 
                                             border-radius: 20px; font-weight: 600; font-size: 0.85rem; margin-right: 8px;'>
                                    {ticket['status']}
                                </span>
                                <span style='background: {priority_color}; color: white; padding: 6px 14px; 
                                             border-radius: 20px; font-weight: 600; font-size: 0.85rem;'>
                                    {ticket['priority']} Priority
                                </span>
                            </div>
                            <span style='color: #6b7280; font-size: 0.9rem;'>
                                👤 {ticket['username']}
                            </span>
                        </div>
                        <div style='background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                            <p style='color: #1f2937; margin: 0; line-height: 1.6; font-weight: 500;'>
                                {ticket['description']}
                            </p>
                        </div>
                        <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;'>
                            <div>
                                <span style='color: #6b7280; font-size: 0.85rem;'>📂 Category:</span><br>
                                <span style='color: #1f2937; font-weight: 600;'>{ticket['category']}</span>
                            </div>
                            <div>
                                <span style='color: #6b7280; font-size: 0.85rem;'>📅 Created:</span><br>
                                <span style='color: #1f2937; font-weight: 600;'>{ticket['created_at']}</span>
                            </div>
                            <div>
                                <span style='color: #6b7280; font-size: 0.85rem;'>🔄 Updated:</span><br>
                                <span style='color: #1f2937; font-weight: 600;'>{ticket.get('updated_at', 'N/A')}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Management section
                col_mgmt1, col_mgmt2 = st.columns(2)
                
                with col_mgmt1:
                    new_status = st.selectbox(
                        "Update Status",
                        ["Open", "In Progress", "Resolved", "Closed"],
                        index=["Open", "In Progress", "Resolved", "Closed"].index(ticket['status']),
                        key=f"status_{ticket['id']}"
                    )
                
                with col_mgmt2:
                    resolution_text = st.text_area(
                        "Final Resolution",
                        value=ticket.get('resolution', ''),
                        height=100,
                        key=f"resolution_{ticket['id']}",
                        placeholder="Enter resolution details..."
                    )
                
                col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
                with col_btn2:
                    if st.button("💾 Update Ticket", key=f"update_{ticket['id']}", use_container_width=True):
                        update_ticket(ticket['id'], status=new_status, resolution=resolution_text)
                        st.success("✅ Ticket updated successfully!")
                        st.rerun()
