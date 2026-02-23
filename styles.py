"""
Custom CSS styles for the IT Ticket Resolution System
"""

def load_css():
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Card styling */
    .ticket-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .ticket-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.9;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-open {
        background: #fef3c7;
        color: #92400e;
    }
    
    .status-in-progress {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .status-resolved {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-closed {
        background: #e5e7eb;
        color: #374151;
    }
    
    /* Priority badges */
    .priority-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .priority-low {
        background: #d1fae5;
        color: #065f46;
    }
    
    .priority-medium {
        background: #fef3c7;
        color: #92400e;
    }
    
    .priority-high {
        background: #fed7aa;
        color: #9a3412;
    }
    
    .priority-critical {
        background: #fecaca;
        color: #991b1b;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 12px;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        border-radius: 10px;
        font-weight: 600;
        padding: 15px;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: #d1fae5;
        color: #065f46;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #10b981;
    }
    
    .stError {
        background: #fecaca;
        color: #991b1b;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #ef4444;
    }
    
    /* Title styling */
    h1 {
        color: white;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }
    
    h2, h3 {
        color: white;
        font-weight: 600;
    }
    
    /* Login container */
    .login-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        max-width: 500px;
        margin: 50px auto;
    }
    
    /* Suggestion card */
    .suggestion-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #f59e0b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Analytics chart container */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    /* Icon styling */
    .icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    /* Ticket header */
    .ticket-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Category badge */
    .category-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Dashboard grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    /* Animated gradient background */
    @keyframes gradient {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    .animated-bg {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    </style>
    """
