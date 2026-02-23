import streamlit as st
import pandas as pd
from utils.api import api_client
from utils.auth import require_login

st.set_page_config(page_title="Analytics - IT Support Assistant", page_icon="📊", layout="wide")

require_login()

st.title("📊 Analytics Dashboard")
st.markdown("Track your ticket metrics and performance insights")
st.divider()

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["📈 Overview", "📋 My Tickets", "🎯 Performance"])

with tab1:
    st.subheader("Your Ticket Overview")
    
    with st.spinner("🔄 Loading analytics..."):
        try:
            response = api_client.get_user_tickets(token=st.session_state.auth_token)
            tickets = response.get("tickets", [])
            
            if not tickets:
                st.info("📭 No tickets yet. Create one to get started!")
            else:
                # Calculate metrics
                total_tickets = len(tickets)
                open_tickets = len([t for t in tickets if t.get("status") == "Open"])
                in_progress = len([t for t in tickets if t.get("status") == "In Progress"])
                resolved_tickets = len([t for t in tickets if t.get("status") == "Resolved"])
                
                # Calculate resolution rate
                resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "📋 Total Tickets",
                        total_tickets,
                        delta=f"This month"
                    )
                
                with col2:
                    st.metric(
                        "🔴 Open",
                        open_tickets,
                        delta=f"{open_tickets/total_tickets*100:.0f}%" if total_tickets > 0 else "0%"
                    )
                
                with col3:
                    st.metric(
                        "🟠 In Progress",
                        in_progress,
                        delta=f"{in_progress/total_tickets*100:.0f}%" if total_tickets > 0 else "0%"
                    )
                
                with col4:
                    st.metric(
                        "🟢 Resolved",
                        resolved_tickets,
                        delta=f"{resolution_rate:.0f}% rate"
                    )
                
                st.divider()
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Status Distribution**")
                    status_data = {
                        "Open": open_tickets,
                        "In Progress": in_progress,
                        "Resolved": resolved_tickets
                    }
                    status_df = pd.DataFrame(list(status_data.items()), columns=["Status", "Count"])
                    st.bar_chart(status_df.set_index("Status"))
                
                with col2:
                    st.markdown("**Tickets by Category**")
                    category_counts = {}
                    for ticket in tickets:
                        cat = ticket.get("category", "Other")
                        category_counts[cat] = category_counts.get(cat, 0) + 1
                    
                    if category_counts:
                        cat_df = pd.DataFrame(list(category_counts.items()), columns=["Category", "Count"])
                        st.bar_chart(cat_df.set_index("Category"))
                    else:
                        st.info("No category data available")
        
        except Exception as e:
            st.error(f"❌ Error loading analytics: {str(e)}")

with tab2:
    st.subheader("Your Recent Tickets")
    
    with st.spinner("🔄 Loading tickets..."):
        try:
            response = api_client.get_user_tickets(token=st.session_state.auth_token)
            tickets = response.get("tickets", [])
            
            if not tickets:
                st.info("📭 No tickets found")
            else:
                # Filter options
                col1, col2 = st.columns(2)
                
                with col1:
                    status_filter = st.selectbox(
                        "Filter by Status",
                        options=["All", "Open", "In Progress", "Resolved"],
                        key="analytics_status_filter"
                    )
                
                with col2:
                    category_filter = st.selectbox(
                        "Filter by Category",
                        options=["All", "Network", "Login", "Application", "Hardware", "Other"],
                        key="analytics_category_filter"
                    )
                
                # Apply filters
                filtered_tickets = tickets
                
                if status_filter != "All":
                    filtered_tickets = [t for t in filtered_tickets if t.get("status") == status_filter]
                
                if category_filter != "All":
                    filtered_tickets = [t for t in filtered_tickets if t.get("category") == category_filter]
                
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
                            "Category": ticket.get("category", "N/A"),
                            "Priority": ticket.get("priority", "N/A"),
                            "Status": status_display,
                            "Created": ticket.get("created_at", "N/A")[:10],
                        })
                    
                    df = pd.DataFrame(table_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
        
        except Exception as e:
            st.error(f"❌ Error loading tickets: {str(e)}")

with tab3:
    st.subheader("Performance Insights")
    
    with st.spinner("🔄 Calculating insights..."):
        try:
            response = api_client.get_user_tickets(token=st.session_state.auth_token)
            tickets = response.get("tickets", [])
            
            if not tickets:
                st.info("📭 Create tickets to see performance insights")
            else:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Priority Distribution**")
                    priority_counts = {}
                    for ticket in tickets:
                        pri = ticket.get("priority", "Low")
                        priority_counts[pri] = priority_counts.get(pri, 0) + 1
                    
                    if priority_counts:
                        pri_df = pd.DataFrame(list(priority_counts.items()), columns=["Priority", "Count"])
                        st.pie_chart(pri_df.set_index("Priority"))
                    else:
                        st.info("No priority data available")
                
                with col2:
                    st.markdown("**Status Breakdown**")
                    status_counts = {}
                    for ticket in tickets:
                        status = ticket.get("status", "Open")
                        status_counts[status] = status_counts.get(status, 0) + 1
                    
                    if status_counts:
                        status_df = pd.DataFrame(list(status_counts.items()), columns=["Status", "Count"])
                        st.pie_chart(status_df.set_index("Status"))
                    else:
                        st.info("No status data available")
                
                st.divider()
                
                # Key insights
                st.markdown("**📌 Key Insights**")
                
                total = len(tickets)
                resolved = len([t for t in tickets if t.get("status") == "Resolved"])
                open_count = len([t for t in tickets if t.get("status") == "Open"])
                high_priority = len([t for t in tickets if t.get("priority") == "High"])
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if total > 0:
                        st.metric("Resolution Rate", f"{resolved/total*100:.0f}%")
                    else:
                        st.metric("Resolution Rate", "0%")
                
                with col2:
                    st.metric("Pending Tickets", open_count)
                
                with col3:
                    st.metric("High Priority", high_priority)
                
                with col4:
                    avg_per_category = total / len(set([t.get("category") for t in tickets]))
                    st.metric("Avg per Category", f"{avg_per_category:.1f}")
                
                st.divider()
                
                # Recommendations
                st.markdown("**💡 Recommendations**")
                
                recommendations = []
                
                if open_count > 5:
                    recommendations.append("🔴 You have many open tickets. Consider prioritizing them.")
                
                if high_priority > 0:
                    recommendations.append("⚡ You have high-priority tickets that need attention.")
                
                if resolved / total > 0.8 if total > 0 else False:
                    recommendations.append("✅ Great job! You have a high resolution rate.")
                
                if not recommendations:
                    recommendations.append("✨ Your ticket management looks good!")
                
                for rec in recommendations:
                    st.info(rec)
        
        except Exception as e:
            st.error(f"❌ Error calculating insights: {str(e)}")
