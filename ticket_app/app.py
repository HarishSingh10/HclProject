import streamlit as st
from streamlit_option_menu import option_menu
import os

st.set_page_config(
    page_title="IT Support Assistant",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.auth_token = None

st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body, .main {
        background-color: #0f1419;
        color: #e0e0e0;
        padding-top: 1.5rem;
    }
    
    .stApp {
        background-color: #0f1419;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #1a1f2e 0%, #16192b 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid #2a3f4f;
        color: #e0e0e0;
    }
    
    .stMetric label {
        color: #a0a0a0;
        font-size: 0.85rem;
    }
    
    .card {
        background: linear-gradient(135deg, #1a1f2e 0%, #16192b 100%);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
        border-left: 4px solid #00d084;
        border: 1px solid #2a3f4f;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d084 0%, #00b870 100%);
        color: #0f1419;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 208, 132, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 208, 132, 0.5);
        background: linear-gradient(135deg, #00e894 0%, #00c878 100%);
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #1a1f2e;
        border-radius: 0.75rem;
        border: 2px solid #2a3f4f;
        padding: 0.75rem;
        transition: all 0.3s ease;
        color: #e0e0e0;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00d084;
        box-shadow: 0 0 0 3px rgba(0, 208, 132, 0.15);
        background-color: #1a1f2e;
    }
    
    .streamlit-expanderHeader {
        background-color: #1a1f2e;
        border-radius: 0.75rem;
        border: 1px solid #2a3f4f;
    }
    
    .stDataFrame {
        border-radius: 0.75rem;
        overflow: hidden;
        background-color: #1a1f2e;
    }
    
    .stSuccess {
        background-color: rgba(0, 208, 132, 0.1);
        border-left: 4px solid #00d084;
        border-radius: 0.75rem;
        color: #00d084;
    }
    
    .stError {
        background-color: rgba(255, 71, 87, 0.1);
        border-left: 4px solid #ff4757;
        border-radius: 0.75rem;
        color: #ff6b7a;
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1);
        border-left: 4px solid #ffc107;
        border-radius: 0.75rem;
        color: #ffd54f;
    }
    
    .stInfo {
        background-color: rgba(0, 150, 255, 0.1);
        border-left: 4px solid #0096ff;
        border-radius: 0.75rem;
        color: #4db8ff;
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00d084, transparent);
        margin: 2rem 0;
    }
    
    h1 {
        color: #00d084;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 8px rgba(0, 208, 132, 0.2);
    }
    
    h2 {
        color: #00d084;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #00d084;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f1419;
        border-right: 1px solid #2a3f4f;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1f2e;
        border-bottom: 2px solid #2a3f4f;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #a0a0a0;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #00d084;
        border-bottom: 2px solid #00d084;
    }
    
    .stSpinner {
        color: #00d084;
    }
    
    p, span, label {
        color: #e0e0e0;
    }
    
    a {
        color: #00d084;
        text-decoration: none;
    }
    
    a:hover {
        color: #00e894;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛠️ IT Support Assistant")
    st.divider()
    
    if st.session_state.logged_in:
        st.markdown(f"**User:** {st.session_state.username}")
        
        if st.session_state.role == "admin":
            st.markdown("🔐 **Role:** Admin")
        else:
            st.markdown("👤 **Role:** User")
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.auth_token = None
            st.rerun()
    else:
        st.info("Please log in to continue")

if not st.session_state.logged_in:
    st.switch_page("pages/1_Login.py")
else:
    pages = [
        ("Raise Ticket", "pages/2_Raise_Ticket.py", "📝"),
        ("View Suggestions", "pages/3_View_Suggestions.py", "🤖"),
        ("Ticket Status", "pages/4_Ticket_Status.py", "📊"),
        ("Analytics", "pages/6_Analytics.py", "📈"),
    ]
    
    if st.session_state.role == "admin":
        pages.append(("Admin Dashboard", "pages/5_Admin_Dashboard.py", "🔐"))
    
    page_names = [f"{icon} {name}" for name, _, icon in pages]
    page_files = [file for _, file, _ in pages]
    
    selected = option_menu(
        menu_title=None,
        options=page_names,
        icons=[icon for _, _, icon in pages],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )
    
    selected_index = page_names.index(selected)
    st.switch_page(page_files[selected_index])
