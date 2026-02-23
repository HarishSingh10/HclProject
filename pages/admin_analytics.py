"""
Admin Analytics page
"""
import streamlit as st
from utils import load_tickets
import pandas as pd
from datetime import datetime, timedelta

def show_admin_analytics():
    """Display analytics and insights"""
    
    st.markdown("""
        <div class='animated-title' style='text-align: center; margin-bottom: 40px;'>
            <div style='display: inline-flex; align-items: center; justify-content: center; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        width: 80px; height: 80px; border-radius: 20px; margin-bottom: 20px;
                        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);'>
                <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 20V10M12 20V4M6 20V14" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <h1 style='color: white; font-size: 2.5rem; font-weight: 800; margin-bottom: 10px;'>Analytics & Insights</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem;'>
                Comprehensive ticket analytics and performance metrics
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    tickets = load_tickets()
    
    if not tickets:
        st.info("No data available yet. Tickets will appear here once created.")
        return
    
    df = pd.DataFrame(tickets)
    
    # Overview metrics with modern cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_resolution_time = "2.5 days"  # Placeholder
        st.markdown(f"""
            <div class='metric-card-modern card-3d'>
                <div class='metric-icon'>⏱️</div>
                <div class='metric-value' style='font-size: 2rem;'>{avg_resolution_time}</div>
                <div class='metric-label'>Avg Resolution Time</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        resolution_rate = round((len([t for t in tickets if t['status'] in ['Resolved', 'Closed']]) / len(tickets)) * 100, 1)
        st.markdown(f"""
            <div class='metric-card-modern card-3d'>
                <div class='metric-icon'>✅</div>
                <div class='metric-value'>{resolution_rate}%</div>
                <div class='metric-label'>Resolution Rate</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unique_users = len(df['username'].unique())
        st.markdown(f"""
            <div class='metric-card-modern card-3d'>
                <div class='metric-icon'>👥</div>
                <div class='metric-value'>{unique_users}</div>
                <div class='metric-label'>Active Users</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        critical_tickets = len([t for t in tickets if t['priority'] == 'Critical' and t['status'] not in ['Resolved', 'Closed']])
        st.markdown(f"""
            <div class='metric-card-modern card-3d'>
                <div class='metric-icon'>🚨</div>
                <div class='metric-value'>{critical_tickets}</div>
                <div class='metric-label'>Critical Open</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Charts section with modern containers
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("""
            <div class='chart-container-modern'>
                <h3 style='color: #1f2937; margin-bottom: 20px; font-weight: 700;'>📊 Issues by Category</h3>
            </div>
        """, unsafe_allow_html=True)
        
        category_counts = df['category'].value_counts()
        st.bar_chart(category_counts, use_container_width=True)
    
    with col_chart2:
        st.markdown("""
            <div class='chart-container-modern'>
                <h3 style='color: #1f2937; margin-bottom: 20px; font-weight: 700;'>⚡ Issues by Priority</h3>
            </div>
        """, unsafe_allow_html=True)
        
        priority_counts = df['priority'].value_counts()
        st.bar_chart(priority_counts, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Status distribution
    st.markdown("""
        <div style='background: white; border-radius: 20px; padding: 25px; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
            <h3 style='color: #1f2937; margin-bottom: 20px;'>📈 Status Distribution</h3>
        </div>
    """, unsafe_allow_html=True)
    
    status_counts = df['status'].value_counts()
    st.bar_chart(status_counts, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Most common issues table
    st.markdown("""
        <div style='background: white; border-radius: 20px; padding: 25px; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
            <h3 style='color: #1f2937; margin-bottom: 20px;'>🔥 Recent Tickets</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Display recent tickets in a table
    recent_tickets = df.sort_values('created_at', ascending=False).head(10)
    display_df = recent_tickets[['id', 'username', 'category', 'priority', 'status', 'created_at']].copy()
    display_df.columns = ['ID', 'User', 'Category', 'Priority', 'Status', 'Created At']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Category breakdown
    col_cat1, col_cat2 = st.columns(2)
    
    with col_cat1:
        st.markdown("""
            <div style='background: white; border-radius: 20px; padding: 25px; 
                        box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
                <h3 style='color: #1f2937; margin-bottom: 20px;'>📂 Category Breakdown</h3>
            </div>
        """, unsafe_allow_html=True)
        
        for category in df['category'].unique():
            count = len(df[df['category'] == category])
            percentage = (count / len(df)) * 100
            
            st.markdown(f"""
                <div style='margin-bottom: 15px;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                        <span style='color: #1f2937; font-weight: 600;'>{category}</span>
                        <span style='color: #6b7280;'>{count} ({percentage:.1f}%)</span>
                    </div>
                    <div style='background: #e5e7eb; border-radius: 10px; height: 10px; overflow: hidden;'>
                        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    height: 100%; width: {percentage}%;'></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col_cat2:
        st.markdown("""
            <div style='background: white; border-radius: 20px; padding: 25px; 
                        box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
                <h3 style='color: #1f2937; margin-bottom: 20px;'>⚡ Priority Breakdown</h3>
            </div>
        """, unsafe_allow_html=True)
        
        priority_order = ['Critical', 'High', 'Medium', 'Low']
        for priority in priority_order:
            if priority in df['priority'].values:
                count = len(df[df['priority'] == priority])
                percentage = (count / len(df)) * 100
                
                color_map = {
                    'Critical': '#ef4444',
                    'High': '#f97316',
                    'Medium': '#fbbf24',
                    'Low': '#10b981'
                }
                
                st.markdown(f"""
                    <div style='margin-bottom: 15px;'>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                            <span style='color: #1f2937; font-weight: 600;'>{priority}</span>
                            <span style='color: #6b7280;'>{count} ({percentage:.1f}%)</span>
                        </div>
                        <div style='background: #e5e7eb; border-radius: 10px; height: 10px; overflow: hidden;'>
                            <div style='background: {color_map[priority]}; height: 100%; width: {percentage}%;'></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
