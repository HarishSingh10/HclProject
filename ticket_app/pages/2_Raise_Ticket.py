import streamlit as st
from utils.api import api_client
from utils.auth import require_login

st.set_page_config(page_title="Raise Ticket - IT Support Assistant", page_icon="📝", layout="wide")

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

st.title("📝 Raise a Support Ticket")
st.markdown("Create a new support ticket and get AI-powered solutions")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📌 Description</div>', unsafe_allow_html=True)
        description = st.text_area(
            "Describe your issue",
            placeholder="What's the problem?",
            height=150,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🏷️ Category</div>', unsafe_allow_html=True)
        category = st.selectbox(
            "Select category",
            options=["Network", "Login", "Application", "Hardware", "Other"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">⚡ Priority</div>', unsafe_allow_html=True)
        priority = st.selectbox(
            "Select priority",
            options=["Low", "Medium", "High"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

with st.container():
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🚀 Actions</div>', unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        submit_button = st.button("✅ Submit Ticket", use_container_width=True, type="primary")
    
    with col_btn2:
        clear_button = st.button("🔄 Clear Form", use_container_width=True)
    
    with col_btn3:
        st.write("")
    
    st.markdown('</div>', unsafe_allow_html=True)

if clear_button:
    st.rerun()

if submit_button:
    if not description.strip():
        st.error("❌ Please describe your issue")
    else:
        with st.spinner("📤 Creating ticket..."):
            try:
                response = api_client.create_ticket(
                    description=description,
                    category=category,
                    priority=priority,
                    token=st.session_state.auth_token
                )
                
                ticket_id = response.get("ticket_id")
                
                if ticket_id:
                    st.success("✅ Ticket created successfully!")
                    st.balloons()
                    
                    st.session_state.last_ticket_id = ticket_id
                    
                    st.divider()
                    st.markdown('<div class="card-title">🎫 Ticket Information</div>', unsafe_allow_html=True)
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Ticket ID", ticket_id)
                    with col_b:
                        st.metric("Status", "Open")
                    with col_c:
                        st.metric("Category", category)
                    
                    st.divider()
                    
                    st.info("💡 Next: View AI-powered recommendations for your issue")
                    if st.button("🤖 View Suggestions", use_container_width=True, type="primary"):
                        st.session_state.view_suggestions = True
                        st.switch_page("pages/3_View_Suggestions.py")
                else:
                    st.error("❌ Failed to create ticket")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
