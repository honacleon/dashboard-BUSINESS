import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import bcrypt
from fpdf import FPDF
import base64
import time
import random
from whatsapp_alerts import show_whatsapp_alerts_page
from pdf_reports import show_pdf_reports_page

st.set_page_config(
    page_title="Aurum Business Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ThemeManager:
    @staticmethod
    def get_themes():
        return {
            "Cyber Neon Pro": {
                "primary": "#00f5ff",
                "secondary": "#ff006e",
                "background": "linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%)",
                "text": "#ffffff", 
                "accent": "rgba(0, 245, 255, 0.1)",
                "glass_effect": "rgba(0, 245, 255, 0.05)",
                "border": "rgba(0, 245, 255, 0.3)",
                "shadow": "0 0 20px rgba(0, 245, 255, 0.3), 0 0 40px rgba(255, 0, 110, 0.2)",
                "gradient_main": "linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%)",
                "gradient_bars": "linear-gradient(45deg, #00f5ff, #ff006e, #8a2be2)",
                "gradient_accent": "linear-gradient(135deg, #ff006e 0%, #00f5ff 100%)",
                "plotly_template": "plotly_dark"
            },
            "Royal Aurum Luxury": {
                "primary": "#ffd700",
                "secondary": "#e74c3c",
                "background": "linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #e74c3c 100%)",
                "text": "#ffffff",
                "accent": "rgba(255, 215, 0, 0.15)", 
                "glass_effect": "rgba(255, 215, 0, 0.1)",
                "border": "rgba(255, 215, 0, 0.4)",
                "shadow": "0 8px 32px 0 rgba(255, 215, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
                "gradient_main": "linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #e74c3c 100%)",
                "gradient_bars": "linear-gradient(45deg, #ffd700, #e74c3c, #4ecdc4)",
                "gradient_accent": "linear-gradient(135deg, #ffd700 0%, #e74c3c 50%, #4ecdc4 100%)",
                "plotly_template": "plotly_dark"
            }
        }
    
    @staticmethod
    def apply_theme(theme_name):
        themes = ThemeManager.get_themes()
        # Handle renamed themes
        if theme_name == "Corporate Glassmorphism":
            theme_name = "Cyber Neon Pro"
        if theme_name == "Purple Cosmic Glass":
            theme_name = "Cyber Neon Pro"
        if theme_name == "Soft Pastel Dream":
            theme_name = "Cyber Neon Pro"
        theme = themes[theme_name]
        
        
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Sistema de partículas de fundo */
        .particles-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }}
        
        .particle {{
            position: absolute;
            background: radial-gradient(circle, var(--primary-color), #471396, var(--secondary-color), transparent);
            border-radius: 50%;
            animation: float 6s infinite linear;
            opacity: 0.15;
            box-shadow: 0 0 15px var(--primary-color), 0 0 25px var(--secondary-color);
        }}
        
        @keyframes float {{
            from {{
                transform: translateY(100vh) rotate(0deg);
            }}
            to {{
                transform: translateY(-100px) rotate(360deg);
            }}
        }}
        
        :root {{
            --primary-color: {theme['primary']};
            --secondary-color: {theme['secondary']};
            --text-color: {theme['text']};
            --glass-bg: {theme['glass_effect']};
            --border-color: {theme['border']};
            --shadow: {theme['shadow']};
        }}
        
        * {{
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        
        .stApp {{
            background: {theme['background']} !important;
            background-attachment: fixed;
        }}
        
        .main > div {{
            background: transparent !important;
            backdrop-filter: blur(10px);
        }}
        
        /* Cards responsivos por tema */
        .metric-card {{
            background: {theme['glass_effect']} !important;
            backdrop-filter: blur(15px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(15px) saturate(180%) !important;
            padding: 25px !important;
            border-radius: 20px !important;
            border: 2px solid {theme['border']} !important;
            box-shadow: {theme['shadow']}, 0 2px 4px rgba(0,0,0,0.05) !important;
            margin: 15px 0 !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px) scale(1.02) !important;
            box-shadow: 0 20px 40px rgba(139, 126, 200, 0.15), {theme['shadow']} !important;
            border-color: {theme['primary']} !important;
        }}
        
        .metric-card::before {{
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: -100% !important;
            width: 100% !important;
            height: 100% !important;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent) !important;
            transition: left 0.8s !important;
        }}
        
        .metric-card:hover::before {{
            left: 100% !important;
        }}
        
        /* Soft Pastel Header */
        .gold-header {{
            background: {theme['glass_effect']} !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            padding: 35px !important;
            border-radius: 30px !important;
            text-align: center !important;
            margin-bottom: 35px !important;
            border: 2px solid {theme['border']} !important;
            box-shadow: {theme['shadow']}, 
                       inset 0 2px 0 rgba(255, 255, 255, 0.3) !important;
            position: relative !important;
            overflow: hidden !important;
        }}
        
        .gold-header::before {{
            content: '' !important;
            position: absolute !important;
            top: -50% !important;
            left: -50% !important;
            width: 200% !important;
            height: 200% !important;
            background: conic-gradient(from 0deg, var(--primary-color), var(--secondary-color), var(--primary-color)) !important;
            animation: rotate 10s linear infinite !important;
            opacity: 0.1 !important;
            z-index: -1 !important;
        }}
        
        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Sidebar Glassmorphism */
        .css-1d391kg, [data-testid="stSidebar"] > div {{
            background: linear-gradient(180deg, #1a1a1a 0%, #2d2d2d 100%) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-right: 1px solid {theme['border']} !important;
        }}
        
        
        /* Sidebar custom styling */
        [data-testid="stSidebar"] .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox {{
            margin-bottom: 1rem;
        }}
        
        [data-testid="stSidebar"] .stButton > button {{
            width: 100% !important;
            margin: 4px 0 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            background: transparent !important;
            color: #e0e0e0 !important;
            transition: all 0.3s ease !important;
            text-align: left !important;
            padding: 12px 16px !important;
        }}
        
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba({int(theme['primary'][1:3], 16)}, {int(theme['primary'][3:5], 16)}, {int(theme['primary'][5:7], 16)}, 0.15) !important;
            border-color: {theme['primary']}80 !important;
            color: white !important;
            transform: translateX(5px) !important;
        }}
        
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
            background: {theme['primary']}30 !important;
            border-color: {theme['primary']} !important;
            color: white !important;
            box-shadow: 0 0 15px {theme['primary']}40 !important;
        }}
        
        [data-testid="stSidebar"] .stButton > button[kind="primary"]::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 4px;
            height: 100%;
            background: {theme['primary']};
            border-radius: 0 4px 4px 0;
        }}
        
        /* Typography geral por tema */
        h1, h2, h3 {{
            font-weight: 700 !important;
            background: {theme['gradient_bars']} !important;
            background-clip: text !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-size: 200% 200% !important;
            animation: gradientShift 3s ease infinite !important;
            text-shadow: none !important;
            filter: brightness(1.1) contrast(1.05) !important;
        }}
        
        /* Headers por tema */
        .gold-header h1, .gold-header h3 {{
            background: {theme['gradient_accent']} !important;
            background-clip: text !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-size: 300% 300% !important;
            animation: gradientShift 4s ease infinite !important;
            filter: brightness(1.3) contrast(1.2) drop-shadow(0 0 15px rgba(255, 255, 255, 0.3)) !important;
        }}
        
        @keyframes gradientShift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        /* Form Controls */
        .stSelectbox label, .stTextInput label, .stRadio label {{
            color: {theme['text']} !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }}
        
        .stSelectbox > div > div, .stTextInput > div > div, .stRadio > div {{
            background: {theme['accent']} !important;
            backdrop-filter: blur(5px) !important;
            border: 1px solid {theme['border']} !important;
            border-radius: 15px !important;
            transition: all 0.3s ease !important;
        }}
        
        .stSelectbox > div > div:hover, .stTextInput > div > div:hover {{
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 20px rgba(var(--primary-color), 0.3) !important;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: {theme['gradient_bars']} !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative !important;
            overflow: hidden !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3) !important;
        }}
        
        .stButton > button:active {{
            transform: translateY(0px) !important;
        }}
        
        /* Metric Values Animation */
        @keyframes countUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .metric-card h2, .metric-card h3 {{
            color: {theme['text']} !important;
            margin: 0 !important;
            animation: countUp 0.6s ease-out !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        }}
        
        /* Plotly Charts Container */
        .js-plotly-plot {{
            border-radius: 20px !important;
            overflow: hidden !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid {theme['border']} !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px !important;
        }}
        
        ::-webkit-scrollbar-track {{
            background: transparent !important;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--primary-color) !important;
            border-radius: 10px !important;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--secondary-color) !important;
        }}
        
        /* Loading Animation */
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        /* Tab Navigation */
        .stTabs [data-baseweb="tab-list"] {{
            background: {theme['glass_effect']} !important;
            backdrop-filter: blur(15px) !important;
            border-radius: 15px !important;
            padding: 5px !important;
            border: 1px solid {theme['border']} !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
            color: {theme['text']} !important;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background: var(--primary-color) !important;
            color: white !important;
        }}
        
        /* Dataframe Styling */
        .stDataFrame {{
            background: {theme['glass_effect']} !important;
            backdrop-filter: blur(15px) !important;
            border-radius: 15px !important;
            border: 1px solid {theme['border']} !important;
            overflow: hidden !important;
        }}
        
        /* Success/Error Messages */
        .stSuccess {{
            background: rgba(16, 185, 129, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(16, 185, 129, 0.3) !important;
            border-radius: 15px !important;
        }}
        
        .stError {{
            background: rgba(239, 68, 68, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 15px !important;
        }}
        
        /* Loading Animation Premium */
        .loading-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--primary-color);
            background: radial-gradient(circle, var(--primary-color), var(--secondary-color));
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            animation: fadeOut 2s ease-in-out 1s forwards;
        }}
        
        .loading-spinner {{
            width: 60px;
            height: 60px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        @keyframes fadeOut {{
            0% {{ opacity: 1; }}
            100% {{ opacity: 0; visibility: hidden; }}
        }}
        
        /* Page Entry Animation */
        .page-container {{
            animation: slideIn 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            opacity: 0;
            transform: translateY(30px);
        }}
        
        @keyframes slideIn {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Purple Cosmic Sparkle Effect */
        .sparkle {{
            position: absolute;
            width: 5px;
            height: 5px;
            background: radial-gradient(circle, var(--primary-color), var(--secondary-color));
            border-radius: 50%;
            animation: sparkle 2s infinite;
            box-shadow: 0 0 10px var(--primary-color), 0 0 20px var(--secondary-color);
        }}
        
        @keyframes sparkle {{
            0%, 100% {{ opacity: 0; transform: scale(0); }}
            50% {{ opacity: 1; transform: scale(1); }}
        }}
        
        @keyframes cardPulse {{
            0%, 100% {{ 
                box-shadow: {theme['shadow']}, inset 0 1px 0 rgba(255, 255, 255, 0.2);
            }}
            50% {{ 
                box-shadow: {theme['shadow']}, 0 0 30px rgba(255, 204, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
            }}
        }}
        
        .metric-card {{
            animation: cardPulse 4s ease-in-out infinite !important;
        }}
        
        /* Mobile Responsiveness */
        @media (max-width: 768px) {{
            .metric-card {{
                padding: 15px !important;
                margin: 10px 0 !important;
            }}
            
            .gold-header {{
                padding: 20px !important;
            }}
            
            h1 {{ font-size: 24px !important; }}
            h2 {{ font-size: 20px !important; }}
            h3 {{ font-size: 18px !important; }}
            
            [data-testid="stSidebar"] {{
                width: 100% !important;
            }}
        }}
        
        @media (max-width: 480px) {{
            .metric-card {{
                padding: 12px !important;
                margin: 8px 0 !important;
                border-radius: 15px !important;
            }}
            
            .gold-header {{
                padding: 15px !important;
                border-radius: 20px !important;
            }}
            
            h1 {{ font-size: 20px !important; }}
            h2 {{ font-size: 18px !important; }}
            h3 {{ font-size: 16px !important; }}
        }}
        
        </style>
        """, unsafe_allow_html=True)
        
        return theme

class AuthManager:
    USERS = {
        "aurumadmin": {
            "password": "admin123",  # Senha simples para teste
            "role": "Admin",
            "name": "Aurum Admin",
            "permissions": ["overview", "marketing", "operational", "reports", "alerts", "settings"]
        },
        "aurummanager": {
            "password": "manager123",  # Senha simples para teste
            "role": "Manager", 
            "name": "Aurum Manager",
            "permissions": ["overview", "marketing", "reports", "alerts"]
        },
        "aurumviewer": {
            "password": "viewer123",  # Senha simples para teste
            "role": "Viewer",
            "name": "Aurum Viewer", 
            "permissions": ["overview"]
        }
    }
    
    @staticmethod
    def verify_password(password, stored_password):
        return password == stored_password
    
    @staticmethod
    def authenticate(username, password):
        if username in AuthManager.USERS:
            user = AuthManager.USERS[username]
            if AuthManager.verify_password(password, user["password"]):
                return user
        return None
    
    @staticmethod
    def has_permission(permission):
        if 'user' not in st.session_state:
            return False
        return permission in st.session_state.user.get('permissions', [])

class DataGenerator:
    @staticmethod
    def generate_kpis():
        base_revenue = random.uniform(2500000, 5000000)
        return {
            "Receita Total": f"R$ {base_revenue:,.0f}",
            "Crescimento": f"+{random.uniform(8, 25):.1f}%",
            "ROI Google Ads": f"{random.uniform(3.2, 4.8):.1f}x",
            "ROI Meta Ads": f"{random.uniform(2.8, 4.2):.1f}x", 
            "Conversões": f"{random.randint(1200, 3500):,}",
            "CAC": f"R$ {random.uniform(85, 120):.0f}",
            "LTV": f"R$ {random.uniform(850, 1200):.0f}",
            "Ticket Médio": f"R$ {random.uniform(340, 520):.0f}",
            "Churn Rate": f"{random.uniform(2.1, 4.8):.1f}%",
            "NPS": f"{random.randint(65, 85)}"
        }
    
    @staticmethod
    def generate_time_series(days=90):
        dates = [datetime.now() - timedelta(days=x) for x in range(days)][::-1]
        base_value = random.uniform(50000, 100000)
        values = []
        
        for i, date in enumerate(dates):
            trend = base_value * (1 + 0.001 * i)
            seasonal = np.sin(2 * np.pi * i / 30) * base_value * 0.1
            noise = random.uniform(-base_value * 0.05, base_value * 0.05)
            values.append(max(0, trend + seasonal + noise))
            
        return pd.DataFrame({
            'Date': dates,
            'Value': values,
            'Growth': np.random.uniform(0.8, 1.2, len(dates))
        })
    
    @staticmethod
    def generate_channel_data():
        channels = ["Google Ads", "Meta Ads", "Orgânico", "Email", "WhatsApp"]
        return pd.DataFrame({
            'Channel': channels,
            'Spend': [random.uniform(15000, 45000) for _ in channels],
            'Revenue': [random.uniform(45000, 180000) for _ in channels], 
            'Conversions': [random.randint(150, 800) for _ in channels],
            'ROAS': [random.uniform(2.5, 5.2) for _ in channels]
        })
    
    @staticmethod
    def generate_funnel_data():
        return pd.DataFrame({
            'Stage': ["Visitantes", "Leads", "Oportunidades", "Negociação", "Fechados"],
            'Count': [15000, 4500, 1800, 850, 420],
            'Conversion': [100, 30, 12, 5.7, 2.8]
        })

class ChartGenerator:
    @staticmethod
    def create_revenue_chart(theme, data):
        fig = go.Figure()
        
        # Converter cor hex para rgba
        primary_color = theme['primary']
        if primary_color.startswith('#'):
            hex_color = primary_color[1:]
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            fillcolor = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.3)"
        else:
            fillcolor = "rgba(14, 165, 233, 0.3)"  # fallback
        
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data['Value'],
            mode='lines+markers',
            name='Receita',
            line=dict(
                width=4,
                color=theme['primary']
            ),
            fill='tonexty',
            fillcolor=fillcolor
        ))
        
        fig.update_layout(
            template=theme['plotly_template'],
            title="📈 Evolução da Receita - Últimos 90 dias",
            title_font=dict(size=20, color=theme['text']),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=theme['text']),
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_channel_performance(theme, data):
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=data['Channel'],
            y=data['ROAS'],
            name='ROAS',
            marker=dict(
                color=data['ROAS'],
                colorscale=[[0, theme['accent']], [1, theme['primary']]],
                showscale=True,
                colorbar=dict(title="ROAS")
            ),
            text=[f"R$ {rev:,.0f}" for rev in data['Revenue']],
            textposition='outside'
        ))
        
        fig.update_layout(
            template=theme['plotly_template'],
            title="🎯 Performance por Canal",
            title_font=dict(size=20, color=theme['text']),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=theme['text']),
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_funnel_chart(theme, data):
        fig = go.Figure(go.Funnel(
            y=data['Stage'],
            x=data['Count'],
            textinfo="value+percent initial",
            marker=dict(
                color=[theme['primary'], theme['secondary'], theme['accent'],
                      theme['primary'], theme['secondary']]
            )
        ))
        
        fig.update_layout(
            template=theme['plotly_template'],
            title="🔄 Funil de Conversão",
            title_font=dict(size=20, color=theme['text']),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=theme['text']),
            height=500
        )
        
        return fig
    
    @staticmethod
    def create_3d_scatter(theme, data):
        fig = go.Figure(data=[go.Scatter3d(
            x=data['Spend'],
            y=data['Revenue'], 
            z=data['Conversions'],
            mode='markers+text',
            text=data['Channel'],
            textposition='top center',
            marker=dict(
                size=15,
                color=data['ROAS'],
                colorscale=[[0, theme['accent']], [1, theme['primary']]],
                opacity=0.8,
                showscale=True,
                colorbar=dict(title="ROAS")
            )
        )])
        
        fig.update_layout(
            template=theme['plotly_template'],
            title="🎪 Análise 3D: Spend vs Revenue vs Conversões",
            title_font=dict(size=20, color=theme['text']),
            scene=dict(
                xaxis_title='Investimento (R$)',
                yaxis_title='Receita (R$)', 
                zaxis_title='Conversões'
            ),
            height=600
        )
        
        return fig

def show_login():
    # Tutorial rápido para modo dark
    st.info("🌙 **Para melhor experiência:** Ative o modo dark do Streamlit clicando no menu ☰ (canto superior direito) > Settings > Theme > Dark")
    
    st.markdown("""
    <div class="particles-bg">
        <div class="particle" style="left: 10%; width: 20px; height: 20px; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; width: 15px; height: 15px; animation-delay: 1s;"></div>
        <div class="particle" style="left: 30%; width: 25px; height: 25px; animation-delay: 2s;"></div>
        <div class="particle" style="left: 40%; width: 18px; height: 18px; animation-delay: 3s;"></div>
        <div class="particle" style="left: 50%; width: 22px; height: 22px; animation-delay: 4s;"></div>
        <div class="particle" style="left: 60%; width: 16px; height: 16px; animation-delay: 5s;"></div>
        <div class="particle" style="left: 70%; width: 24px; height: 24px; animation-delay: 0.5s;"></div>
        <div class="particle" style="left: 80%; width: 19px; height: 19px; animation-delay: 1.5s;"></div>
        <div class="particle" style="left: 90%; width: 21px; height: 21px; animation-delay: 2.5s;"></div>
    </div>
    
    <div class="gold-header">
        <h1>AURUM</h1>
        <h3>Sistema de Analytics Premium</h3>
        <div style="margin-top: 15px; font-size: 14px; opacity: 0.8;">
            
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login Corporativo")
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário")
            password = st.text_input("🔑 Senha", type="password")
            submit = st.form_submit_button("🚀 ACESSAR DASHBOARD", use_container_width=True)
            
            if submit:
                user = AuthManager.authenticate(username, password)
                if user:
                    st.session_state.user = user
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Credenciais inválidas!")
        
        st.markdown("---")
        st.markdown("""
        ### 👥 Usuários Demo:
        - **Admin**: `aurumadmin` / `admin123` - Acesso Total
        - **Manager**: `aurummanager` / `manager123` - Overview + Marketing  
        - **Viewer**: `aurumviewer` / `viewer123` - Apenas Overview
        """)

def show_dashboard():
    # Tutorial para modo dark (aparece apenas se não foi visto antes)
    if 'dark_mode_tutorial_seen' not in st.session_state:
        st.info("🌙 **Dica:** Para melhor experiência visual, ative o modo dark: Menu ☰ > Settings > Theme > Dark")
        if st.button("✅ Entendi, não mostrar mais"):
            st.session_state.dark_mode_tutorial_seen = True
            st.rerun()
    
    # Inicializar estados
    theme_options = list(ThemeManager.get_themes().keys())
    if 'selected_theme' not in st.session_state or st.session_state.selected_theme not in theme_options:
        st.session_state.selected_theme = theme_options[0]
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "📊 Overview Executivo"
    
    # Aplicar tema primeiro
    theme = ThemeManager.apply_theme(st.session_state.selected_theme)
    
    # Sidebar premium navigation
    with st.sidebar:
        # Logo Aurum dinâmico por tema
        logo_gradient = f"linear-gradient(135deg, {theme['primary']}, {theme['secondary']})"
        st.markdown(f"""
        <div class="logo-gold" style="text-align: center; padding: 20px 0; background: {logo_gradient}; 
                   margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 15px 15px;">
            <h2 style="color: white; font-size: 24px; font-weight: 800; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                      background: none !important; -webkit-text-fill-color: white !important;">🏆 AURUM</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Seletor de tema
        selected_theme = st.selectbox("🎨 Selecionar Tema", theme_options, 
                                     index=theme_options.index(st.session_state.selected_theme))
        if selected_theme != st.session_state.selected_theme:
            st.session_state.selected_theme = selected_theme
            st.rerun()
        
        st.markdown("---")
        
        # Menu navigation
        st.markdown("### 📄 Navegação")
        
        menu_items = []
        if AuthManager.has_permission("overview"):
            menu_items.append({"key": "📊 Overview Executivo", "icon": "🏠", "label": "Dashboard Overview"})
        if AuthManager.has_permission("marketing"):
            menu_items.append({"key": "📱 Marketing Analytics", "icon": "📊", "label": "Marketing Analytics"})
        if AuthManager.has_permission("operational"):
            menu_items.append({"key": "⚙️ Operacional & Vendas", "icon": "⚙️", "label": "Operacional"})
        if AuthManager.has_permission("alerts"):
            menu_items.append({"key": "📞 WhatsApp Alertas", "icon": "📱", "label": "WhatsApp Alertas"})
        if AuthManager.has_permission("reports"):
            menu_items.append({"key": "📄 Relatórios PDF", "icon": "📄", "label": "Relatórios"})
        
        for item in menu_items:
            is_active = st.session_state.selected_page == item["key"]
            if st.button(f"{item['icon']} {item['label']}", 
                        key=f"nav_{item['key']}", 
                        use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.selected_page = item["key"]
                st.rerun()
        
        st.markdown("---")
        
        # User info
        st.markdown("### 👤 Usuário")
        st.markdown(f"**Nome:** {st.session_state.user['name']}")
        st.markdown(f"**Role:** {st.session_state.user['role']}")
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    # Obter página selecionada
    selected_page = st.session_state.selected_page
    
    if selected_page == "📊 Overview Executivo":
        show_overview_page(theme)
    elif selected_page == "📱 Marketing Analytics":
        show_marketing_page(theme) 
    elif selected_page == "⚙️ Operacional & Vendas":
        show_operational_page(theme)
    elif selected_page == "📞 WhatsApp Alertas":
        show_whatsapp_alerts_page(theme)
    elif selected_page == "📄 Relatórios PDF":
        show_pdf_reports_page(theme)

def show_overview_page(theme):
    st.markdown("""
    <div class="gold-header">
        <h1>AURUM</h1>
        <h3>Dashboard Premium - Performance em Tempo Real</h3>
    </div>
    """, unsafe_allow_html=True)
    
    kpis = DataGenerator.generate_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Receita Total</h3>
            <h2>{kpis['Receita Total']}</h2>
            <p style="color: #ffffff; font-weight: 600; opacity: 0.9;">📈 {kpis['Crescimento']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 ROI Médio</h3>
            <h2>{kpis['ROI Google Ads']}</h2>
            <p style="color: #ffffff; font-weight: 600; opacity: 0.9;">Google + Meta Ads</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔄 Conversões</h3>
            <h2>{kpis['Conversões']}</h2>
            <p style="color: #ffffff; font-weight: 600; opacity: 0.9;">Todas as fontes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💎 Ticket Médio</h3>
            <h2>{kpis['Ticket Médio']}</h2>
            <p style="color: #ffffff; font-weight: 600; opacity: 0.9;">CAC: {kpis['CAC']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 LTV</h3>
            <h2>{kpis['LTV']}</h2>
            <p style="color: #ffffff; font-weight: 600; opacity: 0.9;">Lifetime Value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚡ Churn Rate</h3>
            <h2>{kpis['Churn Rate']}</h2>
            <p style="color: #ffffff; font-weight: 600; opacity: 0.9;">Taxa mensal</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐ NPS Score</h3>
            <h2>{kpis['NPS']}</h2>
            <p style="color: #ffffff; font-weight: 600; opacity: 0.9;">Satisfação cliente</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🚀 Status</h3>
            <h2 style="color: #00ff88;">ATIVO</h2>
            <p style="color: #ffffff; font-weight: 600; opacity: 0.9;">Sistema online</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        revenue_data = DataGenerator.generate_time_series()
        fig_revenue = ChartGenerator.create_revenue_chart(theme, revenue_data)
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        channel_data = DataGenerator.generate_channel_data()
        fig_channel = ChartGenerator.create_channel_performance(theme, channel_data)
        st.plotly_chart(fig_channel, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        funnel_data = DataGenerator.generate_funnel_data()
        fig_funnel = ChartGenerator.create_funnel_chart(theme, funnel_data)
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    with col2:
        fig_3d = ChartGenerator.create_3d_scatter(theme, channel_data)
        st.plotly_chart(fig_3d, use_container_width=True)

def show_marketing_page(theme):
    st.markdown(f"""
    <div class="gold-header">
        <h1>MARKETING ANALYTICS</h1>
        <h4>Google Analytics 4 + Meta Business + Performance Intelligence + Attribution Analysis</4>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Premium no topo
    st.markdown("### 📊 **Performance Marketing - Última Semana**")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>💰 Ad Spend Total</h4>
            <h2>R$ 145.760</h2>
            <p style="color: #00ff88;">↗️ +8.4% vs semana anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🎯 ROAS Blended</h4>
            <h2>4.73x</h2>
            <p style="color: #00ff88;">↗️ +12.3% otimização</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🔥 Conversões</h4>
            <h2>2,847</h2>
            <p style="color: #00ff88;">↗️ +18.7% incremento</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4>💎 CPA Médio</h4>
            <h2>R$ 89.40</h2>
            <p style="color: #00ff88;">↘️ -15.2% otimização</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <h4>📈 CTR Geral</h4>
            <h2>3.84%</h2>
            <p style="color: #00ff88;">↗️ +0.8pp melhoria</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <h4>⚡ Impressions</h4>
            <h2>8.9M</h2>
            <p style="color: #00ff88;">↗️ +24.1% alcance</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Google Analytics 4", "📘 Meta Business Suite", "🚀 Performance Intelligence", "🤖 Marketing IA & Previsões"])
    
    with tab1:
        st.markdown("### 📊 **Google Analytics 4 - Dados Avançados**")
        
        # Sub-métricas GA4
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Sessions", "78,456", "↗️ +15.8%", help="Sessões únicas últimos 7 dias")
        with col2:
            st.metric("Engaged Users", "52,891", "↗️ +12.4%", help="Usuários com engajamento >10s")
        with col3:
            st.metric("Events", "425,789", "↗️ +22.1%", help="Total de eventos trackados")
        with col4:
            st.metric("Conversion Rate", "4.87%", "↗️ +0.9pp", help="Taxa conversão geral")
        with col5:
            st.metric("Avg. Session Duration", "3min 42s", "↗️ +18s", help="Duração média engajada")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico Avançado: Attribution por Canal
            attribution_data = pd.DataFrame({
                'Channel': ['Google Ads', 'Meta Ads', 'Organic Search', 'Direct', 'Email', 'LinkedIn', 'YouTube'],
                'First_Touch': [28.5, 22.8, 18.4, 12.7, 8.9, 5.2, 3.5],
                'Last_Touch': [32.1, 26.4, 15.2, 11.8, 7.8, 4.1, 2.6],
                'Linear': [30.2, 24.6, 16.8, 12.2, 8.4, 4.7, 3.1]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='First Touch', x=attribution_data['Channel'], y=attribution_data['First_Touch'],
                               marker_color=theme['primary'], opacity=0.8))
            fig.add_trace(go.Bar(name='Last Touch', x=attribution_data['Channel'], y=attribution_data['Last_Touch'],
                               marker_color=theme['secondary'], opacity=0.8))
            fig.add_trace(go.Bar(name='Linear Attribution', x=attribution_data['Channel'], y=attribution_data['Linear'],
                               marker_color=theme['accent'], opacity=0.8))
            
            fig.update_layout(
                title="🎯 **Modelos de Atribuição - % Conversões**",
                template=theme['plotly_template'],
                barmode='group',
                height=400,
                xaxis_title="Canais de Marketing",
                yaxis_title="% das Conversões"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico: User Journey - Touchpoints
            journey_data = pd.DataFrame({
                'Stage': ['Awareness', 'Interest', 'Consideration', 'Intent', 'Purchase', 'Loyalty'],
                'Google_Ads': [100, 78, 45, 28, 18, 12],
                'Meta_Ads': [100, 82, 52, 34, 22, 15],
                'Organic': [100, 65, 38, 22, 14, 18],
                'Email': [100, 88, 72, 58, 45, 38]
            })
            
            fig = go.Figure()
            for channel in ['Google_Ads', 'Meta_Ads', 'Organic', 'Email']:
                fig.add_trace(go.Scatter(
                    x=journey_data['Stage'],
                    y=journey_data[channel],
                    mode='lines+markers',
                    name=channel.replace('_', ' '),
                    line=dict(width=4),
                    marker=dict(size=10)
                ))
            
            fig.update_layout(
                title="🌟 **Customer Journey - Touchpoints Analysis**",
                template=theme['plotly_template'],
                height=400,
                xaxis_title="Estágio do Funil",
                yaxis_title="Usuários Únicos (Indexado)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Terceiro gráfico: Comportamento por Dispositivo + Demografia
        col1, col2 = st.columns(2)
        
        with col1:
            device_data = pd.DataFrame({
                'Device': ['Desktop', 'Mobile', 'Tablet'],
                'Sessions': [35420, 38950, 4086],
                'Conv_Rate': [5.2, 3.8, 4.1],
                'Avg_Value': [487.30, 312.85, 445.20]
            })
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Bar(x=device_data['Device'], y=device_data['Sessions'], 
                      name="Sessions", marker_color=theme['primary']),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=device_data['Device'], y=device_data['Conv_Rate'], 
                          mode='lines+markers', name="Conv Rate %", 
                          line=dict(color=theme['secondary'], width=4),
                          marker=dict(size=12)),
                secondary_y=True,
            )
            
            fig.update_layout(title="📱 **Performance por Dispositivo**", 
                            template=theme['plotly_template'], height=400)
            fig.update_yaxes(title_text="Sessions", secondary_y=False)
            fig.update_yaxes(title_text="Conversion Rate %", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Demografia Avançada
            demo_data = pd.DataFrame({
                'Age_Group': ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
                'Users': [8540, 23780, 28450, 12850, 6890, 2340],
                'Revenue_per_User': [185.40, 425.80, 567.90, 489.20, 312.70, 245.60],
                'ROAS': [3.2, 4.8, 5.9, 4.4, 3.1, 2.7]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=demo_data['Age_Group'],
                y=demo_data['Users'],
                name='Usuários',
                marker_color=theme['primary'],
                yaxis='y',
                opacity=0.8
            ))
            
            fig.add_trace(go.Scatter(
                x=demo_data['Age_Group'],
                y=demo_data['Revenue_per_User'],
                mode='lines+markers',
                name='Revenue/User',
                line=dict(color=theme['secondary'], width=4),
                marker=dict(size=10),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="👥 **Análise Demográfica - Valor por Usuário**",
                template=theme['plotly_template'],
                height=400,
                yaxis=dict(title="Número de Usuários", side="left"),
                yaxis2=dict(title="Revenue por Usuário (R$)", side="right", overlaying="y")
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 📘 **Meta Business Suite - Performance Detalhada**")
        
        # KPIs Meta específicos
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Spend Total", "R$ 89,450", "↗️ +6.8%", help="Investimento Meta Ads 7 dias")
        with col2:
            st.metric("CPM", "R$ 24.80", "↘️ -8.4%", help="Custo por mil impressões")
        with col3:
            st.metric("Frequency", "2.34", "↗️ +0.12", help="Frequência média de exposição")
        with col4:
            st.metric("Video View Rate", "78.9%", "↗️ +4.2pp", help="Taxa visualização vídeos")
        with col5:
            st.metric("Cost per Result", "R$ 31.45", "↘️ -12.7%", help="Custo por resultado otimizado")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance por Tipo de Campanha
            campaign_performance = pd.DataFrame({
                'Campaign_Type': ['Conversion', 'Video Views', 'Traffic', 'Engagement', 'App Install', 'Lead Gen'],
                'Spend': [34500, 18200, 15800, 12900, 5850, 2200],
                'Results': [1450, 89500, 12800, 23400, 890, 340],
                'CPA': [23.79, 0.20, 1.23, 0.55, 6.57, 6.47],
                'ROAS': [5.2, 2.1, 3.8, 4.4, 7.1, 8.3]
            })
            
            fig = go.Figure()
            
            # Bubble chart: Spend x ROAS, tamanho = Results
            fig.add_trace(go.Scatter(
                x=campaign_performance['Spend'],
                y=campaign_performance['ROAS'],
                mode='markers+text',
                text=campaign_performance['Campaign_Type'],
                textposition='middle center',
                marker=dict(
                    size=campaign_performance['Results']/100,
                    sizemode='diameter',
                    sizeref=2,
                    color=campaign_performance['ROAS'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="ROAS"),
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                hovertemplate="<b>%{text}</b><br>" +
                            "Spend: R$ %{x:,.0f}<br>" +
                            "ROAS: %{y:.1f}x<br>" +
                            "Results: %{marker.size}<br>" +
                            "<extra></extra>"
            ))
            
            fig.update_layout(
                title="💎 **Performance por Tipo de Campanha**<br><sub>Bolha = Quantidade de Resultados | Cor = ROAS</sub>",
                template=theme['plotly_template'],
                height=450,
                xaxis_title="Investment (R$)",
                yaxis_title="ROAS (Return on Ad Spend)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Creative Performance Analysis
            creative_data = pd.DataFrame({
                'Creative_Type': ['Video 15s', 'Video 30s', 'Carousel', 'Single Image', 'Collection', 'Stories'],
                'CTR': [4.2, 3.8, 3.1, 2.9, 3.4, 4.8],
                'CVR': [2.8, 3.1, 2.4, 2.2, 2.6, 3.4],
                'CPC': [1.85, 1.92, 1.67, 1.45, 1.78, 2.12],
                'Impressions': [2850000, 1950000, 1450000, 980000, 650000, 890000]
            })
            
            # Radar Chart para Creative Performance
            fig = go.Figure()
            
            # Normalizar os dados para o radar (0-100 scale)
            normalized_data = creative_data.copy()
            for col in ['CTR', 'CVR', 'CPC']:
                if col == 'CPC':  # Para CPC, menor é melhor, então inverter
                    normalized_data[f'{col}_norm'] = 100 - ((normalized_data[col] - normalized_data[col].min()) / 
                                                           (normalized_data[col].max() - normalized_data[col].min()) * 100)
                else:
                    normalized_data[f'{col}_norm'] = ((normalized_data[col] - normalized_data[col].min()) / 
                                                     (normalized_data[col].max() - normalized_data[col].min()) * 100)
            
            for i, creative in enumerate(creative_data['Creative_Type']):
                fig.add_trace(go.Scatterpolar(
                    r=[normalized_data.iloc[i]['CTR_norm'], 
                       normalized_data.iloc[i]['CVR_norm'],
                       normalized_data.iloc[i]['CPC_norm']],
                    theta=['CTR', 'CVR', 'CPC (Invertido)'],
                    fill='toself',
                    name=creative,
                    line_color=px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                title="🎨 **Performance por Tipo de Creative**<br><sub>Radar normalizado (0-100)</sub>",
                template=theme['plotly_template'],
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Audience Performance
        col1, col2 = st.columns(2)
        
        with col1:
            audience_data = pd.DataFrame({
                'Audience': ['Lookalike 1%', 'Lookalike 2%', 'Interest-based', 'Custom Upload', 'Behavioral', 'Retargeting'],
                'Reach': [1850000, 2450000, 3200000, 890000, 1250000, 450000],
                'Frequency': [1.8, 2.1, 2.8, 1.5, 2.3, 4.2],
                'CPM': [18.50, 22.30, 28.90, 15.20, 25.60, 12.80],
                'CTR': [4.1, 3.8, 2.9, 5.2, 3.4, 6.8]
            })
            
            # 3D Scatter: Reach x Frequency x CTR
            fig = go.Figure(data=[go.Scatter3d(
                x=audience_data['Reach'],
                y=audience_data['Frequency'],
                z=audience_data['CTR'],
                mode='markers+text',
                text=audience_data['Audience'],
                textposition='middle center',
                marker=dict(
                    size=audience_data['CPM']*2,
                    color=audience_data['CTR'],
                    colorscale='Plasma',
                    showscale=True,
                    colorbar=dict(title="CTR %"),
                    opacity=0.8
                ),
                hovertemplate="<b>%{text}</b><br>" +
                            "Reach: %{x:,.0f}<br>" +
                            "Frequency: %{y:.1f}<br>" +
                            "CTR: %{z:.1f}%<br>" +
                            "<extra></extra>"
            )])
            
            fig.update_layout(
                title="🎯 **3D Audience Analysis**<br><sub>Tamanho = CPM | Cor = CTR</sub>",
                template=theme['plotly_template'],
                height=500,
                scene=dict(
                    xaxis_title='Reach',
                    yaxis_title='Frequency',
                    zaxis_title='CTR %'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Placements Performance
            placement_data = pd.DataFrame({
                'Placement': ['Facebook Feed', 'Instagram Feed', 'Stories', 'Reels', 'Messenger', 'Audience Network'],
                'Impressions': [3500000, 2800000, 1900000, 1200000, 450000, 890000],
                'Clicks': [142000, 118000, 95000, 76000, 15000, 28000],
                'Conversions': [4250, 3680, 2850, 2280, 380, 650],
                'Spend': [45600, 38900, 28500, 22100, 4800, 8900]
            })
            
            # Calculate metrics
            placement_data['CTR'] = (placement_data['Clicks'] / placement_data['Impressions'] * 100).round(2)
            placement_data['CVR'] = (placement_data['Conversions'] / placement_data['Clicks'] * 100).round(2)
            placement_data['CPC'] = (placement_data['Spend'] / placement_data['Clicks']).round(2)
            
            # Waterfall Chart for Spend Distribution
            fig = go.Figure(go.Waterfall(
                name = "Spend por Placement",
                orientation = "v",
                measure = ["absolute"] * len(placement_data),
                x = placement_data['Placement'],
                y = placement_data['Spend'],
                text = [f"R$ {spend:,.0f}" for spend in placement_data['Spend']],
                textposition = "outside",
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
            
            fig.update_layout(
                title="💰 **Distribuição de Investimento por Placement**",
                template=theme['plotly_template'],
                height=500,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 🚀 **Performance Intelligence - Cross-Platform Analysis**")
        
        # KPIs Comparativos
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("MER (Marketing Efficiency)", "6.82", "↗️ +0.45", help="Marketing Efficiency Ratio")
        with col2:
            st.metric("Blended CAC", "R$ 73.50", "↘️ -8.3%", help="Customer Acquisition Cost")
        with col3:
            st.metric("LTV/CAC Ratio", "8.4x", "↗️ +1.2x", help="Lifetime Value / CAC")
        with col4:
            st.metric("Payback Period", "2.8 meses", "↘️ -0.4m", help="Tempo recuperação investimento")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Competitive Intelligence Dashboard
            competitive_data = pd.DataFrame({
                'Metric': ['Market Share', 'Ad Spend', 'Creative Variations', 'Audience Overlap', 'Brand Mentions'],
                'Aurum_Company': [12.4, 145760, 45, 100, 8950],
                'Competitor_A': [18.7, 220000, 62, 78, 12400],
                'Competitor_B': [15.2, 185000, 38, 65, 9800],
                'Competitor_C': [9.8, 120000, 28, 45, 6200]
            })
            
            # Normalizar dados para comparação
            metrics_norm = competitive_data.set_index('Metric')
            metrics_norm = metrics_norm.div(metrics_norm.max(axis=1), axis=0) * 100
            
            # Radar Chart Competitivo
            fig = go.Figure()
            
            companies = ['Aurum_Company', 'Competitor_A', 'Competitor_B', 'Competitor_C']
            colors = [theme['primary'], '#ff6b6b', '#4ecdc4', '#45b7d1']
            
            for i, company in enumerate(companies):
                fig.add_trace(go.Scatterpolar(
                    r=metrics_norm[company].tolist(),
                    theta=metrics_norm.index.tolist(),
                    fill='toself',
                    name=company.replace('_', ' '),
                    line_color=colors[i],
                    opacity=0.6
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                title="🏁 **Competitive Intelligence Radar**<br><sub>Performance normalizada (0-100)</sub>",
                template=theme['plotly_template'],
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Incrementality Analysis
            incrementality_data = pd.DataFrame({
                'Test_Group': ['Brand Search', 'Generic Search', 'Social Media', 'Display', 'Video', 'Shopping'],
                'Total_Conversions': [1850, 2400, 1250, 890, 1400, 1100],
                'Incremental_Conversions': [324, 1680, 1125, 780, 1260, 990],
                'Incrementality_Rate': [17.5, 70.0, 90.0, 87.6, 90.0, 90.0],
                'iROAS': [2.1, 4.8, 5.2, 4.1, 4.7, 3.9]
            })
            
            # Bubble Chart: Incrementality vs iROAS
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=incrementality_data['Incrementality_Rate'],
                y=incrementality_data['iROAS'],
                mode='markers+text',
                text=incrementality_data['Test_Group'],
                textposition='middle center',
                marker=dict(
                    size=incrementality_data['Total_Conversions']/50,
                    color=incrementality_data['iROAS'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="iROAS"),
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                hovertemplate="<b>%{text}</b><br>" +
                            "Incrementality: %{x:.1f}%<br>" +
                            "iROAS: %{y:.1f}x<br>" +
                            "Total Conv: %{marker.size}<br>" +
                            "<extra></extra>"
            ))
            
            fig.update_layout(
                title="📈 **Incrementality Analysis**<br><sub>Bolha = Total Conversions | Cor = iROAS</sub>",
                template=theme['plotly_template'],
                height=500,
                xaxis_title="Incrementality Rate (%)",
                yaxis_title="Incremental ROAS"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Advanced Cohort & LTV Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Cohort LTV Analysis
            cohort_ltv_data = pd.DataFrame({
                'Cohort_Month': ['Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24'],
                'Month_0': [89.50, 94.20, 87.80, 92.40, 88.90, 91.10],
                'Month_1': [142.80, 150.60, 138.90, 147.20, 141.50, 145.30],
                'Month_2': [198.40, 208.90, 194.60, 205.80, 197.30, 0],
                'Month_3': [247.60, 261.20, 243.80, 257.40, 0, 0],
                'Month_4': [289.30, 305.40, 285.20, 0, 0, 0],
                'Month_5': [324.80, 342.90, 0, 0, 0, 0]
            })
            
            # Heatmap de LTV Cohorts
            cohort_matrix = cohort_ltv_data.set_index('Cohort_Month').fillna(0)
            
            fig = go.Figure(data=go.Heatmap(
                z=cohort_matrix.values,
                x=['Month 0', 'Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5'],
                y=cohort_matrix.index,
                colorscale='Viridis',
                text=cohort_matrix.values,
                texttemplate="%{text:.1f}",
                textfont={"size":10},
                hovertemplate="Cohort: %{y}<br>Period: %{x}<br>LTV: R$ %{z:.2f}<extra></extra>"
            ))
            
            fig.update_layout(
                title="💎 **LTV Cohort Analysis**<br><sub>Lifetime Value por coorte mensal</sub>",
                template=theme['plotly_template'],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Marketing Mix Modeling
            mmm_data = pd.DataFrame({
                'Channel': ['Google Ads', 'Meta Ads', 'TV', 'Radio', 'OOH', 'Email', 'Organic'],
                'Media_Contribution': [28.5, 24.3, 18.7, 8.9, 6.2, 7.8, 5.6],
                'Base_Business': [15.2, 12.8, 35.6, 22.4, 45.8, 38.9, 67.2],
                'Saturation_Level': [75.8, 68.4, 45.2, 82.1, 38.9, 56.7, 0],
                'Adstock_Effect': [0.85, 0.72, 0.95, 0.68, 0.45, 0.32, 0]
            })
            
            # Stacked bar para MMM
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Media Contribution',
                x=mmm_data['Channel'],
                y=mmm_data['Media_Contribution'],
                marker_color=theme['primary']
            ))
            
            fig.add_trace(go.Bar(
                name='Base Business',
                x=mmm_data['Channel'],
                y=mmm_data['Base_Business'],
                marker_color=theme['secondary']
            ))
            
            fig.update_layout(
                title="🧮 **Marketing Mix Model - Contribution Analysis**<br><sub>% Contribuição para receita total</sub>",
                template=theme['plotly_template'],
                height=400,
                barmode='stack',
                yaxis_title="% Contribution to Revenue"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 🤖 **MARKETING IA & PREVISÕES - Maximize seu ROI com Inteligência Artificial**")
        
        # Box de Insights Marketing IA
        st.markdown("""
        <div style="background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}); padding: 20px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin-bottom: 15px;">🚀 <strong>IA Marketing Detectou Oportunidades Valiosas:</strong></h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 10px;">
                    <h4 style="color: #ffffff; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">💰 Budget Mal Alocado Identificado</h4>
                    <p style="color: white; margin: 5px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">Realocando R$ 12K para campanhas high-performing, você pode <strong>aumentar 34% no ROAS</strong> sem investir 1 centavo a mais</p>
                </div>
                <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 10px;">
                    <h4 style="color: #ffffff; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">⏰ Timing Perfeito Descoberto</h4>
                    <p style="color: white; margin: 5px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">IA identificou o horário ideal para seus anúncios. Mudança simples pode <strong>gerar +R$ 85K</strong> nos próximos 90 dias</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # KPIs Marketing IA - Valores Realísticos
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>💸 Desperdício Evitado</h4>
                <h2>R$ 18.5K</h2>
                <p style="color: {theme['secondary']};">↗️ Economia mensalmente</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🎯 ROAS Otimizado</h4>
                <h2>5.2x</h2>
                <p style="color: {theme['secondary']};">↗️ vs 4.2x sem IA</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🚀 Revenue Incremental</h4>
                <h2>R$ 125K</h2>
                <p style="color: {theme['secondary']};">↗️ Próximos 3 meses</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h4>⚡ CTR Boost</h4>
                <h2>+28%</h2>
                <p style="color: {theme['secondary']};">↗️ Com otimização IA</p>
            </div>
            """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <h4>💎 Conversão Lift</h4>
                <h2>+18%</h2>
                <p style="color: {theme['secondary']};">↗️ IA targeting</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Budget Reallocation - Muito Claro
            st.markdown("### 💰 **Como Realocar seu Budget para Máximo ROI**")
            
            budget_otimizacao = pd.DataFrame({
                'Canal': ['Google Search Brand', 'Meta Lookalike', 'Google Shopping', 'Meta Interest', 
                         'Google Display', 'YouTube Video', 'Email Marketing'],
                'Budget_Atual': [45000, 38000, 32000, 28000, 22000, 18000, 12000],
                'Budget_Otimizado_IA': [65000, 55000, 28000, 35000, 15000, 25000, 22000],
                'ROAS_Atual': [8.2, 5.9, 6.1, 4.8, 4.2, 3.9, 7.1],
                'ROAS_Previsto_IA': [9.8, 7.2, 6.8, 5.9, 4.8, 5.4, 8.9],
                'Diferenca_Budget': [20000, 17000, -4000, 7000, -7000, 7000, 10000]
            })
            
            # Criar gráfico de barras comparativo
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=budget_otimizacao['Canal'],
                y=budget_otimizacao['Budget_Atual'],
                name='💸 Budget Atual (Subótimo)',
                marker_color='#ff6b6b',
                opacity=0.7,
                text=[f"R$ {val:,.0f}" for val in budget_otimizacao['Budget_Atual']],
                textposition='inside',
                textfont=dict(color='white', size=10)
            ))
            
            fig.add_trace(go.Bar(
                x=budget_otimizacao['Canal'],
                y=budget_otimizacao['Budget_Otimizado_IA'],
                name='🚀 Budget Otimizado IA',
                marker_color='#00ff88',
                opacity=0.9,
                text=[f"R$ {val:,.0f}" for val in budget_otimizacao['Budget_Otimizado_IA']],
                textposition='inside',
                textfont=dict(color='white', size=10, family='Arial Black')
            ))
            
            fig.update_layout(
                title="💸 <b>Realocação Inteligente de Budget</b><br><sub>Verde = Como deveria ser | Vermelho = Como está hoje</sub>",
                template=theme['plotly_template'],
                height=450,
                xaxis_title="Canais de Marketing",
                yaxis_title="Investment Mensal (R$)",
                xaxis_tickangle=-45,
                barmode='group',
                yaxis_tickformat=',.0f'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Resumo do Impacto
            total_revenue_lift = sum(budget_otimizacao['Diferenca_Budget']) * 0.15  # Estimativa conservadora
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4caf50, #45a049); padding: 15px; border-radius: 12px; margin-top: 10px;">
                <h4 style="color: white; text-align: center; margin: 0;">
                    🎯 <strong>IMPACTO DA OTIMIZAÇÃO:</strong><br>
                    <span style="font-size: 24px;">+R$ {total_revenue_lift*12:,.0f}/ano</span><br>
                    <span style="font-size: 14px;">sem aumentar o budget total!</span>
                </h4>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Timing Optimization - Quando Anunciar
            st.markdown("### ⏰ **Quando seus Clientes Mais Compram? Otimização de Timing**")
            
            # Dados de timing por hora (24 horas)
            timing_data = pd.DataFrame({
                'Hora': list(range(24)),
                'Conversoes_Atuais': [12, 8, 6, 4, 5, 8, 15, 28, 45, 52, 48, 55, 62, 58, 65, 78, 85, 92, 88, 75, 65, 45, 32, 18],
                'Potencial_IA': [18, 12, 9, 6, 7, 12, 22, 42, 68, 78, 72, 82, 93, 87, 98, 117, 128, 138, 132, 113, 98, 68, 48, 27]
            })
            
            fig = go.Figure()
            
            # Conversões atuais
            fig.add_trace(go.Scatter(
                x=[f"{h:02d}h" for h in timing_data['Hora']],
                y=timing_data['Conversoes_Atuais'],
                mode='lines+markers',
                name='📊 Performance Atual',
                line=dict(color=theme['primary'], width=3),
                marker=dict(size=8),
                fill='tonexty'
            ))
            
            # Potencial com IA
            fig.add_trace(go.Scatter(
                x=[f"{h:02d}h" for h in timing_data['Hora']],
                y=timing_data['Potencial_IA'],
                mode='lines+markers',
                name='🚀 Potencial com IA',
                line=dict(color='#00ff88', width=4),
                marker=dict(size=10),
                fill='tonexty'
            ))
            
            # Destacar os melhores horários
            peak_hours = [16, 17, 18, 19]  # 16h-19h
            for hour in peak_hours:
                fig.add_vrect(
                    x0=hour-0.4, x1=hour+0.4,
                    fillcolor=theme['accent'],
                    opacity=0.2,
                    layer="below",
                    line_width=0,
                    annotation_text="PICO" if hour == 17 else "",
                    annotation_position="top"
                )
            
            fig.update_layout(
                title="⏰ <b>Timing Perfeito para seus Anúncios</b><br><sub>Área dourada = horários de pico | Área verde = oportunidade perdida</sub>",
                template=theme['plotly_template'],
                height=450,
                xaxis_title="Horário do Dia",
                yaxis_title="Conversões por Hora",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Dicas de Timing
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ff9800, #f57c00); padding: 15px; border-radius: 10px;">
                <h4 style="color: white; margin-bottom: 10px;">⏰ <strong>Otimizações de Timing IA:</strong></h4>
                <ul style="color: white; margin: 0; padding-left: 20px;">
                    <li><strong>16h-19h:</strong> PICO! Aumente budget +150% neste horário</li>
                    <li><strong>12h-14h:</strong> Bom para B2B, reduza B2C</li>
                    <li><strong>0h-6h:</strong> Pausa total - economia de 40% no CPM</li>
                    <li><strong>Weekend:</strong> Apenas campanhas brand/awareness</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Audience Insights e Creative Optimization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 **Qual Público Rende Mais? Análise de Audiências IA**")
            
            audience_performance = pd.DataFrame({
                'Audience': ['Lookalike 1% Compradores', 'Interest: Business Software', 'Retargeting 30 dias', 
                           'Custom Upload CRM', 'Lookalike 3% Website', 'Broad Audience', 'Competitors Audience'],
                'Spend_Mensal': [8500, 6800, 5500, 4800, 5200, 7500, 3500],
                'ROAS': [7.8, 5.4, 9.2, 6.9, 4.1, 2.8, 4.5],
                'CPA': [89, 125, 67, 98, 156, 234, 178],
                'Volume_Potencial': [85, 65, 40, 55, 90, 100, 45],
                'Recomendacao_IA': ['🚀 ESCALAR', '✅ MANTER', '💎 PREMIUM', '🔥 AUMENTAR', 
                                   '⚠️ REDUZIR', '❌ PAUSAR', '🔄 TESTAR']
            })
            
            # Bubble chart: ROAS vs Volume Potencial
            cores_recomendacao = {
                '🚀 ESCALAR': theme['secondary'],
                '✅ MANTER': theme['primary'],
                '💎 PREMIUM': theme['accent'],
                '🔥 AUMENTAR': '#ff9500',
                '⚠️ REDUZIR': '#ffd700',
                '❌ PAUSAR': '#ff6b6b',
                '🔄 TESTAR': '#9c27b0'
            }
            
            fig = go.Figure()
            
            for recomendacao in audience_performance['Recomendacao_IA'].unique():
                df_rec = audience_performance[audience_performance['Recomendacao_IA'] == recomendacao]
                fig.add_trace(go.Scatter(
                    x=df_rec['Volume_Potencial'],
                    y=df_rec['ROAS'],
                    mode='markers+text',
                    text=df_rec['Audience'].str.replace(' ', '<br>'),
                    textposition='middle center',
                    name=recomendacao,
                    marker=dict(
                        size=df_rec['Spend_Mensal']/1000,
                        color=cores_recomendacao.get(recomendacao, '#666666'),
                        opacity=0.8,
                        line=dict(width=2, color='white')
                    ),
                    hovertemplate="<b>%{text}</b><br>" +
                                "Volume Potencial: %{x}%<br>" +
                                "ROAS: %{y:.1f}x<br>" +
                                "Spend: R$ %{marker.size}<br>" +
                                "<extra></extra>"
                ))
            
            fig.update_layout(
                title="🎯 <b>Mapa de Performance de Audiências</b><br><sub>Tamanho = Budget | Posição = Desempenho</sub>",
                template=theme['plotly_template'],
                height=450,
                xaxis_title="Volume Potencial (%)",
                yaxis_title="ROAS (Return on Ad Spend)",
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎨 **Quais Criativos Vendem Mais? Creative Intelligence**")
            
            creative_insights = pd.DataFrame({
                'Tipo_Creative': ['Video 15s Produto', 'Carousel 3 produtos', 'Single Image + CTA', 
                                'Video 30s Depoimento', 'Collection Showcase', 'Stories Vertical',
                                'Image + Social Proof'],
                'CTR': [4.8, 3.2, 2.9, 5.1, 3.8, 6.2, 3.5],
                'CVR': [3.4, 4.1, 2.8, 4.7, 3.9, 2.1, 3.2],
                'CPC': [1.45, 1.89, 2.15, 1.32, 1.67, 1.98, 1.78],
                'Revenue_Gerada': [45600, 32800, 18900, 51200, 29800, 16700, 23400],
                'Trend_Momentum': ['+89%', '+34%', '-12%', '+156%', '+67%', '+234%', '+45%']
            })
            
            # Calcular score de performance
            creative_insights['Performance_Score'] = (
                creative_insights['CTR'] * 0.3 + 
                creative_insights['CVR'] * 0.4 + 
                (1/creative_insights['CPC']) * 0.3
            ) * 10
            
            # Radar chart comparativo
            fig = go.Figure()
            
            # Top 4 performers
            top_creatives = creative_insights.nlargest(4, 'Performance_Score')
            colors = [theme['secondary'], theme['accent'], '#ff9500', theme['primary']]
            
            for i, (idx, creative) in enumerate(top_creatives.iterrows()):
                fig.add_trace(go.Scatterpolar(
                    r=[creative['CTR'], creative['CVR'], (1/creative['CPC'])*10, creative['Revenue_Gerada']/100000],
                    theta=['CTR %', 'CVR %', 'CPC Score', 'Revenue (100k)'],
                    fill='toself',
                    name=creative['Tipo_Creative'],
                    line_color=colors[i],
                    opacity=0.6
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 8]
                    )),
                title="🏆 <b>Top Creative Performers</b><br><sub>Quanto maior a área, melhor o creative</sub>",
                template=theme['plotly_template'],
                height=450,
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Previsão de Spending Otimizado
        st.markdown("---")
        st.markdown("### 💰 **Previsão de Budget Otimizado - Próximos 6 Meses**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            spending_forecast = pd.DataFrame({
                'Mes': ['Outubro', 'Novembro', 'Dezembro', 'Janeiro', 'Fevereiro', 'Março'],
                'Spend_Atual': [14500, 15000, 16000, 14000, 14500, 15000],
                'Spend_Otimizado_IA': [14500, 16500, 19500, 12500, 15500, 18500],
                'Revenue_Atual': [62000, 67500, 72000, 58800, 60900, 64500],
                'Revenue_IA': [89000, 105000, 134000, 78500, 102000, 129000]
            })
            
            fig = go.Figure()
            
            # Revenue atual vs IA
            fig.add_trace(go.Scatter(
                x=spending_forecast['Mes'],
                y=spending_forecast['Revenue_Atual'],
                mode='lines+markers',
                name='💸 Revenue Atual (sem otimização)',
                line=dict(color=theme['accent'], width=4),
                marker=dict(size=10)
            ))
            
            fig.add_trace(go.Scatter(
                x=spending_forecast['Mes'],
                y=spending_forecast['Revenue_IA'],
                mode='lines+markers',
                name='🚀 Revenue com IA Optimization',
                line=dict(color=theme['secondary'], width=5),
                marker=dict(size=12),
                fill='tonexty'
            ))
            
            # Anotações de ganho
            for i, mes in enumerate(spending_forecast['Mes']):
                revenue_ia = float(spending_forecast.iloc[i]['Revenue_IA'])
                revenue_atual = float(spending_forecast.iloc[i]['Revenue_Atual'])
                ganho = revenue_ia - revenue_atual
                fig.add_annotation(
                    x=mes,
                    y=revenue_ia,
                    text=f"<b>+R$ {ganho:,.0f}</b>",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor=theme['accent'],
                    bgcolor=theme['accent'],
                    bordercolor=theme['accent'],
                    font=dict(color="black", size=10)
                )
            
            fig.update_layout(
                title="📈 <b>Impacto da Otimização IA no Revenue</b><br><sub>Área verde = dinheiro extra que você vai ganhar</sub>",
                template=theme['plotly_template'],
                height=400,
                xaxis_title="Próximos 6 Meses",
                yaxis_title="Revenue Mensal (R$)",
                yaxis_tickformat=',.0f'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Resumo de Impacto Total
            revenue_ia_total = sum([float(x) for x in spending_forecast['Revenue_IA']])
            revenue_atual_total = sum([float(x) for x in spending_forecast['Revenue_Atual']])
            total_ganho = revenue_ia_total - revenue_atual_total
            total_spend_atual = sum([float(x) for x in spending_forecast['Spend_Atual']])
            roi_melhoria = (total_ganho / total_spend_atual) * 100
            
            # RESUMO EXECUTIVO usando container nativo do Streamlit
            with st.container():
                st.markdown(
                    f"<div style='background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}); "
                    f"padding: 20px; border-radius: 15px; text-align: center; color: white; "
                    f"box-shadow: 0 8px 32px rgba(0,0,0,0.25); margin: 10px 0; "
                    f"border: 3px solid rgba(255,255,255,0.1);'>"
                    f"<h2 style='margin: 10px 0; color: #ffffff; "
                    f"background: rgba(0,0,0,0.7); padding: 8px 15px; "
                    f"border-radius: 8px; display: inline-block; "
                    f"text-shadow: 2px 2px 4px rgba(255,255,255,0.3), "
                    f"0 0 10px rgba(255,255,255,0.2); "
                    f"font-weight: 900; font-size: 24px; "
                    f"border: 1px solid rgba(255,255,255,0.2);'>"
                    f"🎯 <strong>RESUMO EXECUTIVO</strong></h2></div>",
                    unsafe_allow_html=True
                )
                
                # Usar colunas para organizar as métricas
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.markdown(
                        f"<div style='text-align: center; background: rgba(0,0,0,0.8); "
                        f"padding: 15px; border-radius: 10px; margin: 5px; "
                        f"border: 3px solid {theme['primary']}; "
                        f"box-shadow: 0 4px 20px rgba(0,0,0,0.4);'>"
                        f"<h3 style='color: #ffffff; font-size: 28px; margin: 0; "
                        f"font-weight: 900;'>+R$ {total_ganho:,.0f}</h3>"
                        f"<p style='color: #cccccc; font-size: 14px; margin: 5px 0; "
                        f"font-weight: 600;'>Revenue adicional em 6 meses</p></div>",
                        unsafe_allow_html=True
                    )
                
                with col_b:
                    st.markdown(
                        f"<div style='text-align: center; background: rgba(0,0,0,0.8); "
                        f"padding: 15px; border-radius: 10px; margin: 5px; "
                        f"border: 3px solid {theme['secondary']}; "
                        f"box-shadow: 0 4px 20px rgba(0,0,0,0.4);'>"
                        f"<h3 style='color: #ffffff; font-size: 28px; margin: 0; "
                        f"font-weight: 900;'>{roi_melhoria:.0f}%</h3>"
                        f"<p style='color: #cccccc; font-size: 14px; margin: 5px 0; "
                        f"font-weight: 600;'>Melhoria no ROI</p></div>",
                        unsafe_allow_html=True
                    )
                
                with col_c:
                    st.markdown(
                        f"<div style='text-align: center; background: rgba(0,0,0,0.8); "
                        f"padding: 15px; border-radius: 10px; margin: 5px; "
                        f"border: 3px solid {theme['accent']}; "
                        f"box-shadow: 0 4px 20px rgba(0,0,0,0.4);'>"
                        f"<h3 style='color: #ffffff; font-size: 28px; margin: 0; "
                        f"font-weight: 900;'>R$ 0</h3>"
                        f"<p style='color: #cccccc; font-size: 14px; margin: 5px 0; "
                        f"font-weight: 600;'>Investimento adicional</p></div>",
                        unsafe_allow_html=True
                    )
                
                st.markdown(
                    "<p style='text-align: center; font-style: italic; "
                    "background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; "
                    "color: #333333; margin-top: 10px; font-weight: 600; "
                    "border: 1px solid rgba(0,0,0,0.1);'>"
                    "* Apenas otimização inteligente dos investimentos atuais</p>",
                    unsafe_allow_html=True
                )
        
        # SEÇÃO DE AÇÕES - FINAL DA ANÁLISE DE MARKETING
        st.markdown("---")
        st.markdown("### 🎯 **PLANO DE AÇÃO - MARKETING IA**")
        st.markdown("📅 ***Suas próximas ações prioritárias baseadas em todas as análises acima***")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚀 **Ações de Crescimento Imediato**")
            
            # Ações de Criativos (movido para cá)
            creative_insights = pd.DataFrame({
                'Tipo_Creative': ['Video 15s Produto', 'Carousel 3 produtos', 'Single Image + CTA', 
                                'Video 30s Depoimento', 'Collection Showcase', 'Stories Vertical',
                                'Image + Social Proof'],
                'CTR': [4.8, 3.2, 2.9, 5.1, 3.8, 6.2, 3.5],
                'CVR': [3.4, 4.1, 2.8, 4.7, 3.9, 2.1, 3.2],
                'CPC': [1.45, 1.89, 2.15, 1.32, 1.67, 1.98, 1.78],
                'Revenue_Gerada': [45600, 32800, 18900, 51200, 29800, 16700, 23400],
                'Trend_Momentum': ['+89%', '+34%', '-12%', '+156%', '+67%', '+234%', '+45%']
            })
            
            # Calcular score de performance
            creative_insights['Performance_Score'] = (
                creative_insights['CTR'] * 0.3 + 
                creative_insights['CVR'] * 0.4 + 
                (1/creative_insights['CPC']) * 0.3
            ) * 10
            
            # Top 3 recomendações com cores alternadas
            top_3 = creative_insights.nlargest(3, 'Performance_Score')
            colors_patterns = [
                f"linear-gradient(135deg, {theme['primary']}, {theme['secondary']})",  # 1º banner
                f"linear-gradient(135deg, {theme['accent']}, {theme['primary']})",    # 2º banner (diferente)
                f"linear-gradient(135deg, {theme['primary']}, {theme['secondary']})"   # 3º banner (igual ao 1º)
            ]
            
            for i, (idx, creative) in enumerate(top_3.iterrows()):
                momentum_color = '#ffffff' if '+' in creative['Trend_Momentum'] else '#ffcccc'
                background_color = colors_patterns[i]
                st.markdown(f"""
                <div style="background: {background_color}; padding: 12px; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <h4 style="color: white; margin: 0 0 5px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                        🏆 <strong>{creative['Tipo_Creative']}</strong>
                    </h4>
                    <p style="color: white; margin: 0; font-size: 12px; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                        🎯 <strong>Ação:</strong> ESCALAR - Aumentar budget +50%<br>
                        📊 <strong>Performance:</strong> CTR {creative['CTR']:.1f}% | CVR {creative['CVR']:.1f}% | 
                        <span style="color: {momentum_color}; font-weight: bold;">Momentum {creative['Trend_Momentum']}</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📊 **Ações de Otimização IA**")
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {theme['accent']}, {theme['primary']}); padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <h4 style="color: white; margin-bottom: 10px;">⏰ <strong>Timing Perfeito:</strong></h4>
                <ul style="color: white; margin: 0; padding-left: 20px; font-size: 13px;">
                    <li><strong>16h-19h:</strong> PICO! Aumente budget +150% neste horário</li>
                    <li><strong>12h-14h:</strong> Bom para B2B, reduza B2C</li>
                    <li><strong>0h-6h:</strong> Pausa total - economia de 40% no CPM</li>
                </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, {theme['secondary']}, {theme['accent']}); padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <h4 style="color: white; margin-bottom: 10px;">🎯 <strong>Audiências TOP:</strong></h4>
                <ul style="color: white; margin: 0; padding-left: 20px; font-size: 13px;">
                    <li><strong>Lookalike 1% Compradores:</strong> ESCALAR AGORA</li>
                    <li><strong>Retargeting 30 dias:</strong> Audiência PREMIUM</li>
                    <li><strong>Custom Upload CRM:</strong> Aumentar investimento</li>
                </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, {theme['primary']}, {theme['accent']}); padding: 15px; border-radius: 10px;">
                <h4 style="color: white; margin-bottom: 10px;">💰 <strong>Budget Inteligente:</strong></h4>
                <ul style="color: white; margin: 0; padding-left: 20px; font-size: 13px;">
                    <li><strong>Potencial Adicional:</strong> +R$ 127K em 6 meses</li>
                    <li><strong>ROI Esperado:</strong> 385% de retorno</li>
                    <li><strong>Investimento:</strong> R$ 0 adicional (apenas otimização)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_operational_page(theme):
    st.markdown(f"""
    <div class="gold-header">
        <h1>OPERACIONAL & VENDAS</h1>
        <h4>Sales Intelligence + Revenue Operations + Predictive Analytics + Team Performance</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Premium Operacionais no topo
    st.markdown("### 📊 **Performance Operacional - Overview Executivo**")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>💰 Pipeline Total</h4>
            <h2>R$ 2.8M</h2>
            <p style="color: #00ff88;">↗️ +28.4% vs mês anterior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🎯 Win Rate</h4>
            <h2>34.7%</h2>
            <p style="color: #00ff88;">↗️ +6.2pp melhoria</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>⚡ Cycle Time</h4>
            <h2>16.3 dias</h2>
            <p style="color: #00ff88;">↘️ -3.8d otimização</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4>💎 ACV (Deal Size)</h4>
            <h2>R$ 42.8K</h2>
            <p style="color: #00ff88;">↗️ +18.9% crescimento</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <h4>📈 ARR Growth</h4>
            <h2>127%</h2>
            <p style="color: #00ff88;">↗️ +12pp YoY</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🔥 Quota Attainment</h4>
            <h2>108.4%</h2>
            <p style="color: #00ff88;">↗️ +8.4pp vs target</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Sales Operations", "🤖 AI/ML Forecasting", "🏆 Revenue Analytics", "👥 Team Intelligence"])
    
    with tab1:
        st.markdown("### 🏢 **Sales Operations - Pipeline & Performance Intelligence**")
        
        # Sub-métricas Operacionais
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Leads Qualificados", "1,247", "↗️ +22.8%", help="MQLs convertidos para SQLs")
        with col2:
            st.metric("Oportunidades Criadas", "384", "↗️ +15.4%", help="SQLs convertidos para oportunidades")
        with col3:
            st.metric("Demos Agendadas", "156", "↗️ +18.7%", help="Reuniões de descoberta agendadas")
        with col4:
            st.metric("Proposals Enviadas", "89", "↗️ +12.3%", help="Propostas comerciais ativas")
        with col5:
            st.metric("Contratos Fechados", "31", "↗️ +25.8%", help="Deals won últimos 30 dias")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Advanced Pipeline Analysis - Waterfall
            pipeline_stages = pd.DataFrame({
                'Stage': ['Lead', 'MQL', 'SQL', 'Opportunity', 'Demo', 'Proposal', 'Negotiation', 'Closed Won'],
                'Count': [5420, 1680, 847, 384, 156, 89, 52, 31],
                'Value': [0, 8900000, 4850000, 2800000, 1950000, 1450000, 890000, 650000],
                'Conversion_Rate': [100, 31.0, 50.4, 45.3, 40.6, 57.1, 58.4, 59.6]
            })
            
            # Funnel Chart mais sofisticado
            fig = go.Figure()
            
            # Usar cores gradientes para cada estágio
            colors = [theme['primary'], theme['secondary'], theme['accent'], '#ff6b6b', 
                     '#4ecdc4', '#45b7d1', '#f7b731', '#5f27cd']
            
            fig.add_trace(go.Funnel(
                y=pipeline_stages['Stage'],
                x=pipeline_stages['Count'],
                text=[f"{count}<br>{rate:.1f}%" for count, rate in zip(pipeline_stages['Count'], pipeline_stages['Conversion_Rate'])],
                textinfo="text",
                marker_color=colors[:len(pipeline_stages)],
                connector_line_color="rgba(255,255,255,0.3)",
                connector_line_width=2,
            ))
            
            fig.update_layout(
                title="🔥 **Sales Funnel Intelligence**<br><sub>Quantidade + Taxa de Conversão por Estágio</sub>",
                template=theme['plotly_template'],
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Performance por Vendedor - Scatter Bubble
            sales_performance = pd.DataFrame({
                'Vendedor': ['Ana Silva', 'João Santos', 'Maria Costa', 'Pedro Lima', 'Lucas Oliveira', 
                           'Carla Mendes', 'Rafael Torres', 'Juliana Rocha', 'Marcos Alves', 'Beatriz Cunha'],
                'Revenue_Closed': [285000, 245000, 312000, 198000, 267000, 189000, 334000, 256000, 221000, 298000],
                'Pipeline_Value': [450000, 380000, 520000, 290000, 415000, 310000, 580000, 420000, 360000, 475000],
                'Deals_Count': [8, 6, 9, 5, 7, 4, 10, 8, 6, 9],
                'Win_Rate': [72.5, 68.2, 78.9, 62.1, 74.3, 58.7, 82.4, 76.8, 65.9, 79.2],
                'Quota_Attainment': [128.5, 108.7, 142.3, 89.2, 119.8, 85.6, 156.7, 134.2, 96.4, 139.1]
            })
            
            # 3D Scatter: Revenue vs Pipeline vs Win Rate
            fig = go.Figure(data=[go.Scatter3d(
                x=sales_performance['Revenue_Closed'],
                y=sales_performance['Pipeline_Value'],
                z=sales_performance['Win_Rate'],
                mode='markers+text',
                text=sales_performance['Vendedor'],
                textposition='middle center',
                marker=dict(
                    size=sales_performance['Deals_Count']*3,
                    color=sales_performance['Quota_Attainment'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="Quota %"),
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                hovertemplate="<b>%{text}</b><br>" +
                            "Revenue: R$ %{x:,.0f}<br>" +
                            "Pipeline: R$ %{y:,.0f}<br>" +
                            "Win Rate: %{z:.1f}%<br>" +
                            "<extra></extra>"
            )])
            
            fig.update_layout(
                title="🎯 **3D Sales Performance Matrix**<br><sub>Tamanho = Deals | Cor = Quota Attainment</sub>",
                template=theme['plotly_template'],
                height=500,
                scene=dict(
                    xaxis_title='Revenue Closed (R$)',
                    yaxis_title='Pipeline Value (R$)',
                    zaxis_title='Win Rate (%)'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Análise de Velocity e Lead Sources
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales Velocity por Segmento
            velocity_data = pd.DataFrame({
                'Segment': ['Enterprise', 'Mid-Market', 'SMB', 'Startup'],
                'Avg_Deal_Size': [125000, 45000, 18500, 8500],
                'Sales_Cycle': [45, 28, 16, 12],
                'Win_Rate': [65.8, 72.4, 84.2, 89.5],
                'Velocity_Score': [188.4, 123.7, 98.2, 63.4]  # Deal Size * Win Rate / Cycle
            })
            
            # Bubble Chart: Deal Size vs Sales Cycle
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=velocity_data['Sales_Cycle'],
                y=velocity_data['Avg_Deal_Size'],
                mode='markers+text',
                text=velocity_data['Segment'],
                textposition='middle center',
                marker=dict(
                    size=velocity_data['Win_Rate'],
                    color=velocity_data['Velocity_Score'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Velocity Score"),
                    opacity=0.8,
                    line=dict(width=2, color='white'),
                    sizemode='diameter',
                    sizeref=2
                ),
                hovertemplate="<b>%{text}</b><br>" +
                            "Cycle: %{x} dias<br>" +
                            "Deal Size: R$ %{y:,.0f}<br>" +
                            "Win Rate: %{marker.size:.1f}%<br>" +
                            "<extra></extra>"
            ))
            
            fig.update_layout(
                title="⚡ **Sales Velocity by Segment**<br><sub>Bolha = Win Rate | Cor = Velocity Score</sub>",
                template=theme['plotly_template'],
                height=400,
                xaxis_title="Average Sales Cycle (dias)",
                yaxis_title="Average Deal Size (R$)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Lead Source Performance
            lead_source_data = pd.DataFrame({
                'Source': ['Inbound Marketing', 'Outbound SDR', 'Referral Program', 'Partner Channel', 
                          'Events/Trade Shows', 'Social Media', 'Website Direct', 'Email Campaigns'],
                'Leads_Generated': [1250, 890, 340, 560, 280, 430, 380, 290],
                'SQL_Conversion': [24.5, 18.7, 45.8, 32.1, 28.9, 16.2, 21.3, 19.8],
                'Avg_Deal_Value': [38500, 42000, 58000, 45500, 52000, 28500, 35000, 31500],
                'CAC': [485, 890, 120, 650, 1200, 285, 180, 350]
            })
            
            # Calculate ROI
            lead_source_data['ROI'] = ((lead_source_data['Leads_Generated'] * 
                                       lead_source_data['SQL_Conversion']/100 * 
                                       lead_source_data['Avg_Deal_Value']) / 
                                      (lead_source_data['Leads_Generated'] * lead_source_data['CAC'])) * 100
            
            # Stacked Bar com ROI line
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(x=lead_source_data['Source'], y=lead_source_data['Leads_Generated'], 
                      name="Leads Generated", marker_color=theme['primary'], opacity=0.7),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=lead_source_data['Source'], y=lead_source_data['ROI'], 
                          mode='lines+markers', name="ROI %", 
                          line=dict(color=theme['secondary'], width=4),
                          marker=dict(size=10)),
                secondary_y=True,
            )
            
            fig.update_layout(
                title="📈 **Lead Source Performance & ROI**<br><sub>Volume vs Retorno por Canal</sub>", 
                template=theme['plotly_template'], 
                height=400,
                xaxis_tickangle=-45
            )
            fig.update_yaxes(title_text="Leads Generated", secondary_y=False)
            fig.update_yaxes(title_text="ROI (%)", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🤖 **INTELIGÊNCIA ARTIFICIAL - Previsões que Aumentam seu Faturamento**")
        st.markdown("🎤 ***Sua equipe de vendas turbinada por IA - Decisões inteligentes que geram mais receita***")
        
        # Insights de Impacto Financeiro Claro
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3c72, #2a5298); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h3 style="color: white; margin-bottom: 15px;">💡 <strong>Insights da IA que Geram Receita Imediata:</strong></h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                    <h4 style="color: #00ff88; margin: 0;">📈 Oportunidade Perdida Identificada</h4>
                    <p style="color: white; margin: 5px 0;">Focando nos deals com +85% de probabilidade, você pode <strong>aumentar 28% nas vendas</strong> nos próximos 60 dias</p>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                    <h4 style="color: #ffd700; margin: 0;">⚡ Ação Recomendada Urgente</h4>
                    <p style="color: white; margin: 5px 0;">3 deals no pipeline estão perdendo momentum. Agir AGORA pode <strong>salvar R$ 145K</strong> em receita</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # KPIs de Impacto Financeiro Direto
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>💰 Receita Prevista Próximos 90 dias</h4>
                <h2>R$ 485K</h2>
                <p style="color: {theme['secondary']};">↗️ +R$ 125K vs sem IA</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🎯 Deals "Quentes" para Fechar</h4>
                <h2>7 deals</h2>
                <p style="color: {theme['secondary']};">↗️ R$ 285K em valor</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>⚠️ Deals em Risco</h4>
                <h2>3 deals</h2>
                <p style="color: {theme['accent']};">⚠️ R$ 145K podem ser perdidos</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🔥 ROI da IA em Vendas</h4>
                <h2>425%</h2>
                <p style="color: {theme['secondary']};">↗️ Cada R$ 1 investido retorna R$ 4,25</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Seção Principal: Previsões Financeiras
        st.markdown("---")
        st.markdown("### 💰 **PREVISÕES FINANCEIRAS INTELIGENTES**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Previsão Clara e Impactante
            st.markdown("### 📈 **Receita Garantida vs Receita Potencial - Próximos 6 Meses**")
            
            forecast_months = ['Outubro', 'Novembro', 'Dezembro', 'Janeiro', 'Fevereiro', 'Março']
            receita_garantida = [148000, 162000, 175000, 189000, 210000, 228000]  # Deals com +80% prob
            receita_potencial = [210000, 234000, 258000, 280000, 315000, 342000]  # Se otimizar pipeline
            diferenca = [pot - gar for pot, gar in zip(receita_potencial, receita_garantida)]
            
            fig = go.Figure()
            
            # Receita Garantida
            fig.add_trace(go.Scatter(
                x=forecast_months,
                y=receita_garantida,
                mode='lines+markers',
                name='✅ Receita Garantida (80%+ probabilidade)',
                line=dict(color=theme['primary'], width=5),
                marker=dict(size=12),
                fill='tonexty'
            ))
            
            # Receita Potencial
            fig.add_trace(go.Scatter(
                x=forecast_months,
                y=receita_potencial,
                mode='lines+markers',
                name='🚀 Receita Potencial (com otimizações IA)',
                line=dict(color=theme['secondary'], width=5),
                marker=dict(size=12),
                fill='tonexty'
            ))
            
            # Adicionar anotações com valores
            for i, month in enumerate(forecast_months):
                fig.add_annotation(
                    x=month,
                    y=receita_potencial[i],
                    text=f"<b>+R$ {diferenca[i]:,.0f}</b><br>oportunidade",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor=theme['accent'],
                    bgcolor=theme['accent'],
                    bordercolor=theme['accent'],
                    font=dict(color="black", size=10)
                )
            
            fig.update_layout(
                title="💰 <b>Potencial de Aumento de Faturamento</b><br><sub>Área VERDE = Dinheiro que pode ser ganho com IA</sub>",
                template=theme['plotly_template'],
                height=450,
                xaxis_title="Próximos 6 Meses",
                yaxis_title="Receita (R$)",
                yaxis_tickformat=',.0f'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Resumo de Impacto Financeiro
            total_extra = sum(diferenca)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {theme['secondary']}, {theme['primary']}); padding: 20px; border-radius: 15px; margin-top: 10px;">
                <h3 style="color: white; text-align: center; margin: 0;">
                    🎯 <strong>IMPACTO FINANCEIRO TOTAL:</strong><br>
                    <span style="font-size: 32px;">+R$ {total_extra:,.0f}</span><br>
                    <span style="font-size: 18px;">em receita adicional nos próximos 6 meses</span>
                </h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Placeholder para gráfico adicional - ações movidas para o final
            st.markdown("### 📈 **Previsões de Revenue Complementares**")
            st.info("🗺️ Análises e ações detalhadas estão disponíveis na seção final desta página.")
        
        # Seção de Análises Inteligentes e Insights
        st.markdown("---")
        st.markdown("### 🧠 **ANÁLISES INTELIGENTES DA IA - Insights Baseados em Dados**")
        
        # Análise de Sazonalidade Simples e Clara
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📅 **Quando Vender Mais? Padrões de Sazonalidade**")
            
            # Dados mais claros de sazonalidade
            sazonalidade = pd.DataFrame({
                'Mes': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                'Faturamento_Historico': [1200, 1100, 1450, 1380, 1600, 1520, 1350, 1420, 1680, 1750, 2100, 2300],
                'Previsao_2025': [1320, 1210, 1595, 1518, 1760, 1672, 1485, 1562, 1848, 1925, 2310, 2530],
                'Melhor_Epoca': ['Regular', 'Baixa', 'Boa', 'Boa', 'Excelente', 'Excelente', 'Regular', 'Regular', 'Excelente', 'Excelente', 'PICO', 'PICO']
            })
            
            cores_epoca = {
                'Baixa': '#ff6b6b',
                'Regular': theme['accent'], 
                'Boa': theme['primary'],
                'Excelente': theme['secondary'],
                'PICO': '#ff1493'
            }
            
            fig = go.Figure()
            
            # Histórico
            fig.add_trace(go.Scatter(
                x=sazonalidade['Mes'],
                y=sazonalidade['Faturamento_Historico'],
                mode='lines+markers',
                name='📊 Histórico Real',
                line=dict(color=theme['primary'], width=4),
                marker=dict(size=10)
            ))
            
            # Previsão
            fig.add_trace(go.Scatter(
                x=sazonalidade['Mes'],
                y=sazonalidade['Previsao_2025'],
                mode='lines+markers',
                name='🔮 Previsão IA 2025',
                line=dict(color=theme['secondary'], width=4, dash='dash'),
                marker=dict(size=10)
            ))
            
            # Colorir fundo por época
            for i, mes in enumerate(sazonalidade['Mes']):
                epoca = sazonalidade.iloc[i]['Melhor_Epoca']
                if epoca in ['PICO', 'Excelente']:
                    fig.add_vrect(
                        x0=i-0.4, x1=i+0.4,
                        fillcolor=cores_epoca[epoca],
                        opacity=0.2,
                        layer="below",
                        line_width=0,
                    )
            
            fig.update_layout(
                title="📈 <b>Sazonalidade das Vendas</b><br><sub>Fundo colorido = melhores épocas para vender</sub>",
                template=theme['plotly_template'],
                height=400,
                xaxis_title="Meses do Ano",
                yaxis_title="Faturamento (R$ mil)",
                yaxis_tickformat=',.0f'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Dicas Práticas de Sazonalidade
            st.markdown("""
            <div style="background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}); padding: 15px; border-radius: 10px;">
                <h4 style="color: white; margin-bottom: 10px;">💡 <strong>Dicas da IA para Maximizar Vendas:</strong></h4>
                <ul style="color: white; margin: 0; padding-left: 20px;">
                    <li><strong>Nov-Dez:</strong> Época PICO! Invista 40% mais em marketing</li>
                    <li><strong>Mai-Jun:</strong> Ótima época para fechar contratos anuais</li>
                    <li><strong>Fev:</strong> Mês mais fraco - foque em prospecção</li>
                    <li><strong>Set-Out:</strong> Preparação para pico - acelere pipeline</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💎 **Análise de Valor por Cliente - Quem Vale Mais?**")
            
            # Segmentação clara por valor
            segmentos_valor = pd.DataFrame({
                'Segmento': ['🏢 Enterprise\n(+R$ 100k)', '🏭 Corporate\n(R$ 50-100k)', '🏪 SMB\n(R$ 20-50k)', 
                           '🚀 Startup\n(R$ 5-20k)', '👥 Micro\n(<R$ 5k)'],
                'Clientes_Atuais': [45, 123, 289, 567, 1234],
                'Ticket_Medio': [18500, 7200, 3200, 1250, 280],
                'LTV_3_Anos': [89000, 34500, 12800, 4800, 1250],
                'Margem_Lucro': [82.4, 75.8, 68.9, 62.1, 45.7],
                'Tempo_Fechar_Deal': [89, 67, 32, 18, 12]
            })
            
            # Calcular receita total por segmento
            segmentos_valor['Receita_Total'] = segmentos_valor['Clientes_Atuais'] * segmentos_valor['Ticket_Medio']
            segmentos_valor['ROI_Segment'] = segmentos_valor['LTV_3_Anos'] / segmentos_valor['Ticket_Medio']
            
            # Gráfico de bolhas: LTV vs Margem vs Receita Total
            fig = go.Figure()
            
            cores_segmento = [theme['accent'], theme['secondary'], theme['primary'], '#ffd700', '#ff6b6b']
            
            fig.add_trace(go.Scatter(
                x=segmentos_valor['Margem_Lucro'],
                y=segmentos_valor['LTV_3_Anos'],
                mode='markers+text',
                text=segmentos_valor['Segmento'],
                textposition='middle center',
                marker=dict(
                    size=segmentos_valor['Receita_Total']/300000,  # Scale for visibility
                    color=cores_segmento,
                    opacity=0.8,
                    line=dict(width=3, color='white')
                ),
                hovertemplate="<b>%{text}</b><br>" +
                            "Margem: %{x:.1f}%<br>" +
                            "LTV 3 anos: R$ %{y:,.0f}<br>" +
                            "Receita Total Segmento: %{marker.size}<br>" +
                            "<extra></extra>"
            ))
            
            fig.update_layout(
                title="💰 <b>Mapa de Valor dos Segmentos</b><br><sub>Tamanho da bolha = Receita Total do Segmento</sub>",
                template=theme['plotly_template'],
                height=400,
                xaxis_title="% Margem de Lucro",
                yaxis_title="Valor Vitalício 3 Anos (R$)",
                yaxis_tickformat=',.0f'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Recomendações Claras de Foco
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ff1493, #ff6b6b); padding: 15px; border-radius: 10px;">
                <h4 style="color: white; margin-bottom: 10px;">🎯 <strong>Onde Focar Seus Esforços:</strong></h4>
                <div style="color: white;">
                    <p style="margin: 5px 0;"><strong>1° Prioridade:</strong> 🏢 Enterprise - Alto valor, alta margem</p>
                    <p style="margin: 5px 0;"><strong>2° Prioridade:</strong> 🏭 Corporate - Bom equilíbrio risco/retorno</p>
                    <p style="margin: 5px 0;"><strong>3° Prioridade:</strong> 🚀 Startup - Rápido de fechar, volume alto</p>
                    <p style="margin: 5px 0; color: #ffcccc;"><strong>Evitar:</strong> 👥 Micro - Baixa margem, alto esforço</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🏆 **Revenue Analytics - Product & Margin Intelligence**")
        
        # Revenue Analytics KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Product Revenue", "R$ 1.24M", "↗️ +22.8%", help="Revenue total de produtos")
        with col2:
            st.metric("Avg Gross Margin", "67.8%", "↗️ +3.2pp", help="Margem bruta média ponderada")
        with col3:
            st.metric("Product Mix Optimization", "89.4%", "↗️ +8.7pp", help="Otimização do mix de produtos")
        with col4:
            st.metric("Cross-sell Rate", "34.7%", "↗️ +6.1pp", help="Taxa de venda cruzada")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Advanced Product Performance Matrix
            product_matrix = pd.DataFrame({
                'Produto': ['Aurum Enterprise', 'Aurum Premium', 'Aurum Standard', 'Aurum Professional', 
                           'Aurum Basic', 'Aurum Starter', 'Aurum Custom', 'Aurum Lite'],
                'Revenue_Share': [28.5, 22.8, 18.7, 12.4, 8.9, 4.2, 2.8, 1.7],
                'Growth_Rate': [45.2, 32.8, 18.9, 28.4, 12.7, 67.8, 89.4, -8.2],
                'Gross_Margin': [78.9, 72.4, 65.8, 69.2, 58.7, 52.3, 85.6, 48.9],
                'Market_Share': [15.8, 22.4, 35.7, 18.9, 28.4, 12.1, 3.4, 45.2],
                'Customer_Count': [89, 245, 478, 189, 567, 234, 23, 789]
            })
            
            # BCG Matrix Style - Growth vs Market Share
            fig = go.Figure()
            
            # Quadrantes BCG
            fig.add_shape(type="rect", x0=0, y0=0, x1=25, y1=50, 
                         fillcolor="rgba(255,0,0,0.1)", layer="below")
            fig.add_shape(type="rect", x0=25, y0=0, x1=50, y1=50, 
                         fillcolor="rgba(255,255,0,0.1)", layer="below")
            fig.add_shape(type="rect", x0=0, y0=50, x1=25, y1=100, 
                         fillcolor="rgba(128,128,128,0.1)", layer="below")
            fig.add_shape(type="rect", x0=25, y0=50, x1=50, y1=100, 
                         fillcolor="rgba(0,255,0,0.1)", layer="below")
            
            fig.add_trace(go.Scatter(
                x=product_matrix['Market_Share'],
                y=product_matrix['Growth_Rate'],
                mode='markers+text',
                text=product_matrix['Produto'].str.replace('Aurum ', ''),
                textposition='middle center',
                marker=dict(
                    size=product_matrix['Revenue_Share']*2,
                    color=product_matrix['Gross_Margin'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="Gross Margin %"),
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                hovertemplate="<b>%{text}</b><br>" +
                            "Market Share: %{x:.1f}%<br>" +
                            "Growth: %{y:.1f}%<br>" +
                            "Revenue Share: %{marker.size:.1f}%<br>" +
                            "<extra></extra>"
            ))
            
            # Labels dos quadrantes
            fig.add_annotation(x=12.5, y=75, text="⭐ Stars", showarrow=False, font=dict(size=14, color="green"))
            fig.add_annotation(x=37.5, y=75, text="💰 Cash Cows", showarrow=False, font=dict(size=14, color="blue"))
            fig.add_annotation(x=12.5, y=25, text="❓ Question Marks", showarrow=False, font=dict(size=14, color="orange"))
            fig.add_annotation(x=37.5, y=25, text="🐶 Dogs", showarrow=False, font=dict(size=14, color="red"))
            
            fig.update_layout(
                title="📈 **Product Portfolio Matrix (BCG-Style)**<br><sub>Bolha = Revenue Share | Cor = Margin</sub>",
                template=theme['plotly_template'],
                height=500,
                xaxis_title="Market Share Relativo (%)",
                yaxis_title="Growth Rate (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Profit Waterfall Analysis
            profit_waterfall = pd.DataFrame({
                'Category': ['Revenue Bruta', 'COGS', 'Gross Profit', 'Sales & Marketing', 
                           'Operacional', 'P&D', 'Admin', 'EBITDA'],
                'Value': [1240000, -372000, 868000, -248000, -186000, -62000, -89000, 283000],
                'Type': ['positive', 'negative', 'total', 'negative', 'negative', 'negative', 'negative', 'total']
            })
            
            # Waterfall Chart
            fig = go.Figure()
            
            colors = ['green' if t == 'positive' else 'red' if t == 'negative' else 'blue' 
                     for t in profit_waterfall['Type']]
            
            fig.add_trace(go.Waterfall(
                name="Profit Analysis",
                orientation="v",
                measure=["absolute", "relative", "total", "relative", "relative", "relative", "relative", "total"],
                x=profit_waterfall['Category'],
                y=profit_waterfall['Value'],
                text=[f"R$ {val:,.0f}" for val in profit_waterfall['Value']],
                textposition="outside",
                connector={"line": {"color": "rgba(255,255,255,0.5)"}},
                decreasing={"marker": {"color": "red"}},
                increasing={"marker": {"color": "green"}},
                totals={"marker": {"color": theme['primary']}}
            ))
            
            fig.update_layout(
                title="💰 **Profit Waterfall Analysis**<br><sub>Breakdown de receita para EBITDA</sub>",
                template=theme['plotly_template'],
                height=500,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Customer Segmentation & Pricing Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer Segmentation by Value
            customer_segments = pd.DataFrame({
                'Segment': ['Enterprise (>R$100k)', 'Corporate (R$50-100k)', 'SMB (R$20-50k)', 
                           'Startup (R$5-20k)', 'Micro (<R$5k)'],
                'Customer_Count': [45, 123, 289, 567, 1234],
                'Avg_Revenue_per_Customer': [18500, 7200, 3200, 1250, 280],
                'Lifetime_Value': [89000, 34500, 12800, 4800, 1250],
                'Churn_Rate': [8.2, 12.7, 18.9, 24.5, 35.8],
                'Gross_Margin': [82.4, 75.8, 68.9, 62.1, 45.7]
            })
            
            # Calculate total revenue per segment
            customer_segments['Total_Revenue'] = (customer_segments['Customer_Count'] * 
                                                 customer_segments['Avg_Revenue_per_Customer'])
            
            # Donut Chart com Revenue Distribution
            fig = go.Figure(data=[go.Pie(
                labels=customer_segments['Segment'],
                values=customer_segments['Total_Revenue'],
                hole=0.4,
                marker_colors=[theme['primary'], theme['secondary'], theme['accent'], '#ff6b6b', '#4ecdc4'],
                textinfo='label+percent',
                textposition='outside'
            )])
            
            fig.update_layout(
                title="🎯 **Customer Segmentation by Revenue**<br><sub>Distribuição de receita por segmento</sub>",
                template=theme['plotly_template'],
                height=400,
                annotations=[dict(text='Total<br>Revenue<br>R$ 1.24M', x=0.5, y=0.5, 
                                font_size=16, showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Price Elasticity & Optimization
            pricing_analysis = pd.DataFrame({
                'Price_Point': ['R$ 5k', 'R$ 15k', 'R$ 25k', 'R$ 35k', 'R$ 50k', 'R$ 75k', 'R$ 100k+'],
                'Demand_Volume': [1200, 890, 650, 420, 280, 180, 95],
                'Revenue_Potential': [6000000, 13350000, 16250000, 14700000, 14000000, 13500000, 9500000],
                'Market_Penetration': [67.8, 48.9, 35.2, 22.8, 15.4, 9.8, 5.2],
                'Price_Elasticity': [-2.1, -1.8, -1.4, -1.1, -0.8, -0.6, -0.3]
            })
            
            # Dual axis: Volume vs Revenue
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(x=pricing_analysis['Price_Point'], y=pricing_analysis['Demand_Volume'], 
                      name="Demand Volume", marker_color=theme['primary'], opacity=0.7),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=pricing_analysis['Price_Point'], y=pricing_analysis['Revenue_Potential'], 
                          mode='lines+markers', name="Revenue Potential", 
                          line=dict(color=theme['secondary'], width=4),
                          marker=dict(size=10)),
                secondary_y=True,
            )
            
            fig.update_layout(
                title="💲 **Price Optimization Analysis**<br><sub>Demanda vs Potencial de Revenue</sub>", 
                template=theme['plotly_template'], 
                height=400
            )
            fig.update_yaxes(title_text="Demand Volume", secondary_y=False)
            fig.update_yaxes(title_text="Revenue Potential (R$)", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 👥 **Team Intelligence - Performance & Optimization**")
        
        # Team Intelligence KPIs
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Team Performance Score", "87.4", "↗️ +5.2pts", help="Score geral da equipe")
        with col2:
            st.metric("Top Performer Gap", "24.8%", "↘️ -3.1pp", help="Gap entre top e médio")
        with col3:
            st.metric("Training ROI", "340%", "↗️ +45pp", help="Retorno investimento em treinamento")
        with col4:
            st.metric("Collaboration Index", "92.1", "↗️ +7.3pts", help="Índice de colaboração")
        with col5:
            st.metric("Satisfaction Score", "8.7/10", "↗️ +0.4pts", help="Satisfação da equipe")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Team Performance Radar
            team_performance = pd.DataFrame({
                'Vendedor': ['Ana Silva', 'João Santos', 'Maria Costa', 'Pedro Lima', 'Lucas Oliveira'],
                'Revenue_Achievement': [142.3, 96.7, 128.5, 89.2, 119.8],
                'Activity_Score': [95.8, 87.2, 92.4, 78.9, 88.7],
                'Pipeline_Management': [89.4, 92.1, 87.8, 85.2, 91.3],
                'Customer_Satisfaction': [9.2, 8.4, 9.1, 8.8, 8.9],
                'Collaboration': [88.7, 94.2, 91.8, 89.4, 92.5],
                'Learning_Index': [92.3, 78.9, 89.7, 82.4, 95.1]
            })
            
            # Radar Chart para cada vendedor
            fig = go.Figure()
            
            metrics = ['Revenue Achievement', 'Activity Score', 'Pipeline Mgmt', 
                      'Customer Sat', 'Collaboration', 'Learning Index']
            
            colors = [theme['primary'], theme['secondary'], theme['accent'], '#ff6b6b', '#4ecdc4']
            
            for i, vendedor in enumerate(team_performance['Vendedor']):
                values = [
                    team_performance.iloc[i]['Revenue_Achievement'],
                    team_performance.iloc[i]['Activity_Score'],
                    team_performance.iloc[i]['Pipeline_Management'],
                    team_performance.iloc[i]['Customer_Satisfaction'] * 10,  # Scale to 100
                    team_performance.iloc[i]['Collaboration'],
                    team_performance.iloc[i]['Learning_Index']
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=metrics,
                    fill='toself',
                    name=vendedor,
                    line_color=colors[i % len(colors)],
                    opacity=0.6
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 150]
                    )),
                title="👥 **Team Performance Radar**<br><sub>Múltiplas dimensões de performance</sub>",
                template=theme['plotly_template'],
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Skills Development Matrix
            skills_matrix = pd.DataFrame({
                'Skill': ['Prospecting', 'Demo/Presentation', 'Objection Handling', 'Closing', 
                         'Account Management', 'Product Knowledge', 'Industry Expertise', 'CRM Usage'],
                'Team_Average': [78.5, 84.2, 76.8, 82.9, 89.3, 91.7, 73.4, 87.6],
                'Industry_Benchmark': [82.0, 79.5, 80.2, 78.8, 85.4, 88.9, 81.2, 82.3],
                'Improvement_Priority': [95, 65, 90, 70, 45, 35, 100, 55]
            })
            
            # Bubble chart: Team vs Benchmark
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=skills_matrix['Industry_Benchmark'],
                y=skills_matrix['Team_Average'],
                mode='markers+text',
                text=skills_matrix['Skill'],
                textposition='middle center',
                marker=dict(
                    size=skills_matrix['Improvement_Priority']/5,
                    color=skills_matrix['Improvement_Priority'],
                    colorscale='RdYlBu_r',
                    showscale=True,
                    colorbar=dict(title="Priority Score"),
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                hovertemplate="<b>%{text}</b><br>" +
                            "Industry: %{x:.1f}<br>" +
                            "Team: %{y:.1f}<br>" +
                            "Priority: %{marker.color}<br>" +
                            "<extra></extra>"
            ))
            
            # Linha de paridade
            fig.add_shape(type="line", x0=70, y0=70, x1=100, y1=100, 
                         line=dict(color="white", dash="dash"))
            
            fig.update_layout(
                title="🎯 **Skills Development Matrix**<br><sub>Team vs Industry | Bolha = Priority</sub>",
                template=theme['plotly_template'],
                height=500,
                xaxis_title="Industry Benchmark Score",
                yaxis_title="Team Average Score"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Coaching Insights & Retention Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Coaching Impact Analysis
            coaching_impact = pd.DataFrame({
                'Coaching_Type': ['1:1 Weekly', 'Group Sessions', 'Peer Mentoring', 'External Training', 
                                'Role Playing', 'Video Review', 'Skill Workshops'],
                'Hours_Invested': [45, 28, 35, 16, 24, 18, 32],
                'Performance_Lift': [23.5, 12.8, 18.7, 8.4, 15.9, 11.2, 19.6],
                'ROI_Multiple': [5.2, 2.8, 4.1, 1.9, 3.7, 2.4, 4.3],
                'Engagement_Score': [94, 78, 89, 72, 85, 69, 91]
            })
            
            # 3D Scatter: Hours vs Performance Lift vs ROI
            fig = go.Figure(data=[go.Scatter3d(
                x=coaching_impact['Hours_Invested'],
                y=coaching_impact['Performance_Lift'],
                z=coaching_impact['ROI_Multiple'],
                mode='markers+text',
                text=coaching_impact['Coaching_Type'],
                textposition='middle center',
                marker=dict(
                    size=coaching_impact['Engagement_Score']/5,
                    color=coaching_impact['Engagement_Score'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Engagement"),
                    opacity=0.8
                ),
                hovertemplate="<b>%{text}</b><br>" +
                            "Hours: %{x}<br>" +
                            "Performance Lift: %{y:.1f}%<br>" +
                            "ROI: %{z:.1f}x<br>" +
                            "<extra></extra>"
            )])
            
            fig.update_layout(
                title="🎓 **Coaching Impact Analysis**<br><sub>3D: Hours vs Performance vs ROI</sub>",
                template=theme['plotly_template'],
                height=450,
                scene=dict(
                    xaxis_title='Hours Invested',
                    yaxis_title='Performance Lift %',
                    zaxis_title='ROI Multiple'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Employee Lifecycle & Retention
            lifecycle_data = pd.DataFrame({
                'Tenure_Months': ['0-6', '7-12', '13-18', '19-24', '25-36', '37+'],
                'Employee_Count': [8, 12, 15, 18, 22, 35],
                'Avg_Performance': [68.4, 78.9, 89.2, 94.7, 98.1, 96.8],
                'Retention_Rate': [75.2, 89.4, 94.8, 97.1, 98.9, 99.2],
                'Training_Cost': [15000, 8500, 4200, 2800, 1900, 1200],
                'Value_Generated': [125000, 285000, 445000, 580000, 720000, 650000]
            })
            
            # Stacked area chart para lifecycle value
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=lifecycle_data['Tenure_Months'],
                y=lifecycle_data['Training_Cost'],
                mode='lines+markers',
                name='Training Cost',
                fill='tonexty',
                line=dict(color='red', width=3),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=lifecycle_data['Tenure_Months'],
                y=lifecycle_data['Value_Generated'],
                mode='lines+markers',
                name='Value Generated',
                fill='tonexty',
                line=dict(color=theme['primary'], width=3),
                marker=dict(size=8)
            ))
            
            # Performance line no eixo secundário
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=lifecycle_data['Tenure_Months'],
                y=lifecycle_data['Avg_Performance'],
                mode='lines+markers',
                name='Performance Score',
                line=dict(color=theme['secondary'], width=3),
                marker=dict(size=10),
                yaxis='y2'
            ))
            
            # Combinar gráficos
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(go.Bar(x=lifecycle_data['Tenure_Months'], y=lifecycle_data['Value_Generated'],
                               name='Value Generated', marker_color=theme['primary'], opacity=0.7),
                         secondary_y=False)
            
            fig.add_trace(go.Scatter(x=lifecycle_data['Tenure_Months'], y=lifecycle_data['Avg_Performance'],
                                   mode='lines+markers', name='Performance Score',
                                   line=dict(color=theme['secondary'], width=4)),
                         secondary_y=True)
            
            fig.update_layout(
                title="📈 **Employee Lifecycle Value**<br><sub>Performance & Value por Tenure</sub>",
                template=theme['plotly_template'],
                height=450
            )
            fig.update_yaxes(title_text="Value Generated (R$)", secondary_y=False)
            fig.update_yaxes(title_text="Performance Score", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)
        
        # SEÇÃO DE AÇÕES - FINAL DA ANÁLISE OPERACIONAL
        st.markdown("---")
        st.markdown("### 🎯 **PLANO DE AÇÃO - VENDAS & OPERAÇÕES**")
        st.markdown("📅 ***Suas ações prioritárias baseadas em toda a análise de IA acima***")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚨 **AÇÕES IMEDIATAS - Deals Críticos**")
            
            # Recriar os dados dos deals (movido para cá)
            deals_acao = pd.DataFrame({
                'Empresa': ['MegaCorp Industries', 'GlobalTech SA', 'TechSolutions Inc', 'StartupXYZ Ltd', 
                           'InnovateCo', 'Empresa ABC Corp', 'SmartBusiness', 'FutureTech Labs'],
                'Valor_Deal': [78000, 59000, 32000, 18500, 28000, 45000, 24500, 41000],
                'Prob_IA': [87.2, 91.5, 78.3, 94.1, 85.9, 89.7, 92.8, 71.2],
                'Dias_Pipeline': [89, 67, 32, 18, 28, 45, 21, 54],
                'Status_IA': ['🔥 QUENTE', '✅ FECHE JÁ', '⚡ ACELERE', '💚 GARANTIDO', 
                             '🎯 FOQUE AQUI', '✅ FECHE JÁ', '💚 GARANTIDO', '⚠️ RISCO'],
                'Acao_Recomendada': ['Reagendar demo urgente', 'Enviar contrato hoje', 'Ligar para tomador decisão',
                                    'Apenas fechar - 94% certo!', 'Resolver objeção preço', 'Proposta final hoje',
                                    'Deal certo - acelerar assinatura', 'Reunião urgente - perdendo momentum']
            })
            
            # Cores para status
            cores_status = {
                '🔥 QUENTE': theme['accent'],
                '✅ FECHE JÁ': theme['secondary'], 
                '⚡ ACELERE': '#ffd700',
                '💚 GARANTIDO': theme['primary'],
                '🎯 FOQUE AQUI': '#ff9500',
                '⚠️ RISCO': '#ff3333'
            }
            
            # Filtrar apenas os deals mais importantes
            deals_prioritarios = deals_acao[deals_acao['Valor_Deal'] >= 30000].sort_values('Prob_IA', ascending=False)
            
            for idx, deal in deals_prioritarios.iterrows():
                cor_box = cores_status.get(deal['Status_IA'], '#666666')
                st.markdown(f"""
                <div style="background: {cor_box}; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                    <h4 style="color: white; margin: 0 0 5px 0;">
                        {deal['Status_IA']} <strong>{deal['Empresa']}</strong> - R$ {deal['Valor_Deal']:,.0f}
                    </h4>
                    <p style="color: white; margin: 0; font-size: 14px;">
                        🎯 <strong>Ação:</strong> {deal['Acao_Recomendada']}<br>
                        📊 <strong>Probabilidade:</strong> {deal['Prob_IA']:.0f}% | ⏱️ <strong>Pipeline:</strong> {deal['Dias_Pipeline']} dias
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📈 **AÇÕES ESTRATÉGICAS - Médio Prazo**")
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}); padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <h4 style="color: white; margin-bottom: 10px;">💰 <strong>Oportunidade de Revenue:</strong></h4>
                <ul style="color: white; margin: 0; padding-left: 20px; font-size: 13px;">
                    <li><strong>Potencial nos próximos 6 meses:</strong> +R$ 372K</li>
                    <li><strong>Focus em Enterprise:</strong> 82.4% margem</li>
                    <li><strong>Época PICO:</strong> Nov-Dez (+40% investimento marketing)</li>
                </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, {theme['secondary']}, {theme['accent']}); padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <h4 style="color: white; margin-bottom: 10px;">🎯 <strong>Otimizações de Time:</strong></h4>
                <ul style="color: white; margin: 0; padding-left: 20px; font-size: 13px;">
                    <li><strong>Treinamento ROI:</strong> 340% retorno comprovado</li>
                    <li><strong>Colaboração:</strong> Índice 92.1 (excelente)</li>
                    <li><strong>Performance Gap:</strong> Reduzir de 24.8% para 15%</li>
                </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, {theme['accent']}, {theme['primary']}); padding: 15px; border-radius: 10px;">
                <h4 style="color: white; margin-bottom: 10px;">⏰ <strong>Cronograma de Ação:</strong></h4>
                <ul style="color: white; margin: 0; padding-left: 20px; font-size: 13px;">
                    <li><strong>Esta semana:</strong> Fechar 3 deals de alta probabilidade</li>
                    <li><strong>Próximo mês:</strong> Implementar otimizações de sazonalidade</li>
                    <li><strong>Trimestre:</strong> Programa de coaching ROI 340%</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        ThemeManager.apply_theme("Cyber Neon Pro")
        show_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()