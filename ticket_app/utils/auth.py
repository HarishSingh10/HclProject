import streamlit as st
from typing import Tuple

def require_login():
    if not st.session_state.logged_in:
        st.warning("⚠️ Please log in to access this page")
        st.switch_page("pages/1_Login.py")
        st.stop()

def require_admin():
    if not st.session_state.logged_in:
        st.warning("⚠️ Please log in to access this page")
        st.switch_page("pages/1_Login.py")
        st.stop()
    
    if st.session_state.role != "admin":
        st.error("❌ Access Denied: Admin privileges required")
        st.stop()

def set_user_session(user_id: str, username: str, role: str, token: str):
    st.session_state.logged_in = True
    st.session_state.user_id = user_id
    st.session_state.username = username
    st.session_state.role = role
    st.session_state.auth_token = token

def clear_user_session():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.auth_token = None
