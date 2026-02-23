"""
Manage Resolutions page for admin
"""
import streamlit as st
from utils import load_resolutions, save_resolutions

def show_manage_resolutions():
    """Display resolution management interface"""
    
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: 10px;'>🔧 Manage Resolutions</h1>
        <p style='text-align: center; color: white; font-size: 1.1rem; opacity: 0.9; margin-bottom: 40px;'>
            Add and manage solution templates for common issues
        </p>
    """, unsafe_allow_html=True)
    
    # Add new resolution section
    st.markdown("""
        <div style='background: white; border-radius: 20px; padding: 30px; margin-bottom: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <h3 style='color: #667eea; margin-bottom: 20px;'>➕ Add New Resolution</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("add_resolution_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "📂 Category",
                ["Network", "Hardware", "Software", "Access", "Other"]
            )
        
        with col2:
            issue = st.text_input(
                "🎯 Issue Title",
                placeholder="e.g., Cannot connect to WiFi"
            )
        
        resolution = st.text_area(
            "💡 Resolution Steps",
            height=200,
            placeholder="Enter detailed resolution steps...\n\nExample:\n1. First step\n2. Second step\n3. Third step"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
        with col_btn2:
            submit_button = st.form_submit_button("💾 Add Resolution", use_container_width=True)
        
        if submit_button:
            if not issue or not resolution:
                st.error("⚠️ Please fill in all fields")
            else:
                resolutions = load_resolutions()
                resolutions.append({
                    "category": category,
                    "issue": issue,
                    "resolution": resolution
                })
                save_resolutions(resolutions)
                st.success("✅ Resolution added successfully!")
                st.balloons()
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display existing resolutions
    st.markdown("""
        <h3 style='color: white; margin-bottom: 20px;'>📚 Existing Resolutions</h3>
    """, unsafe_allow_html=True)
    
    resolutions = load_resolutions()
    
    # Group by category
    categories = {}
    for res in resolutions:
        cat = res['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(res)
    
    # Display by category
    for category, res_list in categories.items():
        with st.expander(f"📂 {category} ({len(res_list)} resolutions)", expanded=True):
            for i, res in enumerate(res_list):
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                                border-radius: 15px; padding: 20px; margin-bottom: 15px;
                                border-left: 5px solid #667eea;'>
                        <h4 style='color: #1f2937; margin-bottom: 15px;'>
                            {i+1}. {res['issue']}
                        </h4>
                        <div style='background: white; padding: 15px; border-radius: 10px;'>
                            <p style='color: #374151; margin: 0; line-height: 1.8; white-space: pre-line;'>
                                {res['resolution']}
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Delete button
                col_del1, col_del2, col_del3 = st.columns([3, 1, 3])
                with col_del2:
                    if st.button(f"🗑️ Delete", key=f"delete_{category}_{i}", use_container_width=True):
                        resolutions = load_resolutions()
                        resolutions.remove(res)
                        save_resolutions(resolutions)
                        st.success("Resolution deleted!")
                        st.rerun()
    
    # Statistics
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 20px; padding: 30px; color: white; text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <h3 style='margin-bottom: 20px;'>📊 Resolution Database Stats</h3>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;'>
                <div>
                    <div style='font-size: 2.5rem; font-weight: 700;'>{total}</div>
                    <div style='font-size: 1rem; opacity: 0.9;'>Total Resolutions</div>
                </div>
                <div>
                    <div style='font-size: 2.5rem; font-weight: 700;'>{categories_count}</div>
                    <div style='font-size: 1rem; opacity: 0.9;'>Categories</div>
                </div>
                <div>
                    <div style='font-size: 2.5rem; font-weight: 700;'>{avg_per_cat}</div>
                    <div style='font-size: 1rem; opacity: 0.9;'>Avg per Category</div>
                </div>
            </div>
        </div>
    """.format(
        total=len(resolutions),
        categories_count=len(categories),
        avg_per_cat=round(len(resolutions) / len(categories), 1) if categories else 0
    ), unsafe_allow_html=True)
