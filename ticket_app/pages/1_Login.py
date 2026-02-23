import streamlit as st
from utils.api import api_client
from utils.auth import set_user_session

st.set_page_config(page_title="Login - IT Support Assistant", page_icon="🛠️", layout="wide")

st.markdown("""
    <style>
    [data-testid="collapsedControl"] {
        display: none
    }
    
    body, .main {
        background-color: #0f1419;
    }
    
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    
    .login-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #16192b 100%);
        padding: 3rem;
        border-radius: 1.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        max-width: 450px;
        width: 100%;
        border: 1px solid #2a3f4f;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-header h1 {
        color: #00d084;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 8px rgba(0, 208, 132, 0.2);
    }
    
    .login-header p {
        color: #a0a0a0;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        color: #000000;
        border-radius: 0.75rem;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00d084;
        box-shadow: 0 0 0 3px rgba(0, 208, 132, 0.15);
        background-color: #ffffff;
        color: #000000;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999999;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d084 0%, #00b870 100%);
        color: #0f1419;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 208, 132, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 208, 132, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
        <div class="login-header">
            <h1>🛠️ IT Support</h1>
            <p>Intelligent Ticket Resolution System</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.form("login_form"):
        email = st.text_input(
            "📧 Email Address",
            placeholder="Enter your email",
            help="Your registered email address"
        )
        password = st.text_input(
            "🔐 Password",
            type="password",
            placeholder="Enter your password",
            help="Your account password"
        )
        
        submit_button = st.form_submit_button("🚀 Sign In", use_container_width=True)
    
    if submit_button:
        if not email or not password:
            st.error("❌ Please enter both email and password")
        else:
            with st.spinner("🔄 Signing in..."):
                try:
                    response = api_client.login(email, password)
                    
                    user_id = response.get("user_id")
                    username = response.get("username")
                    role = response.get("role", "user")
                    token = response.get("access_token")
                    
                    if token:
                        set_user_session(user_id, username, role, token)
                        st.success("✅ Login successful!")
                        st.balloons()
                        st.switch_page("pages/2_Raise_Ticket.py")
                    else:
                        st.error("❌ Login failed: No token received")
                
                except Exception as e:
                    st.error(f"❌ Login failed: {str(e)}")
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #a0a0a0; font-size: 0.85rem; margin-top: 2rem;'>
        <p>🔒 Secure authentication with JWT tokens</p>
        <p>Need help? Contact your IT administrator</p>
        </div>
    """, unsafe_allow_html=True)
