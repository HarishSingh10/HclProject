"""
Login and Signup page
"""
import streamlit as st
from utils import authenticate_user, register_user, init_data_files

def show_login_page():
    """Display login/signup page with attractive UI"""
    
    # Initialize data files
    init_data_files()
    
    # Custom HTML for hero section with IT icon
    st.markdown("""
        <div class='animated-title' style='text-align: center; padding: 50px 0;'>
            <div style='display: inline-flex; align-items: center; justify-content: center; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        width: 120px; height: 120px; border-radius: 30px; margin-bottom: 30px;
                        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);'>
                <svg width="70" height="70" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 7H4C2.89543 7 2 7.89543 2 9V19C2 20.1046 2.89543 21 4 21H20C21.1046 21 22 20.1046 22 19V9C22 7.89543 21.1046 7 20 7Z" 
                          stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M8 21V5C8 4.46957 8.21071 3.96086 8.58579 3.58579C8.96086 3.21071 9.46957 3 10 3H14C14.5304 3 15.0391 3.21071 15.4142 3.58579C15.7893 3.96086 16 4.46957 16 5V21" 
                          stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="12" cy="14" r="2" fill="white"/>
                </svg>
            </div>
            <h1 style='font-size: 4rem; margin-bottom: 15px; background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;
                       text-shadow: 0 4px 20px rgba(0,0,0,0.2);'>
                IT Ticket System
            </h1>
            <p style='font-size: 1.4rem; color: white; opacity: 0.95; font-weight: 400; text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>
                Your one-stop solution for IT support and ticket management
            </p>
            <div style='margin-top: 20px;'>
                <span style='background: rgba(255,255,255,0.2); padding: 8px 20px; border-radius: 20px; 
                             color: white; font-size: 0.9rem; backdrop-filter: blur(10px);'>
                    ⚡ Powered by AI & NLP
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create centered columns for login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Tabs for Login and Signup
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                st.markdown("""
                    <div style='text-align: center; margin-bottom: 30px;'>
                        <h2 style='color: #1f2937; font-weight: 700; margin-bottom: 8px;'>Welcome Back!</h2>
                        <p style='color: #6b7280; font-size: 0.95rem;'>Please enter your credentials to continue</p>
                    </div>
                """, unsafe_allow_html=True)
                
                username = st.text_input("👤 Username", placeholder="Enter your username", label_visibility="collapsed", key="login_username_input")
                st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", label_visibility="collapsed", key="login_password_input")
                
                st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    login_button = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if login_button:
                    if not username or not password:
                        st.error("⚠️ Please fill in all fields")
                    else:
                        success, user_type = authenticate_user(username, password)
                        
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.user_type = user_type
                            st.success("✅ Login successful! Redirecting...")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
            
            # Demo credentials info
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🔍 Demo Credentials"):
                st.markdown("""
                    **Admin Account:**
                    - Username: `admin`
                    - Password: `admin123`
                    
                    **User Account:**
                    - Username: `user`
                    - Password: `user123`
                """)
        
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.form("signup_form", clear_on_submit=True):
                st.markdown("""
                    <div style='text-align: center; margin-bottom: 30px;'>
                        <h2 style='color: #1f2937; font-weight: 700; margin-bottom: 8px;'>Create New Account</h2>
                        <p style='color: #6b7280; font-size: 0.95rem;'>Join us to get instant IT support</p>
                    </div>
                """, unsafe_allow_html=True)
                
                new_username = st.text_input("👤 Username", placeholder="Choose a username", label_visibility="collapsed", key="signup_username_input")
                st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
                new_email = st.text_input("📧 Email", placeholder="your.email@company.com", label_visibility="collapsed", key="signup_email_input")
                st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
                new_password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password", label_visibility="collapsed", key="signup_password_input")
                st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password", label_visibility="collapsed", key="signup_confirm_input")
                
                st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    signup_button = st.form_submit_button("✨ Create Account", use_container_width=True)
                
                if signup_button:
                    if not new_username or not new_email or not new_password or not confirm_password:
                        st.error("⚠️ Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("⚠️ Password must be at least 6 characters long")
                    else:
                        success, message = register_user(new_username, new_password, new_email)
                        
                        if success:
                            st.success(f"✅ {message} Please login to continue.")
                            st.balloons()
                        else:
                            st.error(f"❌ {message}")
    
    # Features section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; margin-top: 60px;'>
            <h2 style='color: white; font-weight: 600; margin-bottom: 40px;'>Why Choose Our System?</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='feature-card'>
                <div class='metric-icon'>⚡</div>
                <h3 style='color: white; font-size: 1.3rem; margin-bottom: 12px; font-weight: 700;'>Instant Solutions</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;'>
                    Get top 3 AI-powered suggested fixes instantly using NLP
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='feature-card'>
                <div class='metric-icon'>📊</div>
                <h3 style='color: white; font-size: 1.3rem; margin-bottom: 12px; font-weight: 700;'>Track Progress</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;'>
                    Monitor ticket status in real-time with live updates
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='feature-card'>
                <div class='metric-icon'>🎯</div>
                <h3 style='color: white; font-size: 1.3rem; margin-bottom: 12px; font-weight: 700;'>Smart Matching</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;'>
                    TF-IDF & Cosine Similarity powered recommendations
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='feature-card'>
                <div class='metric-icon'>🔒</div>
                <h3 style='color: white; font-size: 1.3rem; margin-bottom: 12px; font-weight: 700;'>Secure & Fast</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;'>
                    FastAPI backend with robust authentication
                </p>
            </div>
        """, unsafe_allow_html=True)
