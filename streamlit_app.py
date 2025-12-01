import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# === JEXA — ปรับให้สวยขึ้นนิดเดียวตามที่คุณขอ ===
st.set_page_config(page_title="JEXA", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main {background-color: #000000; color: white; padding: 0;}
    .block-container {padding-top: 2.5rem;}
    h1 {font-family: 'Helvetica Neue', sans-serif; font-size: 5.5rem; font-weight: 900; 
        background: linear-gradient(90deg, #ffffff, #888888); -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0;}
    .subtitle {text-align: center; color: #777; font-size: 1.4rem; margin: 8px 0 40px 0;}
    .stButton>button {background: linear-gradient(135deg, #00ff88, #00d1ff); color: black; 
                      font-weight: bold; border-radius: 16px; height: 60px; font-size: 1.3rem;}
    .metric-card {background: rgba(40,40,40,0.85); border-radius: 16px; padding: 1.6rem; 
                  text-align: center; border: 1px solid #333; box-shadow: 0 6px 20px rgba(0,0,0,0.3);}
    .sidebar .sidebar-content {background: #0a0a0a;}
    .stMarkdown {margin-bottom: 1.5rem;}
</style>
""", unsafe_allow_html=True)

# Header — เหมือนเดิมทุกอย่าง แต่สบายตามากขึ้น
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("https://files.catbox.sh/8wz1v1.png", use_column_width=True)
st.markdown("<h1>JEXA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-Powered Trading Intelligence</p>", unsafe_allow_html=True)
st.markdown("---")

# === AI SCANNER (อยู่ด้านบนสุด) ===
st.markdown("## JEXA AI Scanner")
if st.button("SCAN ALL 26 ASSETS NOW", type="primary", use_container_width=True):
    with st.spinner("Scanning 18 stocks + 8 cryptos with AI..."):
        try:
            from alpha_engine import STOCKS, CRYPTO, get_ml_signal
            from discord_alert import send_daily_signals

            all_assets = STOCKS + CRYPTO
            results = []
            for asset in all_assets:
                sig = get_ml_signal(asset)
                if sig and sig['confidence'] > 0.60:
                    results.append(sig)
            results.sort(key=lambda x: x['confidence'], reverse=True)

            if results:
                st.success(f"Found {len(results)} Strong Signals!")
                df = pd.DataFrame(results)
                df.index = range(1, len(df)+1)
                st.dataframe(df.style.format({"confidence": "{:.1%}", "price": "${:,.2f}"}), use_container_width=True)
                send_daily_signals(results)
            else:
                st.info("No strong signals today.")
        except Exception as e:
            st.error(f"AI Error: {e}")

st.markdown("---")

# === Sidebar Controls ===
with st.sidebar:
    st.markdown("<h2 style='color:#00ff88;text-align:center;'>Backtest Controls</h2>", unsafe_allow_html=True)
    
    popular = {
        "NVDA":"NVIDIA","TSLA":"Tesla","AAPL":"Apple","AMD":"AMD","SMCI":"Super Micro",
        "META":"Meta","MSFT":"Microsoft","GOOGL":"Google","AMZN":"Amazon",
        "BTC-USD":"Bitcoin","ETH-USD":"Ethereum","SOL-USD":"Solana"
    }
    
    ticker = st.selectbox("Asset", options=list(popular.keys()), 
                          format_func=lambda x: f"{x} — {popular[x]}", index=0)
    
    col1, col2 = st.columns(2)
    with col1:
        timeframe = st.selectbox("Timeframe", ["1d","4h","1h","30m","15m","5m"], index=0)
    with col2:
        period = st.selectbox("Period", ["6mo","1y","2y","5y","max"], index=1)

    st.markdown("#### Buy Rules (ALL)")
    rsi_buy  = st.checkbox("RSI < 30", True)
    sma_buy  = st.checkbox("Price > SMA20", True)
    macd_buy = st.checkbox("MACD > Signal", True)
    bb_buy   = st.checkbox("Price < Lower BB", False)

    st.markdown("#### Sell Rules (ANY)")
    rsi_sell  = st.checkbox("RSI > 70", True)
    sma_sell  = st.checkbox("Price < SMA20", False)
    macd_sell = st.checkbox("MACD < Signal", False)
    bb_sell   = st.checkbox("Price > Upper BB", False)

    st.markdown("#### Risk Management")
    capital = st.number_input("Initial Capital ($)", 10000, 5000000, 100000, step=10000)
    risk = st.slider("Risk per Trade (%)", 0.5, 10.0, 2.0, 0.1)
    sl = st.slider("Stop Loss (%)", 2.0, 30.0, 10.0, 0.5)
    tp = st.slider("Take Profit (%)", 5.0, 100.0, 25.0, 1.0)

# === ดึงข้อมูล & Backtest (เหมือนเดิมเป๊ะ) ===
@st.cache_data(ttl=300)
def load_data(t, p, i):
    df = yf.download(t, period=p, interval=i, progress=False, auto_adjust=True)
    if df.empty: 
        st.error("No data")
        st.stop()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    return df

df = load_data(ticker, period, timeframe)
close = df["Close"]
high, low = df["High"], df["Low"]

# Indicators
sma20 = close.rolling(20).mean()
std20 = close.rolling(20).std()
upper_bb = sma20 + 2*std20
lower_bb = sma20 - 2*std20
delta = close.diff()
gain = delta.where(delta>0,0).rolling(14).mean()
loss = -delta.where(delta<0,0).rolling(14).mean()
rsi = 100 - 100/(1 + gain/loss)
macd_line = close.ewm(span=12,adjust=False).mean() - close.ewm(span=26,adjust=False).mean()
macd_sig = macd_line.ewm(span=9,adjust=False).mean()

# Signals
buy  = pd.Series(False, index=df.index)
sell = pd.Series(False, index=df.index)
if rsi_buy:   buy  |= (rsi < 30)
if sma_buy:   buy  |= (close > sma20)
if macd_buy:  buy  |= (macd_line > macd_sig)
if bb_buy:    buy  |= (close < lower_bb)
if rsi_sell:  sell |= (rsi > 70)
if sma_sell:  sell |= (close < sma20)
if macd_sell: sell |= (macd_line < macd_sig)
if bb_sell:    sell |= (close > upper_bb)

# Backtest (เหมือนเดิมเป๊ะ)
position = 0
capital_now = capital
equity = [capital]
trades = []

for i in range(20, len(df)):
    price = close.iloc[i]
    if position == 0 and buy.iloc[i]:
        shares = (capital_now * risk/100) / (price * sl/100)
        if shares < 0.001: continue
        position = shares
        stop_price = price * (1 - sl/100)
        tp_price = price * (1 + tp/100)
        capital_now -= shares * price
        trades.append({"type":"BUY","time":df.index[i],"price":price})
    elif position > 0:
        if price <= stop_price:
            capital_now += position * stop_price
            trades.append({"type":"STOP LOSS","time":df.index[i],"price":stop_price})
            position = 0
        elif price >= tp_price:
            capital_now += position * tp_price
            trades.append({"type":"TAKE PROFIT","time":df.index[i],"price":tp_price})
            position = 0
        elif sell.iloc[i]:
            capital_now += position * price
            trades.append({"type":"SELL","time":df.index[i],"price":price})
            position = 0
    equity.append(capital_now + position*price)

# Results
equity = np.array(equity)
total_ret = equity[-1]/capital - 1
win_rate = len([t for t in trades if t["type"] in ["TAKE PROFIT","SELL"]]) / max(1,(len(trades)+1)//2) * 100
max_dd = ((np.maximum.accumulate(equity) - equity)/np.maximum.accumulate(equity)).max()

# Metrics — ปรับให้ดูสบายตามากขึ้น
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"<div class='metric-card'><h3 style='color:#00ff88'>${equity[-1]:,.0f}</h3><p style='color:#888'>Final Capital</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3 style='color:{'#00ff88' if total_ret>0 else '#ff3366'}'>{total_ret:+.1%}</h3><p style='color:#888'>Return</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3 style='color:#00d1ff'>{win_rate:.1f}%</h3><p style='color:#888'>Win Rate</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><h3 style='color:#ffa500'>{len(trades)//2}</h3><p style='color:#888'>Trades</p></div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div class='metric-card'><h3 style='color:#ff3366'>-{max_dd:.1%}</h3><p style='color:#888'>Max DD</p></div>", unsafe_allow_html=True)

# Charts
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df.Open, high=high, low=low, close=close, name=ticker))
fig.add_trace(go.Scatter(x=df.index, y=sma20, name="SMA20", line=dict(color="#00ff88", width=2)))
fig.add_trace(go.Scatter(x=df.index, y=upper_bb, name="Upper BB", line=dict(color="#555", dash="dot")))
fig.add_trace(go.Scatter(x=df.index, y=lower_bb, name="Lower BB", line=dict(color="#555", dash="dot")))

buys = [t for t in trades if t["type"]=="BUY"]
sells = [t for t in trades if t["type"]!="BUY"]
if buys:
    fig.add_trace(go.Scatter(x=[t["time"] for t in buys], y=[t["price"]*0.985 for t in buys],
                             mode="markers", name="BUY", marker=dict(symbol="triangle-up", size=18, color="#00ff88")))
if sells:
    fig.add_trace(go.Scatter(x=[t["time"] for t in sells], y=[t["price"]*1.015 for t in sells],
                             mode="markers", name="EXIT", marker=dict(symbol="triangle-down", size=18, color="#ff3366")))

fig.update_layout(height=700, template="plotly_dark", xaxis_rangeslider_visible=False, paper_bgcolor="#000", plot_bgcolor="#000")
st.plotly_chart(fig, use_container_width=True)

# Equity Curve
fig2 = go.Figure()
fig2.add_trace(go.Scatter(y=equity, name="JEXA Strategy", line=dict(color="#00ff88", width=5)))
fig2.add_trace(go.Scatter(y=close/close.iloc[0]*capital, name="Buy & Hold", line=dict(color="#666", width=2, dash="dot")))
fig2.update_layout(height=400, template="plotly_dark", title="Equity Curve", paper_bgcolor="#000", plot_bgcolor="#000")
st.plotly_chart(fig2, use_container_width=True)

# Export
if trades:
    csv = pd.DataFrame(trades).to_csv(index=False)
    st.download_button("Download Trade Log", csv, "jexa_trades.csv", "text/csv")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#555;'>© 2025 JEXA — Built by trader, for traders</p>", unsafe_allow_html=True)