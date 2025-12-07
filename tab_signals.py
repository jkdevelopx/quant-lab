"""
Tab 4: Quick Signals
Fast ML predictions for watchlists
"""

import streamlit as st
from assets import WATCHLISTS
from ml_engine import scan_market

def render():
    """Render the Quick Signals tab"""
    
    col1, col2 = st.columns([4, 2])
    
    with col1:
        watchlist_name = st.selectbox("Select Watchlist", 
                                     list(WATCHLISTS.keys()),
                                     key="signals_wl")
    
    with col2:
        if st.button("📡 Generate Signals", use_container_width=True, type="primary", key="signals_gen"):
            generate_signals(watchlist_name)


def generate_signals(watchlist_name):
    """Generate ML signals for watchlist"""
    
    symbols = WATCHLISTS[watchlist_name]
    
    with st.spinner(f"Analyzing {len(symbols)} assets..."):
        results = scan_market(symbols, max_results=len(symbols))
        
        if results:
            st.success(f"✅ Generated {len(results)} signals")
            
            st.markdown("### Signals")
            
            for r in results:
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.markdown(f"**{r['symbol']}**")
                    st.caption("Symbol")
                
                with col2:
                    st.markdown(f"**${r['price']:.2f}**")
                    st.caption("Price")
                
                with col3:
                    emoji = "📈" if r['direction'] == 'UP' else "📉"
                    st.markdown(f"**{emoji} {r['direction']}**")
                    st.caption("Direction")
                
                with col4:
                    st.markdown(f"**{r['confidence']:.1%}**")
                    st.caption("Confidence")
                
                with col5:
                    st.markdown(f"**{r['model_accuracy']:.1%}**")
                    st.caption("Model Accuracy")
                
                st.markdown("---")
        
        else:
            st.warning("⚠️ No signals generated. Try a different watchlist.")