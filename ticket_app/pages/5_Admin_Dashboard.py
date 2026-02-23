import streamlit as st
import pandas as pd
from utils.api import api_client
from utils.auth import require_admin

st.set_page_config(page_title="Admin Dashboard - IT Support Assistant", page_icon="📈", layout="wide")

require_admin()

st.title("📈 Admin Dashboard")
st.markdown("System overview and ticket management")
st.divider()

# Fetch admin stats
with st.spinner("🔄 Loading dashboard data..."):
    try:
        stats_response = api_client.get_admin_stats(token=st.session_state.auth_token)
        tickets_response = api_client.get_admin_tickets(token=st.session_state.auth_token)
        
        stats = stats_response.get("stats", {})
        all_tickets = tickets_response.get("tickets", [])
        
        # Top metrics row
        st.subheader("📊 Key Metrics")
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(
                "📋 Total Tickets",
                stats.get("total_tickets", 0),
                delta=f"+{stats.get('tickets_today', 0)} today"
            )
        
        with metric_col2:
            st.metric(
                "🔴 Open Tickets",
                stats.get("open_tickets", 0),
                delta=f"{stats.get('open_percentage', 0):.0f}%"
            )
        
        with metric_col3:
            st.metric(
                "🟢 Resolved Tickets",
                stats.get("resolved_tickets", 0),
                delta=f"{stats.get('resolution_rate', 0):.0f}% rate"
            )
        
        with metric_col4:
            avg_time = stats.get("avg_resolution_time", 0)
            st.metric(
                "⏱️ Avg Resolution Time",
                f"{avg_time:.1f}h" if avg_time else "N/A"
            )
        
        st.divider()
        
        # Charts section
        st.subheader("📈 Analytics")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("**Tickets by Category**")
            category_data = stats.get("tickets_by_category", {})
            if category_data:
                st.bar_chart(category_data)
            else:
                st.info("No category data available")
        
        with chart_col2:
            st.markdown("**Status Distribution**")
            status_data = stats.get("status_distribution", {})
            if status_data:
                st.pie_chart(status_data)
            else:
                st.info("No status data available")
        
        # Time series chart
        st.markdown("**Tickets Over Time**")
        time_series = stats.get("tickets_over_time", {})
        if time_series:
            st.line_chart(time_series)
        else:
            st.info("No time series data available")
        
        st.divider()
        
        # All tickets management
        st.subheader("🎫 All Tickets Management")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                options=["All", "Open", "In Progress", "Resolved"],
                key="admin_status_filter"
            )
        
        with col2:
            category_filter = st.selectbox(
                "Filter by Category",
                options=["All", "Network", "Login", "Application", "Hardware", "Other"],
                key="admin_category_filter"
            )
        
        with col3:
            priority_filter = st.selectbox(
                "Filter by Priority",
                options=["All", "Low", "Medium", "High"],
                key="admin_priority_filter"
            )
        
        # Apply filters
        filtered_tickets = all_tickets
        
        if status_filter != "All":
            filtered_tickets = [t for t in filtered_tickets if t.get("status") == status_filter]
        
        if category_filter != "All":
            filtered_tickets = [t for t in filtered_tickets if t.get("category") == category_filter]
        
        if priority_filter != "All":
            filtered_tickets = [t for t in filtered_tickets if t.get("priority") == priority_filter]
        
        if not filtered_tickets:
            st.info("📭 No tickets match the selected filters")
        else:
            # Prepare table data
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
                    "User": ticket.get("user_name", "N/A"),
                    "Category": ticket.get("category", "N/A"),
                    "Priority": ticket.get("priority", "N/A"),
                    "Status": status_display,
                    "Created": ticket.get("created_at", "N/A")[:10],
                })
            
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.divider()
            
            # Bulk actions
            st.subheader("⚙️ Bulk Actions")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_ticket_id = st.selectbox(
                    "Select ticket to manage",
                    options=[t.get("id") for t in filtered_tickets],
                    format_func=lambda x: f"{x} - {next((t.get('category') for t in filtered_tickets if t.get('id') == x), 'N/A')}"
                )
            
            if selected_ticket_id:
                selected_ticket = next((t for t in filtered_tickets if t.get("id") == selected_ticket_id), None)
                
                if selected_ticket:
                    with st.container():
                        st.markdown("---")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("User", selected_ticket.get("user_name", "N/A"))
                        with col2:
                            st.metric("Category", selected_ticket.get("category", "N/A"))
                        with col3:
                            st.metric("Priority", selected_ticket.get("priority", "N/A"))
                        with col4:
                            st.metric("Status", selected_ticket.get("status", "N/A"))
                        
                        st.markdown("**Description:**")
                        st.write(selected_ticket.get("description", "No description"))
                        
                        st.markdown("---")
                        
                        # Status update
                        new_status = st.selectbox(
                            "Update Status",
                            options=["Open", "In Progress", "Resolved"],
                            index=["Open", "In Progress", "Resolved"].index(selected_ticket.get("status", "Open")),
                            key="admin_status_update"
                        )
                        
                        col1, col2 = st.columns(2)
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
                            if st.button("🔄 Refresh Data", use_container_width=True):
                                st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {str(e)}")
