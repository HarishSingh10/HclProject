"""
Enhanced Frontend Styles with Dynamic Backgrounds and Modern UI
"""

def load_enhanced_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated gradient background */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles effect */
    .main::before {
        content: '';
        position: fixed;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Glass morphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        padding: 32px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
    }
    
    /* Metric cards with icons */
    .metric-card-modern {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.5);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card-modern:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 50px rgba(0,0,0,0.25);
    }
    
    .metric-icon {
        font-size: 3.5rem;
        margin-bottom: 12px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 12px 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        box-shadow: 4px 0 20px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 14px 16px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    /* Status badges with icons */
    .status-badge-modern {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Ticket cards */
    .ticket-card-modern {
        background: white;
        border-radius: 20px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border-left: 6px solid;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .ticket-card-modern::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, transparent 70%);
        border-radius: 50%;
        transform: translate(30%, -30%);
    }
    
    .ticket-card-modern:hover {
        transform: translateX(8px);
        box-shadow: 0 15px 50px rgba(0,0,0,0.15);
    }
    
    /* Suggestion cards */
    .suggestion-card-modern {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 18px;
        padding: 24px;
        margin: 16px 0;
        border-left: 5px solid #f59e0b;
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.2);
        transition: all 0.3s ease;
    }
    
    .suggestion-card-modern:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 32px rgba(245, 158, 11, 0.3);
    }
    
    /* Title animations */
    .animated-title {
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Chart containers */
    .chart-container-modern {
        background: white;
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 24px 0;
        border-top: 4px solid #667eea;
    }
    
    /* Progress bars */
    .progress-bar-container {
        background: #e5e7eb;
        border-radius: 12px;
        height: 12px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        transition: width 1s ease;
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        background: rgba(255,255,255,0.25);
        transform: translateY(-8px);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        border-radius: 12px;
        font-weight: 600;
        padding: 18px;
        border-left: 4px solid #667eea;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border-radius: 12px;
        padding: 16px;
        border-left: 5px solid #10b981;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .stError {
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
        color: #991b1b;
        border-radius: 12px;
        padding: 16px;
        border-left: 5px solid #ef4444;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
    }
    
    /* Loading animation */
    .loading-spinner {
        border: 4px solid rgba(255,255,255,0.3);
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide deploy button */
    .stDeployButton {display: none;}
    button[kind="header"] {display: none;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Enhanced card hover effects */
    .card-3d {
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1);
    }
    
    .card-3d:hover {
        transform: rotateY(5deg) rotateX(5deg) translateZ(20px);
    }
    
    /* Pulse animation for important elements */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.8;
            transform: scale(1.05);
        }
    }
    
    .pulse-animation {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Glow effect */
    .glow {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5),
                    0 0 40px rgba(102, 126, 234, 0.3),
                    0 0 60px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar enhancement */
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        box-shadow: 4px 0 30px rgba(0,0,0,0.3);
    }
    
    /* Radio button styling */
    .stRadio > label {
        background: rgba(255,255,255,0.1);
        padding: 12px 20px;
        border-radius: 10px;
        margin: 5px 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stRadio > label:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(5px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.1);
        padding: 8px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Form styling */
    .stForm {
        background: rgba(255,255,255,0.05);
        padding: 30px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Metric card icons with gradient */
    .metric-icon-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
    }
    
    /* Dashboard grid layout */
    .dashboard-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
        margin: 30px 0;
    }
    
    /* Ticket status timeline */
    .status-timeline {
        position: relative;
        padding-left: 30px;
    }
    
    .status-timeline::before {
        content: '';
        position: absolute;
        left: 10px;
        top: 0;
        bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .status-timeline-item {
        position: relative;
        margin-bottom: 20px;
    }
    
    .status-timeline-item::before {
        content: '';
        position: absolute;
        left: -24px;
        top: 5px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #667eea;
        border: 3px solid white;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3);
    }
    </style>
    """
