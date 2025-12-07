import streamlit as st
from assets import STOCKS, CRYPTO, CATEGORIES
from ml_engine import find_next_nvda

def render():
    c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
    
    with c1:
        market = st.selectbox("Market", ["All Stocks", "AI & Semiconductors", "Crypto"], key="o1")
    with c2:
        conf = st.slider("Min Confidence", 60, 90, 70, 5, key="o2")
    with c3:
        max_scan = st.number_input("Max", 10, 50, 20, 5, key="o3")
    with c4:
        if st.button("Scan", use_container_width=True, type="primary", key="o4"):
            scan(market, conf, max_scan)

def scan(market, conf, max_scan):
    if market == "AI & Semiconductors":
        syms = CATEGORIES.get("AI & Semiconductors", [])
    elif market == "Crypto":
        syms = list(CRYPTO.keys())
    else:
        syms = list(STOCKS.keys())
    
    with st.spinner("Scanning..."):
        results = find_next_nvda(syms[:max_scan], conf/100)
        
        if results:
            st.success(f"✅ Found {len(results)} opportunities")
            
            for i, r in enumerate(results[:10], 1):
                c1, c2, c3, c4, c5 = st.columns([1, 2, 2, 2, 2])
                
                with c1:
                    emoji = "🔥" if r['nvda_score'] > 85 else "⭐"
                    st.markdown(f"### {emoji} #{i}")
                with c2:
                    st.markdown(f"**{r['symbol']}**")
                with c3:
                    st.markdown(f"${r['price']:.2f}")
                with c4:
                    st.markdown(f"{r['confidence']:.1%}")
                with c5:
                    st.markdown(f"{r['nvda_score']:.0f}/100")
                st.markdown("---")
        else:
            st.warning("No opportunities found")