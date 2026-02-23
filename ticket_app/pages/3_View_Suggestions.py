import streamlit as st
from utils.api import api_client
from utils.auth import require_login

st.set_page_config(page_title="View Suggestions - IT Support Assistant", page_icon="🤖", layout="wide")

require_login()

st.title("🤖 Recommended Solutions")
st.markdown("AI-powered intelligent suggestions for your support ticket")
st.divider()

# Get ticket ID from session or input
ticket_id = None

if hasattr(st.session_state, 'last_ticket_id') and st.session_state.last_ticket_id:
    ticket_id = st.session_state.last_ticket_id
else:
    # Allow manual ticket ID input
    col1, col2 = st.columns([3, 1])
    with col1:
        ticket_id = st.text_input(
            "🎫 Enter Ticket ID",
            placeholder="e.g., TICKET-001",
            help="Enter the ticket ID to view recommendations"
        )
    with col2:
        st.write("")  # Spacing
        search_button = st.button("🔍 Search", use_container_width=True)

if ticket_id:
    with st.spinner("🔄 Fetching recommendations..."):
        try:
            response = api_client.get_recommendations(
                ticket_id=ticket_id,
                token=st.session_state.auth_token
            )
            
            recommendations = response.get("recommendations", [])
            ticket_info = response.get("ticket", {})
            
            if not recommendations:
                st.warning("⚠️ No recommendations available for this ticket yet")
            else:
                # Display ticket info
                with st.container():
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Ticket ID", ticket_info.get("id", "N/A"))
                    with col2:
                        st.metric("Category", ticket_info.get("category", "N/A"))
                    with col3:
                        st.metric("Priority", ticket_info.get("priority", "N/A"))
                
                st.divider()
                
                # Display recommendations
                st.subheader("💡 Top Recommendations")
                
                for idx, rec in enumerate(recommendations[:3], 1):
                    similarity = rec.get("similarity_score", 0)
                    resolution = rec.get("resolution_text", "")
                    source = rec.get("source", "Knowledge Base")
                    
                    # Color code based on similarity
                    if similarity >= 0.8:
                        badge_color = "🟢"
                        confidence = "High"
                        color_class = "success"
                    elif similarity >= 0.6:
                        badge_color = "🟡"
                        confidence = "Medium"
                        color_class = "warning"
                    else:
                        badge_color = "🔵"
                        confidence = "Low"
                        color_class = "info"
                    
                    with st.expander(
                        f"{badge_color} Solution {idx} - {confidence} Match ({similarity*100:.0f}%)",
                        expanded=(idx == 1)
                    ):
                        st.markdown(f"**Resolution:**\n\n{resolution}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Confidence", f"{similarity*100:.0f}%")
                        with col2:
                            st.metric("Source", source)
                        with col3:
                            st.metric("Rank", f"#{idx}")
                
                st.divider()
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✅ Mark as Resolved", use_container_width=True, type="primary"):
                        with st.spinner("📤 Updating ticket..."):
                            try:
                                api_client.update_ticket_status(
                                    ticket_id=ticket_id,
                                    status="Resolved",
                                    token=st.session_state.auth_token
                                )
                                st.success("✅ Ticket marked as resolved!")
                                st.balloons()
                                st.session_state.last_ticket_id = None
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                
                with col2:
                    if st.button("📝 Raise New Ticket", use_container_width=True):
                        st.session_state.last_ticket_id = None
                        st.switch_page("pages/2_Raise_Ticket.py")
                
                with col3:
                    if st.button("📊 View All Tickets", use_container_width=True):
                        st.switch_page("pages/4_Ticket_Status.py")
        
        except Exception as e:
            st.error(f"❌ Error fetching recommendations: {str(e)}")
else:
    st.info("💡 Enter a ticket ID above to view AI-powered recommendations")
