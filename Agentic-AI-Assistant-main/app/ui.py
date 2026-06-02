"""
ui.py — Streamlit Redirect (Migrated to React + Vite)
---------------------------------------------------
This file has been replaced because the project now uses a high-fidelity React + Vite
frontend. 

To run the new frontend:
1. Make sure your FastAPI backend is running:
   python app/api.py
2. In a separate terminal, navigate to the frontend directory and start Vite:
   cd frontend
   npm run dev
"""

import streamlit as st

st.set_page_config(
    page_title="Sujith AI — Migrated to React",
    page_icon="🛍️",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');
    * { font-family: 'Outfit', sans-serif; }
    .main-container {
        text-align: center;
        padding: 40px;
        background: rgba(108, 61, 232, 0.05);
        border: 1px solid rgba(108, 61, 232, 0.2);
        border-radius: 20px;
        margin-top: 50px;
    }
    .badge {
        background: linear-gradient(90deg, #6C3DE8, #E8703D);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 20px;
    }
    h1 {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    p {
        color: #9CA3AF;
        font-size: 1rem;
        line-height: 1.6;
    }
    .code-box {
        background: #0f0f1b;
        color: #6CD3E8;
        padding: 15px;
        border-radius: 12px;
        text-align: left;
        font-family: monospace;
        margin: 20px 0;
        border: 1px solid rgba(255,255,255,0.08);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-container">
    <div class="badge">🚀 Upgrade Complete</div>
    <h1>Sujith AI Assistant has Migrated!</h1>
    <p>
        The Streamlit UI has been replaced with a high-fidelity <b>React + Vite</b> frontend 
        featuring glassmorphic panels, animated message bubbles, custom sentiment & department badges, 
        and an inline escalation handler.
    </p>
    <div class="code-box">
        # 1. Start the FastAPI backend server (Port 8000)<br>
        python app/api.py<br><br>
        # 2. Start the React + Vite frontend server (in another terminal)<br>
        cd frontend<br>
        npm run dev
    </div>
    <p style="font-size: 0.85rem; color: #6B7280;">
        Open the React app at the URL provided by the Vite dev server (usually <b>http://localhost:5173</b>).
    </p>
</div>
""", unsafe_allow_html=True)
