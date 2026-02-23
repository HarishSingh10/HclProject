"""
Raise Ticket page with suggestions
"""
import streamlit as st
from utils import create_ticket, get_suggestions

def show_raise_ticket_page():
    """Display ticket submission form with instant suggestions"""
    
    st.markdown("""
        <div class='animated-title' style='text-align: center; margin-bottom: 40px;'>
            <div style='display: inline-flex; align-items: center; justify-content: center; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        width: 80px; height: 80px; border-radius: 20px; margin-bottom: 20px;
                        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);'>
                <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15" 
                          stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7H9V5Z" 
                          stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M9 12H15M9 16H15" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </div>
            <h1 style='color: white; font-size: 2.5rem; font-weight: 800; margin-bottom: 10px;'>Raise New Ticket</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem;'>
                Describe your issue and get instant AI-powered solutions
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for form and preview
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
            <div class='glass-card' style='min-height: 500px;'>
        """, unsafe_allow_html=True)
        
        with st.form("ticket_form", clear_on_submit=True):
            st.markdown("""
                <h3 style='color: #1f2937; margin-bottom: 25px; font-weight: 700;'>
                    🎯 Ticket Details
                </h3>
            """, unsafe_allow_html=True)
            
            # Category selection with icons
            category = st.selectbox(
                "📂 Category",
                ["Network", "Hardware", "Software", "Access", "Other"],
                help="Select the category that best describes your issue"
            )
            
            # Priority selection
            priority = st.selectbox(
                "⚡ Priority Level",
                ["Low", "Medium", "High", "Critical"],
                help="How urgent is this issue?"
            )
            
            # Issue description
            description = st.text_area(
                "📋 Issue Description",
                height=200,
                placeholder="Please describe your issue in detail...\n\nExample: My laptop is not connecting to the office WiFi. I've tried restarting my laptop but the issue persists.",
                help="Provide as much detail as possible for better suggestions"
            )
            
            # Character counter
            if description:
                char_count = len(description)
                st.caption(f"Characters: {char_count}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit_button = st.form_submit_button("🚀 Submit Ticket", use_container_width=True)
            
            if submit_button:
                if not description or len(description.strip()) < 10:
                    st.error("⚠️ Please provide a detailed description (at least 10 characters)")
                else:
                    # Create ticket
                    ticket_id = create_ticket(
                        st.session_state.username,
                        description,
                        category,
                        priority
                    )
                    
                    st.success(f"✅ Ticket #{ticket_id} created successfully!")
                    st.balloons()
                    
                    # Store ticket info in session state for suggestions
                    st.session_state.last_ticket = {
                        'id': ticket_id,
                        'description': description,
                        'category': category,
                        'priority': priority
                    }
                    
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Show suggestions if ticket was just created
        if 'last_ticket' in st.session_state:
            ticket_info = st.session_state.last_ticket
            
            st.markdown("""
                <div style='background: rgba(255,255,255,0.95); border-radius: 20px; padding: 25px; 
                            box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
                    <h3 style='color: #667eea; margin-bottom: 20px; text-align: center;'>
                        💡 Suggested Solutions
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            suggestions = get_suggestions(ticket_info['description'], ticket_info['category'])
            
            if suggestions:
                for i, sug in enumerate(suggestions, 1):
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                    border-radius: 15px; padding: 20px; margin: 15px 0; 
                                    border-left: 5px solid #f59e0b; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                            <h4 style='color: #92400e; margin-bottom: 10px;'>
                                Solution {i}: {sug['issue']}
                            </h4>
                            <p style='color: #78350f; font-size: 0.85rem; margin-bottom: 8px;'>
                                <strong>Category:</strong> {sug['category']}
                            </p>
                            <div style='background: white; padding: 15px; border-radius: 10px; 
                                        color: #1f2937; line-height: 1.6;'>
                                {sug['resolution'].replace(chr(10), '<br>')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                if st.button("✅ Issue Resolved - Clear Suggestions"):
                    del st.session_state.last_ticket
                    st.success("Great! Glad we could help.")
                    st.rerun()
            else:
                st.markdown("""
                    <div style='background: rgba(255,255,255,0.9); border-radius: 15px; 
                                padding: 25px; text-align: center; margin-top: 15px;'>
                        <div style='font-size: 3rem; margin-bottom: 15px;'>🔍</div>
                        <p style='color: #6b7280; font-size: 1rem;'>
                            No automatic suggestions found.<br>
                            Our support team will review your ticket shortly.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            # Show helpful tips
            st.markdown("""
                <div style='background: rgba(255,255,255,0.95); border-radius: 20px; padding: 25px; 
                            box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
                    <h3 style='color: #667eea; margin-bottom: 20px; text-align: center;'>
                        💡 Tips for Better Support
                    </h3>
                    <div style='color: #374151; line-height: 1.8;'>
                        <p><strong>✓</strong> Be specific about the problem</p>
                        <p><strong>✓</strong> Include error messages if any</p>
                        <p><strong>✓</strong> Mention what you've already tried</p>
                        <p><strong>✓</strong> Select the correct category</p>
                        <p><strong>✓</strong> Set appropriate priority level</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Quick stats
            from utils import get_ticket_stats
            stats = get_ticket_stats()
            
            st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            border-radius: 20px; padding: 25px; color: white; text-align: center;
                            box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
                    <h4 style='margin-bottom: 15px;'>📊 System Stats</h4>
                    <div style='font-size: 2.5rem; font-weight: 700; margin: 10px 0;'>
                        {total}
                    </div>
                    <p style='opacity: 0.9;'>Total Tickets Processed</p>
                    <hr style='border: 1px solid rgba(255,255,255,0.3); margin: 20px 0;'>
                    <div style='display: flex; justify-content: space-around; margin-top: 15px;'>
                        <div>
                            <div style='font-size: 1.5rem; font-weight: 600;'>{resolved}</div>
                            <div style='font-size: 0.85rem; opacity: 0.8;'>Resolved</div>
                        </div>
                        <div>
                            <div style='font-size: 1.5rem; font-weight: 600;'>{open}</div>
                            <div style='font-size: 0.85rem; opacity: 0.8;'>Open</div>
                        </div>
                    </div>
                </div>
            """.format(
                total=stats['total'],
                resolved=stats['resolved'],
                open=stats['open']
            ), unsafe_allow_html=True)
