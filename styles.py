"""
ClickUp-Inspired Executive Dashboard Theme
Navy Blue / Clean White / Slate Palette with High-Contrast Legibility
"""

NAVY_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }

    /* Top padding balance */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1240px !important;
    }

    /* Sidebar - Crisp Clean Corporate Dark */
    section[data-testid="stSidebar"] {
        background-color: #0B192C !important;
        border-right: 1px solid #1E293B !important;
    }
    section[data-testid="stSidebar"] h3 {
        color: #93C5FD !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        font-weight: 800 !important;
        margin-top: 1.2rem !important;
    }
    section[data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    /* Executive Navy Hero Banner (White Text inside Blue) */
    .exec-banner {
        background: linear-gradient(135deg, #070F2B 0%, #0B192C 55%, #1E3E62 100%);
        border-radius: 14px;
        padding: 24px 30px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px -5px rgba(7, 15, 43, 0.25);
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .banner-title {
        font-size: 30px !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.6px;
        margin: 0;
    }
    .banner-sub {
        font-size: 14px !important;
        color: #94A3B8 !important;
        margin: 4px 0 0 0;
        font-weight: 500;
    }

    /* Elevated White Stat Boxes */
    .stat-pill {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 10px 20px;
        text-align: center;
        min-width: 95px;
    }
    .stat-val {
        font-size: 22px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1;
    }
    .stat-name {
        font-size: 11px;
        color: #CBD5E1;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 4px;
        letter-spacing: 0.5px;
    }

    /* Outreach Tracker Card */
    .outreach-box {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        margin-bottom: 20px;
    }

    /* Input Boxes: Crisp White Surface, Sharp Black Text, Glowing Blue Focus */
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2) !important;
    }
    input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }
    input::placeholder {
        color: #94A3B8 !important;
    }

    /* ClickUp Style Task Card Container */
    div[data-testid="stVerticalBlock"] > div.stContainer {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease !important;
    }
    div[data-testid="stVerticalBlock"] > div.stContainer:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px -4px rgba(11, 25, 44, 0.08) !important;
        border-color: #93C5FD !important;
    }

    /* Priority Badges */
    .badge-high {
        background: #FEE2E2;
        color: #991B1B;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #FCA5A5;
        letter-spacing: 0.5px;
    }
    .badge-med {
        background: #FEF3C7;
        color: #92400E;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #FCD34D;
        letter-spacing: 0.5px;
    }
    .badge-low {
        background: #F1F5F9;
        color: #475569;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #CBD5E1;
        letter-spacing: 0.5px;
    }

    /* Status Badges */
    .badge-done {
        background: #ECFDF5;
        color: #065F46;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #6EE7B7;
    }
    .badge-pending {
        background: #EFF6FF;
        color: #1E40AF;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #93C5FD;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #E2E8F0;
        padding: 5px;
        border-radius: 10px;
        margin-bottom: 22px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #475569 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 10px rgba(11, 25, 44, 0.2) !important;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 6px 14px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    div.stButton > button:hover {
        background-color: #F1F5F9 !important;
        border-color: #94A3B8 !important;
    }
</style>
"""

def inject_styles():
    import streamlit as st
    st.markdown(NAVY_THEME_CSS, unsafe_allow_html=True)