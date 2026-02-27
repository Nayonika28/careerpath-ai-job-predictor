
import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            background-color: #f8fafc;
        }
        
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            height: 3em;
            background-color: #0d9488;
            color: white;
            border: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #0f766e;
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.2);
        }
        
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        .role-title {
            color: #0f172a;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 0.2rem;
        }
        
        .confidence-badge {
            background-color: #f0fdfa;
            color: #0d9488;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

def card_component(title, content, badge=None):
    badge_html = f'<span class="confidence-badge">{badge} Match</span>' if badge else ""
    st.markdown(f"""
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="role-title">{title}</div>
                {badge_html}
            </div>
            <div style="color: #64748b; font-size: 0.9rem; margin-top: 0.5rem;">{content}</div>
        </div>
    """, unsafe_allow_html=True)
