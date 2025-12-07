import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from assets import ALL_ASSETS

def render():
    c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
    
    with c1:
        search = st.text_input("", placeholder="Search...", key="b1", label_visibility="collapsed")
        filtered = {k:v for k,v in ALL_ASSETS.items() if search.upper() in k or search.lower() in v.lower()} if search else ALL_ASSETS
        ticker = st.selectbox("", list(filtered.keys())[:100], key="b2", label_visibility="collapsed")
    with c2:
        period = st.selectbox("", ["1mo","3mo","6mo","1y"], index=3, key="b3", label_visibility="collapsed")
    with c3:
        capital = st.number_input("Capital", 10000, 1000000, 100000, 10000, key="b4")
    with c4:
        if st.button("Backtest", use_container_width=True, type="primary", key="b5"):
            backtest(ticker, period, capital)

def backtest(ticker, period, capital):
    with st.spinner("Backtesting..."):
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty: st.error("No data"); return
        if hasattr(df.columns, 'levels'): df.columns = df.columns.droplevel(1)
        
        close = df["Close"]
        sma20 = close.rolling(20).mean()
        delta = close.diff()
        gain = delta.where(delta>0,0).rolling(14).mean()
        loss = -delta.where(delta<0,0).rolling(14).mean()
        rsi = 100 - (100/(1 + gain/loss))
        
        buy = (rsi < 30) | (close > sma20)
        sell = (rsi > 70)
        
        pos, cap, eq, trades = 0, capital, [capital], []
        
        for i in range(20, len(df)):
            price = close.iloc[i]
            if pos == 0 and buy.iloc[i]:
                shares = (cap * 0.02) / (price * 0.1)
                if shares >= 0.001:
                    pos = shares
                    stop = price * 0.9
                    target = price * 1.25
                    cap -= shares * price
                    trades.append({"type": "BUY"})
            elif pos > 0:
                if price <= stop:
                    cap += pos * stop
                    trades.append({"type": "STOP"})
                    pos = 0
                elif price >= target:
                    cap += pos * target
                    trades.append({"type": "TP"})
                    pos = 0
                elif sell.iloc[i]:
                    cap += pos * price
                    trades.append({"type": "SELL"})
                    pos = 0
            eq.append(cap + pos*price)
        
        eq = np.array(eq)
        ret = (eq[-1]/capital - 1) * 100
        ntrades = len(trades) // 2
        wins = len([t for t in trades if t["type"] in ["TP", "SELL"]])
        wr = (wins / max(1, ntrades)) * 100
        
        st.markdown("### Performance")
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>${eq[-1]:,.0f}</div><div class='metric-label'>Final</div></div>", unsafe_allow_html=True)
        with c2:
            cls = 'positive' if ret > 0 else 'negative'
            st.markdown(f"<div class='metric-card'><div class='metric-value {cls}'>{ret:+.1f}%</div><div class='metric-label'>Return</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{wr:.1f}%</div><div class='metric-label'>Win Rate</div></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{ntrades}</div><div class='metric-label'>Trades</div></div>", unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=eq, name="Strategy", line=dict(color='#8B5CF6', width=3), fill='tozeroy'))
        fig.update_layout(height=400, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                         plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)