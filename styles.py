import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        
        * { font-family: 'Inter', sans-serif !important; }
        
        /* === PERFECT DARK THEME === */
        .main { 
            background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%) !important;
            color: #FFFFFF !important;
        }
        
        .block-container { 
            padding: 2rem 3rem !important; 
            max-width: 1400px !important;
        }
        
        /* === BEAUTIFUL TITLE === */
        .jexa-title {
            font-size: 4rem !important; 
            font-weight: 900 !important; 
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 1rem 0 0.5rem 0 !important;
            letter-spacing: -0.02em;
        }
        
        .jexa-subtitle { 
            font-size: 1.2rem; 
            color: #a0aec0; 
            text-align: center; 
            margin-bottom: 3rem;
            font-weight: 500;
        }
        
        /* === PERFECT TABS === */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 6px;
            gap: 6px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 0.95rem;
            font-weight: 600;
            color: #a0aec0;
            padding: 0.75rem 1.75rem;
            border-radius: 12px;
            background: transparent;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
        }
        
        /* === PERFECT DROPDOWNS & INPUTS === */
        .stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .stSelectbox > div > div,
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 14px !important;
            height: 50px !important;
            padding: 0 1.25rem !important;
            font-size: 0.95rem !important;
            color: #ffffff !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        .stSelectbox > div > div:hover,
        .stTextInput > div > div > input:hover,
        .stNumberInput > div > div > input:hover {
            background: rgba(255, 255, 255, 0.12) !important;
            border-color: rgba(102, 126, 234, 0.5) !important;
        }
        
        .stSelectbox > div > div:focus-within,
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            background: rgba(255, 255, 255, 0.12) !important;
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        }
        
        /* Dropdown arrow color */
        .stSelectbox svg {
            fill: #ffffff !important;
        }
        
        /* === PERFECT BUTTONS === */
        .stButton > button {
            height: 50px !important;
            border-radius: 14px !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
            transition: all 0.3s ease !important;
            letter-spacing: 0.02em !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6) !important;
        }
        
        /* === DECISION CARD === */
        .decision-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 20px;
            padding: 3rem;
            text-align: center;
            backdrop-filter: blur(20px);
            margin: 2rem 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }
        
        /* === MINI CARDS === */
        .mini-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            border: 2px solid rgba(255, 255, 255, 0.1);
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .mini-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
            border-color: rgba(102, 126, 234, 0.6);
        }
        
        .mini-card.bullish { 
            border-color: #10b981 !important;
            background: rgba(16, 185, 129, 0.1) !important;
        }
        
        .mini-card.bearish { 
            border-color: #ef4444 !important;
            background: rgba(239, 68, 68, 0.1) !important;
        }
        
        /* === METRIC CARDS === */
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            border: 2px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            border-color: rgba(102, 126, 234, 0.5);
        }
        
        .metric-value { 
            font-size: 2rem; 
            font-weight: 800; 
            color: #ffffff;
            margin: 0.5rem 0;
            line-height: 1;
        }
        
        .metric-value.positive { color: #10b981; }
        .metric-value.negative { color: #ef4444; }
        
        .metric-label { 
            font-size: 0.75rem; 
            color: #a0aec0; 
            font-weight: 700; 
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* === SLIDER === */
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        .stSlider > div > div > div > div > div {
            background: white !important;
            border: 3px solid #667eea !important;
        }
        
        /* === HEADINGS === */
        h3 { 
            color: #ffffff !important; 
            font-weight: 700 !important; 
            margin: 2.5rem 0 1.5rem 0 !important;
            font-size: 1.5rem !important;
        }
        
        /* === ALERTS === */
        .stSuccess, .stError, .stWarning, .stInfo {
            background: rgba(255, 255, 255, 0.05) !important;
            border-left: 4px solid !important;
            border-radius: 12px !important;
            padding: 1rem 1.25rem !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* === HIDE STREAMLIT === */
        #MainMenu, footer, header, .stDeployButton { 
            visibility: hidden !important; 
        }
        
        /* === DIVIDER === */
        hr {
            border: none !important;
            height: 1px !important;
            background: rgba(255, 255, 255, 0.1) !important;
            margin: 2rem 0 !important;
        }
        
        /* === EXPANDER === */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            border: 2px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            font-weight: 600 !important;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: rgba(102, 126, 234, 0.5) !important;
        }
        
        /* === CHECKBOX === */
        .stCheckbox label {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
    </style>
    """, unsafe_allow_html=True)