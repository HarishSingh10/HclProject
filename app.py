"""
IT Ticket Resolution System - Main Application
A modern, feature-rich ticket management system with instant AI-powered suggestions
"""
import streamlit as st
from frontend_styles import load_enhanced_css
from pages.login import show_login_page
from pages.raise_ticket import show_raise_ticket_page
from pages.track_tickets import show_track_tickets_page
from pages.admin_dashboard import show_admin_dashboard
from pages.admin_analytics import show_admin_analytics
from pages.manage_resolutions import show_manage_resolutions

# Page configuration
st.set_page_config(
    page_title="IT Ticket Resolution System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Load enhanced custom CSS
st.markdown(load_enhanced_css(), unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None

def main():
    """Main application logic"""
    
    if not st.session_state.logged_in:
        # Show login page
        show_login_page()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"""
                <div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.1); 
                            border-radius: 15px; margin-bottom: 30px;'>
                    <div style='font-size: 3rem; margin-bottom: 10px;'>👤</div>
                    <h3 style='color: white; margin: 0;'>Welcome!</h3>
                    <p style='color: rgba(255,255,255,0.8); margin: 5px 0;'>{st.session_state.username}</p>
                    <span style='background: rgba(255,255,255,0.2); color: white; padding: 5px 15px; 
                                 border-radius: 15px; font-size: 0.85rem; font-weight: 600;'>
                        {st.session_state.user_type.upper()}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🧭 Navigation")
            
            if st.session_state.user_type == "admin":
                # Admin navigation
                page = st.radio(
                    "Select Page",
                    ["📋 Dashboard", "📈 Analytics", "🔧 Manage Resolutions"],
                    label_visibility="collapsed"
                )
            else:
                # User navigation
                page = st.radio(
                    "Select Page",
                    ["📝 Raise Ticket", "📊 Track Tickets"],
                    label_visibility="collapsed"
                )
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user_type = None
                st.session_state.username = None
                if 'last_ticket' in st.session_state:
                    del st.session_state.last_ticket
                st.rerun()
            
            # Footer
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
                <div style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8rem;'>
                    <p>IT Ticket System v1.0</p>
                    <p>© 2024 All Rights Reserved</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Main content area
        if st.session_state.user_type == "admin":
            if page == "📋 Dashboard":
                show_admin_dashboard()
            elif page == "📈 Analytics":
                show_admin_analytics()
            elif page == "🔧 Manage Resolutions":
                show_manage_resolutions()
        else:
            if page == "📝 Raise Ticket":
                show_raise_ticket_page()
            elif page == "📊 Track Tickets":
                show_track_tickets_page()

if __name__ == "__main__":
    main()
