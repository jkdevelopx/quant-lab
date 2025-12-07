import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from assets import ALL_ASSETS

def render():
    c1, c2, c3, c4 = st.columns([4, 2, 2, 2])
    
    with c1:
        search = st.text_input("", placeholder="Search asset...", key="a1", label_visibility="collapsed")
        filtered = {k:v for k,v in ALL_ASSETS.items() if search.upper() in k or search.lower() in v.lower()} if search else ALL_ASSETS
    
    with c2:
        ticker = st.selectbox("", list(filtered.keys())[:100], key="a2", label_visibility="collapsed")
    
    with c3:
        period = st.selectbox("", ["1mo","3mo","6mo","1y","2y"], index=3, key="a3", label_visibility="collapsed")
    
    with c4:
        if st.button("Analyze", use_container_width=True, type="primary", key="a4"):
            analyze(ticker, period)

def analyze(ticker, period):
    with st.spinner("Analyzing..."):
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty: 
            st.error("No data")
            return
        if hasattr(df.columns, 'levels'): 
            df.columns = df.columns.droplevel(1)
        
        close = df["Close"]
        sma20 = close.rolling(20).mean()
        delta = close.diff()
        gain = delta.where(delta>0,0).rolling(14).mean()
        loss = -delta.where(delta<0,0).rolling(14).mean()
        rsi = 100 - (100/(1 + gain/loss))
        macd = close.ewm(span=12).mean() - close.ewm(span=26).mean()
        macd_sig = macd.ewm(span=9).mean()
        
        price = close.iloc[-1]
        rsi_val = rsi.iloc[-1]
        vs_sma = (price/sma20.iloc[-1] - 1) * 100
        
        conf = 50
        if rsi_val < 30: conf += 20
        elif rsi_val > 70: conf -= 20
        if vs_sma > 0: conf += 15
        else: conf -= 15
        if macd.iloc[-1] > macd_sig.iloc[-1]: conf += 15
        else: conf -= 15
        conf = max(0, min(100, conf))
        
        decision = "STRONG BUY" if conf >= 75 else "BUY" if conf >= 60 else "HOLD" if conf >= 45 else "SELL" if conf >= 30 else "STRONG SELL"
        color = "#10B981" if conf >= 60 else "#EF4444" if conf <= 40 else "#94A3B8"
        
        st.markdown(f'''
        <div class="decision-card">
            <h1 style="font-size:3.5rem; margin:0; color:{color};">{decision}</h1>
            <h2 style="margin:1rem 0;">{ticker}</h2>
            <h3 style="font-size:1.75rem; margin:0;">{conf}% Confidence</h3>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("### Indicators")
        cols = st.columns(4)
        indicators = [
            ("RSI", f"{rsi_val:.0f}", "Oversold" if rsi_val<30 else "Overbought" if rsi_val>70 else "Neutral"),
            ("Trend", f"{vs_sma:+.1f}%", "Bullish" if vs_sma>0 else "Bearish"),
            ("Price", f"${price:.2f}", ticker),
            ("MACD", f"{macd.iloc[-1]:.2f}", "Bullish" if macd.iloc[-1]>macd_sig.iloc[-1] else "Bearish")
        ]
        
        for col, (label, val, status) in zip(cols, indicators):
            with col:
                bull = "Bullish" in status or "Oversold" in status
                bear = "Bearish" in status or "Overbought" in status
                st.markdown(f'''
                <div class="mini-card {'bullish' if bull else 'bearish' if bear else ''}">
                    <div style="font-size:0.85rem; opacity:0.8;">{label}</div>
                    <div style="font-size:2rem; font-weight:900; margin:0.5rem 0;">{val}</div>
                    <div style="font-size:0.95rem;">{status}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("### Chart")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df.Open, high=df.High, low=df.Low, close=close,
                                     increasing_line_color='#10B981', decreasing_line_color='#EF4444'))
        fig.add_trace(go.Scatter(x=df.index, y=sma20, name="SMA20", line=dict(color='#8B5CF6', width=2)))
        fig.update_layout(height=500, template="plotly_dark", xaxis_rangeslider_visible=False,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)