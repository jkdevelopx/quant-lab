import streamlit as st
from styles import apply_styles
import tab_analyze, tab_opportunities, tab_signals, tab_backtest

st.set_page_config(page_title="JEXA", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")
apply_styles()

st.markdown('<h1 class="jexa-title">JEXA</h1>', unsafe_allow_html=True)
st.markdown('<p class="jexa-subtitle">AI Trading Intelligence • 2025</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Analyze", "🚀 Opportunities", "⚡ Signals", "📈 Backtest"])

with tab1:
    tab_analyze.render()
with tab2:
    tab_opportunities.render()
with tab3:
    tab_signals.render()
with tab4:
    tab_backtest.render()

st.markdown("<div style='text-align:center; padding:3rem 0; color:#64748B;'>JEXA • Built with AI • 2025</div>", unsafe_allow_html=True)