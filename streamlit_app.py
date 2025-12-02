# ============================================================================
# JEXA - Professional Trading Platform
# Expert UX/UI Design with Beautiful Color Palette
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from assets import ALL_ASSETS, STOCKS, CRYPTO, CATEGORIES, WATCHLISTS
from scanner import StockScanner
from ml_engine import get_ml_signal, scan_market, find_next_nvda

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="JEXA - AI Trading",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# PROFESSIONAL COLOR SYSTEM (20+ Years UX/UI Expertise)
# ============================================================================

COLORS = {
    # Primary Palette
    'primary': '#0066FF',      # Vibrant blue - actions, links
    'primary_dark': '#0052CC',
    'primary_light': '#3385FF',
    
    # Success/Bull
    'success': '#00C48C',      # Teal green - bullish signals
    'success_bg': '#E6F9F4',
    'success_dark': '#00A075',
    
    # Danger/Bear  
    'danger': '#FF5757',       # Coral red - bearish signals
    'danger_bg': '#FFE9E9',
    'danger_dark': '#E63946',
    
    # Warning
    'warning': '#FFB020',      # Amber - caution
    'warning_bg': '#FFF7E6',
    
    # Neutral Grays
    'text_primary': '#1A202C',     # Almost black
    'text_secondary': '#4A5568',   # Medium gray
    'text_tertiary': '#A0AEC0',    # Light gray
    
    # Backgrounds
    'bg_primary': '#FFFFFF',
    'bg_secondary': '#F7FAFC',
    'bg_tertiary': '#EDF2F7',
    'border': '#E2E8F0',
    
    # Chart Colors
    'chart_bull': '#00C48C',
    'chart_bear': '#FF5757',
    'chart_line1': '#0066FF',
    'chart_line2': '#8B5CF6',   # Purple
    'chart_line3': '#F59E0B',   # Orange
    'chart_grid': '#F1F5F9',
}

# ============================================================================
# EXPERT UX/UI STYLING
# ============================================================================

st.markdown(f"""
<style>
    /* === FOUNDATION === */
    .main {{
        background-color: {COLORS['bg_primary']};
        color: {COLORS['text_primary']};
    }}
    
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}
    
    /* === TYPOGRAPHY === */
    h1 {{
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: {COLORS['text_primary']};
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }}
    
    h2, h3 {{
        color: {COLORS['text_primary']};
        font-weight: 600;
        letter-spacing: -0.02em;
    }}
    
    .subtitle {{
        font-size: 1.125rem;
        color: {COLORS['text_secondary']};
        font-weight: 400;
        margin-bottom: 2.5rem;
    }}
    
    /* === METRIC CARDS === */
    .metric-card {{
        background: {COLORS['bg_secondary']};
        border-radius: 16px;
        padding: 1.75rem;
        border: 1px solid {COLORS['border']};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }}
    
    .metric-card:hover {{
        border-color: {COLORS['primary']};
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 102, 255, 0.15);
    }}
    
    .metric-value {{
        font-size: 2.25rem;
        font-weight: 700;
        color: {COLORS['text_primary']};
        margin-bottom: 0.5rem;
        line-height: 1;
    }}
    
    .metric-value.positive {{
        color: {COLORS['success']};
    }}
    
    .metric-value.negative {{
        color: {COLORS['danger']};
    }}
    
    .metric-label {{
        font-size: 0.875rem;
        color: {COLORS['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }}
    
    /* === BUTTONS === */
    .stButton>button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 102, 255, 0.4);
    }}
    
    .stButton>button:active {{
        transform: translateY(0);
    }}
    
    /* === INPUTS === */
    .stSelectbox, .stTextInput {{
        background: white;
    }}
    
    .stSelectbox > div > div {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
    }}
    
    /* === DIVIDER === */
    hr {{
        border: none;
        border-top: 1px solid {COLORS['border']};
        margin: 2.5rem 0;
        opacity: 0.6;
    }}
    
    /* === SIDEBAR === */
    [data-testid="stSidebar"] {{
        background: {COLORS['bg_secondary']};
        border-right: 1px solid {COLORS['border']};
    }}
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2.5rem;
        border-bottom: 2px solid {COLORS['bg_tertiary']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 0.75rem 0;
        color: {COLORS['text_secondary']};
        border-bottom: 3px solid transparent;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.2s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        color: {COLORS['primary']};
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {COLORS['primary']};
        border-bottom-color: {COLORS['primary']};
        font-weight: 600;
    }}
    
    /* === DATAFRAME === */
    .stDataFrame {{
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        overflow: hidden;
    }}
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {{
        background: {COLORS['bg_secondary']};
        border-radius: 8px;
        border: 1px solid {COLORS['border']};
    }}
    
    /* === HIDE STREAMLIT BRANDING === */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* === SIGNAL BADGES === */
    .signal-badge {{
        display: inline-block;
        padding: 0.375rem 0.875rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.875rem;
    }}
    
    .signal-buy {{
        background: {COLORS['success_bg']};
        color: {COLORS['success_dark']};
    }}
    
    .signal-sell {{
        background: {COLORS['danger_bg']};
        color: {COLORS['danger_dark']};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("<h1>JEXA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-Powered Trading Intelligence Platform</p>", unsafe_allow_html=True)

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(["📊 Backtest", "🚀 Find Next NVDA", "🔍 Scanner", "⚡ Quick Signals"])

# ============================================================================
# TAB 1: BACKTEST
# ============================================================================

with tab1:
    st.markdown("### Strategy Backtesting")
    
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    
    with col1:
        search = st.text_input("🔍", placeholder="Search NVDA, AAPL, BTC...", label_visibility="collapsed")
        filtered = {k: v for k, v in ALL_ASSETS.items() 
                   if search.upper() in k.upper() or search.lower() in v.lower()} if search else ALL_ASSETS
        ticker = st.selectbox("Asset", list(filtered.keys()), format_func=lambda x: f"{x}", label_visibility="collapsed")
    
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)
    
    with col3:
        timeframe = st.selectbox("Timeframe", ["1d", "1h", "30m"], index=0)
    
    with col4:
        capital = st.number_input("Capital ($)", value=100000, step=10000)
    
    with st.expander("⚙️ Strategy Settings", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Entry Signals**")
            rsi_buy = st.checkbox("RSI < 30", True)
            sma_buy = st.checkbox("Price > SMA20", True)
            macd_buy = st.checkbox("MACD > Signal", True)
        
        with col2:
            st.markdown("**Exit Signals**")
            rsi_sell = st.checkbox("RSI > 70", True)
            sma_sell = st.checkbox("Price < SMA20", False)
            macd_sell = st.checkbox("MACD < Signal", False)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            risk = st.slider("Risk (%)", 0.5, 10.0, 2.0, 0.5)
        with col2:
            sl = st.slider("Stop Loss (%)", 2.0, 30.0, 10.0, 1.0)
        with col3:
            tp = st.slider("Take Profit (%)", 5.0, 100.0, 25.0, 5.0)
    
    if st.button("▶ Run Backtest", use_container_width=True, type="primary"):
        with st.spinner(f"Backtesting {ticker}..."):
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
            close, high, low = df["Close"], df["High"], df["Low"]
            
            # Indicators
            sma20 = close.rolling(20).mean()
            std20 = close.rolling(20).std()
            upper_bb, lower_bb = sma20 + 2*std20, sma20 - 2*std20
            
            delta = close.diff()
            gain = delta.where(delta>0, 0).rolling(14).mean()
            loss = -delta.where(delta<0, 0).rolling(14).mean()
            rsi = 100 - 100/(1 + gain/loss)
            
            macd_line = close.ewm(span=12, adjust=False).mean() - close.ewm(span=26, adjust=False).mean()
            macd_sig = macd_line.ewm(span=9, adjust=False).mean()
            
            # Signals
            buy, sell = pd.Series(False, index=df.index), pd.Series(False, index=df.index)
            if rsi_buy: buy |= (rsi < 30)
            if sma_buy: buy |= (close > sma20)
            if macd_buy: buy |= (macd_line > macd_sig)
            if rsi_sell: sell |= (rsi > 70)
            if sma_sell: sell |= (close < sma20)
            if macd_sell: sell |= (macd_line < macd_sig)
            
            # Backtest
            position, capital_now, equity, trades = 0, capital, [capital], []
            
            for i in range(20, len(df)):
                price = close.iloc[i]
                if position == 0 and buy.iloc[i]:
                    shares = (capital_now * risk/100) / (price * sl/100)
                    if shares >= 0.001:
                        position = shares
                        stop_price, tp_price = price * (1 - sl/100), price * (1 + tp/100)
                        capital_now -= shares * price
                        trades.append({"type": "BUY", "time": df.index[i], "price": price})
                elif position > 0:
                    if price <= stop_price:
                        capital_now += position * stop_price
                        trades.append({"type": "STOP", "time": df.index[i], "price": stop_price})
                        position = 0
                    elif price >= tp_price:
                        capital_now += position * tp_price
                        trades.append({"type": "TP", "time": df.index[i], "price": tp_price})
                        position = 0
                    elif sell.iloc[i]:
                        capital_now += position * price
                        trades.append({"type": "SELL", "time": df.index[i], "price": price})
                        position = 0
                equity.append(capital_now + position*price)
            
            # Metrics
            equity = np.array(equity)
            total_ret = (equity[-1]/capital - 1) * 100
            num_trades = len(trades) // 2
            wins = len([t for t in trades if t["type"] in ["TP", "SELL"]])
            win_rate = (wins / max(1, num_trades)) * 100
            max_dd = ((np.maximum.accumulate(equity) - equity) / np.maximum.accumulate(equity)).max() * 100
            
            # Display
            st.markdown("### Performance")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown(f"<div class='metric-card'><div class='metric-value'>${equity[-1]:,.0f}</div><div class='metric-label'>Final Capital</div></div>", unsafe_allow_html=True)
            with col2:
                cls = 'positive' if total_ret > 0 else 'negative'
                st.markdown(f"<div class='metric-card'><div class='metric-value {cls}'>{total_ret:+.1f}%</div><div class='metric-label'>Return</div></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{win_rate:.1f}%</div><div class='metric-label'>Win Rate</div></div>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{num_trades}</div><div class='metric-label'>Trades</div></div>", unsafe_allow_html=True)
            with col5:
                st.markdown(f"<div class='metric-card'><div class='metric-value negative'>{max_dd:.1f}%</div><div class='metric-label'>Max DD</div></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Chart: Price
            st.markdown("### Price & Signals")
            fig1 = go.Figure()
            fig1.add_trace(go.Candlestick(
                x=df.index, open=df.Open, high=high, low=low, close=close, name=ticker,
                increasing_line_color=COLORS['chart_bull'], decreasing_line_color=COLORS['chart_bear']
            ))
            fig1.add_trace(go.Scatter(x=df.index, y=sma20, name="SMA20", line=dict(color=COLORS['chart_line1'], width=2)))
            
            buys = [t for t in trades if t["type"] == "BUY"]
            exits = [t for t in trades if t["type"] != "BUY"]
            
            if buys:
                fig1.add_trace(go.Scatter(
                    x=[t["time"] for t in buys], y=[t["price"]*0.98 for t in buys],
                    mode="markers", name="Buy", marker=dict(symbol="triangle-up", size=14, color=COLORS['success'])
                ))
            if exits:
                fig1.add_trace(go.Scatter(
                    x=[t["time"] for t in exits], y=[t["price"]*1.02 for t in exits],
                    mode="markers", name="Exit", marker=dict(symbol="triangle-down", size=14, color=COLORS['danger'])
                ))
            
            fig1.update_layout(
                height=500, template="plotly_white", xaxis_rangeslider_visible=False,
                margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor='white', plot_bgcolor='white'
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # Chart: Indicators
            st.markdown("### Technical Indicators")
            fig2 = make_subplots(rows=3, cols=1, subplot_titles=("RSI", "MACD", "Bollinger %"), vertical_spacing=0.08)
            
            fig2.add_trace(go.Scatter(x=df.index, y=rsi, name="RSI", line=dict(color=COLORS['chart_line2'], width=2)), row=1, col=1)
            fig2.add_hline(y=70, line_dash="dash", line_color=COLORS['danger'], line_width=1, row=1, col=1)
            fig2.add_hline(y=30, line_dash="dash", line_color=COLORS['success'], line_width=1, row=1, col=1)
            
            fig2.add_trace(go.Scatter(x=df.index, y=macd_line, name="MACD", line=dict(color=COLORS['chart_line1'], width=2)), row=2, col=1)
            fig2.add_trace(go.Scatter(x=df.index, y=macd_sig, name="Signal", line=dict(color=COLORS['chart_line3'], width=2)), row=2, col=1)
            
            bb_pct = (close - lower_bb) / (upper_bb - lower_bb)
            fig2.add_trace(go.Scatter(x=df.index, y=bb_pct, name="BB%", line=dict(color=COLORS['chart_line1'], width=2)), row=3, col=1)
            fig2.add_hline(y=1, line_dash="dash", line_color=COLORS['danger'], row=3, col=1)
            fig2.add_hline(y=0, line_dash="dash", line_color=COLORS['success'], row=3, col=1)
            
            fig2.update_layout(height=600, template="plotly_white", showlegend=False, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig2, use_container_width=True)
            
            # Chart: Equity
            st.markdown("### Equity Curve")
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                y=equity, name="Strategy",
                line=dict(color=COLORS['primary'], width=3),
                fill='tozeroy', fillcolor=f"rgba(0, 102, 255, 0.1)"
            ))
            fig3.add_trace(go.Scatter(
                y=close/close.iloc[0]*capital, name="Buy & Hold",
                line=dict(color=COLORS['text_tertiary'], width=2, dash='dot')
            ))
            fig3.update_layout(height=350, template="plotly_white", margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig3, use_container_width=True)

# ============================================================================
# TAB 2: FIND NEXT NVDA
# ============================================================================

with tab2:
    st.markdown("### 🚀 Find Next NVDA")
    st.markdown("AI-powered scanner for high-potential stocks")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        market_filter = st.selectbox("Market", ["All Stocks", "AI/Semiconductors", "Tech Only", "Crypto"])
    with col2:
        min_confidence = st.slider("Min Confidence (%)", 60, 90, 70, 5)
    with col3:
        max_analyze = st.number_input("Max Stocks", 10, 50, 20, 5)
    
    if st.button("🔍 Find Opportunities", use_container_width=True, type="primary"):
        if market_filter == "AI/Semiconductors":
            symbols = CATEGORIES.get("AI & Semiconductors", [])
        elif market_filter == "Tech Only":
            symbols = CATEGORIES.get("Tech Giants", [])
        elif market_filter == "Crypto":
            symbols = list(CRYPTO.keys())
        else:
            symbols = list(STOCKS.keys())
        
        with st.spinner(f"Analyzing {min(len(symbols), max_analyze)} assets..."):
            results = find_next_nvda(symbols[:max_analyze], min_confidence=min_confidence/100)
            
            if results:
                st.success(f"✅ Found {len(results)} high-potential opportunities!")
                
                st.markdown("### Top Picks")
                
                for i, r in enumerate(results[:10], 1):
                    col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 2, 2, 2])
                    
                    with col1:
                        emoji = "🔥" if r['nvda_score'] > 85 else "⭐" if r['nvda_score'] > 75 else "📈"
                        st.markdown(f"### {emoji} #{i}")
                    with col2:
                        st.markdown(f"**{r['symbol']}**")
                        st.caption("Symbol")
                    with col3:
                        st.markdown(f"**${r['price']:.2f}**")
                        st.caption("Price")
                    with col4:
                        st.markdown(f"**{r['confidence']:.1%}**")
                        st.caption("ML Confidence")
                    with col5:
                        st.markdown(f"**{r['nvda_score']:.0f}/100**")
                        st.caption("Score")
                    with col6:
                        st.markdown(f"<span class='signal-badge signal-buy'>{r['direction']} ↗️</span>", unsafe_allow_html=True)
                    
                    st.markdown("---")
            else:
                st.warning("No opportunities found. Try lowering confidence.")

# ============================================================================
# TAB 3: SCANNER
# ============================================================================

with tab3:
    st.markdown("### Market Scanner")
    
    col1, col2 = st.columns(2)
    with col1:
        scan_types = {"🚀 Momentum": "momentum", "📈 Trend": "trend", "💎 Oversold": "oversold", "⚡ Volume": "volume"}
        scan_display = st.selectbox("Scan Type", list(scan_types.keys()))
        scan_type = scan_types[scan_display]
    with col2:
        scan_market = st.selectbox("Market", ["Stocks", "Crypto", "Both"])
    
    if st.button("🔍 Run Scanner", use_container_width=True, type="primary"):
        symbols = list(STOCKS.keys())[:50] if scan_market == "Stocks" else list(CRYPTO.keys()) if scan_market == "Crypto" else list(STOCKS.keys())[:30] + list(CRYPTO.keys())
        
        with st.spinner("Scanning..."):
            scanner = StockScanner(symbols)
            results = scanner.scan(scan_type)
            
            if results:
                st.success(f"Found {len(results)} opportunities!")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, height=400)
            else:
                st.info("No signals found")

# ============================================================================
# TAB 4: QUICK SIGNALS
# ============================================================================

with tab4:
    st.markdown("### ⚡ Quick ML Signals")
    st.markdown("Instant predictions for popular assets")
    
    watchlist_name = st.selectbox("Watchlist", list(WATCHLISTS.keys()))
    symbols = WATCHLISTS[watchlist_name]
    
    if st.button("📡 Generate Signals", use_container_width=True, type="primary"):
        with st.spinner(f"Analyzing {len(symbols)} assets..."):
            results = scan_market(symbols, max_results=len(symbols))
            
            if results:
                st.success(f"✅ {len(results)} signals generated")
                
                for r in results:
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
                    
                    with col1:
                        st.markdown(f"**{r['symbol']}**")
                    with col2:
                        st.markdown(f"${r['price']:.2f}")
                    with col3:
                        badge_class = 'signal-buy' if r['direction'] == 'UP' else 'signal-sell'
                        emoji = "📈" if r['direction'] == "UP" else "📉"
                        st.markdown(f"<span class='signal-badge {badge_class}'>{emoji} {r['direction']}</span>", unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"{r['confidence']:.1%}")
                        st.caption("Confidence")
                    with col5:
                        st.markdown(f"{r['model_accuracy']:.1%}")
                        st.caption("Accuracy")
                    
                    st.markdown("---")
            else:
                st.warning("No signals")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: {COLORS['text_tertiary']}; font-size: 0.875rem; padding: 2rem 0;'>
    <p style='font-weight: 600; color: {COLORS['text_secondary']};'>JEXA</p>
    <p>AI Trading Intelligence Platform</p>
    <p style='margin-top: 0.5rem;'>Python • Streamlit • LightGBM • Machine Learning</p>
</div>
""", unsafe_allow_html=True)