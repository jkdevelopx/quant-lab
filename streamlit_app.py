# ============================================================================
# JEXA - UNIFIED DASHBOARD (Better UX)
# Decision-First Design: Show What Matters, When It Matters
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

st.set_page_config(page_title="JEXA", page_icon="📈", layout="wide")

# ============================================================================
# PREMIUM COLOR SYSTEM
# ============================================================================

COLORS = {
    'bull': '#10B981',
    'bear': '#EF4444',
    'neutral': '#6B7280',
    'primary': '#0A84FF',
    'bg': '#FFFFFF',
    'text': '#1F2937',
    'border': '#E5E7EB',
}

st.markdown(f"""
<style>
    .main {{background: {COLORS['bg']}; color: {COLORS['text']};}}
    .block-container {{padding: 2rem 3rem; max-width: 1800px;}}
    
    /* Decision Card - The Star of the Show */
    .decision-card {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        padding: 2.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
    }}
    
    .decision-title {{
        font-size: 1.25rem;
        font-weight: 600;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }}
    
    .decision-signal {{
        font-size: 4rem;
        font-weight: 800;
        margin: 1rem 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }}
    
    .decision-confidence {{
        font-size: 1.5rem;
        font-weight: 600;
        opacity: 0.95;
    }}
    
    .decision-action {{
        font-size: 1rem;
        opacity: 0.85;
        margin-top: 1rem;
        font-weight: 500;
    }}
    
    /* Signal Strength Bar */
    .signal-bar {{
        height: 12px;
        background: rgba(255,255,255,0.2);
        border-radius: 100px;
        margin: 1.5rem 0;
        overflow: hidden;
    }}
    
    .signal-fill {{
        height: 100%;
        background: white;
        border-radius: 100px;
        transition: width 0.5s ease;
    }}
    
    /* Mini Indicator Cards */
    .mini-card {{
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid {COLORS['border']};
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .mini-card:hover {{
        border-color: {COLORS['primary']};
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }}
    
    .mini-card.bullish {{
        border-color: {COLORS['bull']};
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
    }}
    
    .mini-card.bearish {{
        border-color: {COLORS['bear']};
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
    }}
    
    .mini-label {{
        font-size: 0.875rem;
        color: {COLORS['neutral']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }}
    
    .mini-value {{
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }}
    
    .mini-status {{
        font-size: 0.875rem;
        font-weight: 600;
    }}
    
    /* Unified Chart Container */
    .chart-container {{
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid {COLORS['border']};
        margin-top: 2rem;
    }}
    
    /* Action Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }}
    
    /* Clean Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        border-bottom: 2px solid {COLORS['border']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: {COLORS['neutral']};
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {COLORS['primary']};
        border-bottom: 3px solid {COLORS['primary']};
    }}
    
    h1 {{
        font-size: 3rem;
        font-weight: 800;
        color: {COLORS['text']};
        margin-bottom: 0.5rem;
    }}
    
    .subtitle {{
        font-size: 1.125rem;
        color: {COLORS['neutral']};
        margin-bottom: 2rem;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("<h1>JEXA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Clear signals. Smart decisions. Better returns.</p>", unsafe_allow_html=True)

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["📊 Analyze Asset", "🚀 Find Opportunities", "⚡ Quick Scan"])

# ============================================================================
# TAB 1: UNIFIED ASSET ANALYSIS (NEW APPROACH)
# ============================================================================

with tab1:
    # Top Controls (Simplified)
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        search = st.text_input("Search", placeholder="Type NVDA, AAPL, BTC...", label_visibility="collapsed")
        filtered = {k: v for k, v in ALL_ASSETS.items() 
                   if search.upper() in k.upper() or search.lower() in v.lower()} if search else ALL_ASSETS
        ticker = st.selectbox("Select Asset", list(filtered.keys()), format_func=lambda x: f"{x}", label_visibility="collapsed")
    
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)
    
    with col3:
        if st.button("🔍 Analyze", use_container_width=True, type="primary"):
            with st.spinner(f"Analyzing {ticker}..."):
                # Load Data
                df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
                
                if df.empty:
                    st.error("No data available")
                    st.stop()
                
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                
                close = df["Close"]
                high, low = df["High"], df["Low"]
                
                # Calculate ALL indicators
                sma20 = close.rolling(20).mean()
                sma50 = close.rolling(50).mean()
                
                delta = close.diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = -delta.where(delta < 0, 0).rolling(14).mean()
                rsi = 100 - (100 / (1 + gain / loss))
                
                macd_line = close.ewm(span=12, adjust=False).mean() - close.ewm(span=26, adjust=False).mean()
                macd_sig = macd_line.ewm(span=9, adjust=False).mean()
                
                std20 = close.rolling(20).std()
                bb_upper = sma20 + 2 * std20
                bb_lower = sma20 - 2 * std20
                bb_pct = (close - bb_lower) / (bb_upper - bb_lower)
                
                # Get current values
                current_price = close.iloc[-1]
                current_rsi = rsi.iloc[-1]
                current_macd = macd_line.iloc[-1]
                current_macd_sig = macd_sig.iloc[-1]
                current_bb = bb_pct.iloc[-1]
                price_vs_sma20 = (current_price / sma20.iloc[-1] - 1) * 100
                price_vs_sma50 = (current_price / sma50.iloc[-1] - 1) * 100
                
                # ======= DECISION LOGIC =======
                signals = []
                confidence = 50  # Base confidence
                
                # RSI Signal
                if current_rsi < 30:
                    signals.append("OVERSOLD")
                    confidence += 15
                elif current_rsi > 70:
                    signals.append("OVERBOUGHT")
                    confidence -= 15
                elif 40 < current_rsi < 60:
                    confidence += 10
                
                # Trend Signal
                if price_vs_sma20 > 0 and price_vs_sma50 > 0:
                    signals.append("UPTREND")
                    confidence += 20
                elif price_vs_sma20 < 0 and price_vs_sma50 < 0:
                    signals.append("DOWNTREND")
                    confidence -= 20
                
                # MACD Signal
                if current_macd > current_macd_sig:
                    signals.append("MOMENTUM+")
                    confidence += 15
                else:
                    signals.append("MOMENTUM-")
                    confidence -= 15
                
                # Final Decision
                if confidence >= 70:
                    decision = "STRONG BUY"
                    decision_color = "#10B981"
                    decision_emoji = "🚀"
                    action = "Strong bullish signals. Consider buying."
                elif confidence >= 55:
                    decision = "BUY"
                    decision_color = "#10B981"
                    decision_emoji = "📈"
                    action = "Moderately bullish. Suitable for entry."
                elif confidence >= 45:
                    decision = "HOLD"
                    decision_color = "#6B7280"
                    decision_emoji = "⏸️"
                    action = "Neutral market. Wait for clearer signals."
                elif confidence >= 30:
                    decision = "SELL"
                    decision_color = "#EF4444"
                    decision_emoji = "📉"
                    action = "Moderately bearish. Consider reducing position."
                else:
                    decision = "STRONG SELL"
                    decision_color = "#EF4444"
                    decision_emoji = "⚠️"
                    action = "Strong bearish signals. Avoid or exit."
                
                confidence = max(0, min(100, confidence))
                
                # ======= DISPLAY: DECISION FIRST =======
                
                st.markdown(f"""
                <div class='decision-card' style='background: linear-gradient(135deg, {decision_color} 0%, {decision_color}dd 100%);'>
                    <div class='decision-title'>AI Decision for {ticker}</div>
                    <div class='decision-signal'>{decision_emoji} {decision}</div>
                    <div class='decision-confidence'>{confidence}% Confidence</div>
                    <div class='signal-bar'>
                        <div class='signal-fill' style='width: {confidence}%;'></div>
                    </div>
                    <div class='decision-action'>{action}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # ======= MINI INDICATORS (At a Glance) =======
                
                st.markdown("### Key Indicators")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    rsi_status = "Oversold" if current_rsi < 30 else "Overbought" if current_rsi > 70 else "Neutral"
                    rsi_class = "bullish" if current_rsi < 30 else "bearish" if current_rsi > 70 else ""
                    st.markdown(f"""
                    <div class='mini-card {rsi_class}'>
                        <div class='mini-label'>RSI</div>
                        <div class='mini-value'>{current_rsi:.0f}</div>
                        <div class='mini-status'>{rsi_status}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    trend = "Bullish" if price_vs_sma20 > 0 else "Bearish"
                    trend_class = "bullish" if price_vs_sma20 > 0 else "bearish"
                    st.markdown(f"""
                    <div class='mini-card {trend_class}'>
                        <div class='mini-label'>Trend (SMA20)</div>
                        <div class='mini-value'>{price_vs_sma20:+.1f}%</div>
                        <div class='mini-status'>{trend}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    momentum = "Bullish" if current_macd > current_macd_sig else "Bearish"
                    momentum_class = "bullish" if current_macd > current_macd_sig else "bearish"
                    st.markdown(f"""
                    <div class='mini-card {momentum_class}'>
                        <div class='mini-label'>MACD</div>
                        <div class='mini-value'>{current_macd:.2f}</div>
                        <div class='mini-status'>{momentum}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    bb_status = "Lower Band" if current_bb < 0.2 else "Upper Band" if current_bb > 0.8 else "Middle"
                    bb_class = "bullish" if current_bb < 0.2 else "bearish" if current_bb > 0.8 else ""
                    st.markdown(f"""
                    <div class='mini-card {bb_class}'>
                        <div class='mini-label'>Bollinger</div>
                        <div class='mini-value'>{current_bb:.2f}</div>
                        <div class='mini-status'>{bb_status}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ======= UNIFIED CHART (All-in-One) =======
                
                st.markdown("### Price & Indicators")
                
                # Create subplot with 4 rows
                fig = make_subplots(
                    rows=4, cols=1,
                    row_heights=[0.5, 0.15, 0.15, 0.2],
                    subplot_titles=("", "RSI", "MACD", "Volume"),
                    vertical_spacing=0.03,
                    shared_xaxes=True
                )
                
                # Row 1: Price + Bollinger Bands + SMAs
                fig.add_trace(go.Candlestick(
                    x=df.index, open=df.Open, high=high, low=low, close=close,
                    name=ticker,
                    increasing_line_color='#10B981',
                    decreasing_line_color='#EF4444'
                ), row=1, col=1)
                
                fig.add_trace(go.Scatter(x=df.index, y=sma20, name="SMA20", 
                                        line=dict(color='#0A84FF', width=2)), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=sma50, name="SMA50", 
                                        line=dict(color='#8B5CF6', width=2)), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=bb_upper, name="BB Upper", 
                                        line=dict(color='#E5E7EB', dash='dash', width=1)), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=bb_lower, name="BB Lower", 
                                        line=dict(color='#E5E7EB', dash='dash', width=1),
                                        fill='tonexty', fillcolor='rgba(229, 231, 235, 0.2)'), row=1, col=1)
                
                # Row 2: RSI
                fig.add_trace(go.Scatter(x=df.index, y=rsi, name="RSI",
                                        line=dict(color='#8B5CF6', width=2)), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color='#EF4444', line_width=1, row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color='#10B981', line_width=1, row=2, col=1)
                fig.add_hrect(y0=30, y1=70, fillcolor='#F3F4F6', opacity=0.3, line_width=0, row=2, col=1)
                
                # Row 3: MACD
                fig.add_trace(go.Scatter(x=df.index, y=macd_line, name="MACD",
                                        line=dict(color='#0A84FF', width=2)), row=3, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=macd_sig, name="Signal",
                                        line=dict(color='#F59E0B', width=2)), row=3, col=1)
                fig.add_hline(y=0, line_color='#E5E7EB', line_width=1, row=3, col=1)
                
                # Row 4: Volume
                colors = ['#10B981' if close.iloc[i] > close.iloc[i-1] else '#EF4444' 
                         for i in range(1, len(close))]
                colors.insert(0, '#6B7280')
                fig.add_trace(go.Bar(x=df.index, y=df.Volume, name="Volume",
                                    marker_color=colors, showlegend=False), row=4, col=1)
                
                # Layout
                fig.update_layout(
                    height=1000,
                    template="plotly_white",
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=0, r=0, t=40, b=0),
                    hovermode='x unified'
                )
                
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=True, gridcolor='#F3F4F6')
                
                st.plotly_chart(fig, use_container_width=True)
                
                # ======= TRADE RECOMMENDATION =======
                
                st.markdown("### Trade Recommendation")
                
                if confidence >= 70:
                    st.success(f"""
                    **Entry:** ${current_price:.2f}  
                    **Stop Loss:** ${current_price * 0.95:.2f} (-5%)  
                    **Take Profit:** ${current_price * 1.15:.2f} (+15%)  
                    **Risk/Reward:** 1:3
                    """)
                elif confidence <= 30:
                    st.error(f"""
                    **Action:** Exit or avoid  
                    **Current Price:** ${current_price:.2f}  
                    **Support Level:** ${bb_lower.iloc[-1]:.2f}  
                    **Resistance:** ${bb_upper.iloc[-1]:.2f}
                    """)
                else:
                    st.info(f"""
                    **Current Price:** ${current_price:.2f}  
                    **Action:** Wait for clearer signals  
                    **Next Support:** ${sma20.iloc[-1]:.2f}  
                    **Next Resistance:** ${sma50.iloc[-1]:.2f}
                    """)

# ============================================================================
# TAB 2: FIND OPPORTUNITIES
# ============================================================================

with tab2:
    st.markdown("### 🚀 Find High-Potential Assets")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        market = st.selectbox("Market", ["All Stocks", "AI & Semiconductors", "Crypto"])
    with col2:
        min_conf = st.slider("Min Confidence", 60, 90, 70, 5)
    with col3:
        max_scan = st.number_input("Max Scan", 10, 50, 20, 5)
    
    if st.button("🔍 Scan Market", use_container_width=True, type="primary"):
        if market == "AI & Semiconductors":
            symbols = CATEGORIES.get("AI & Semiconductors", [])
        elif market == "Crypto":
            symbols = list(CRYPTO.keys())
        else:
            symbols = list(STOCKS.keys())
        
        with st.spinner("Scanning..."):
            results = find_next_nvda(symbols[:max_scan], min_conf/100)
            
            if results:
                st.success(f"Found {len(results)} opportunities!")
                
                for i, r in enumerate(results[:10], 1):
                    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                    
                    with col1:
                        st.markdown(f"### #{i}")
                    with col2:
                        st.markdown(f"**{r['symbol']}**  \n${r['price']:.2f}")
                    with col3:
                        st.markdown(f"**{r['confidence']:.1%}** Confidence")
                    with col4:
                        st.markdown(f"**{r['nvda_score']:.0f}/100** Score")
                    
                    st.markdown("---")
            else:
                st.warning("No opportunities found")

# ============================================================================
# TAB 3: QUICK SCAN
# ============================================================================

with tab3:
    st.markdown("### ⚡ Quick ML Signals")
    
    watchlist = st.selectbox("Watchlist", list(WATCHLISTS.keys()))
    symbols = WATCHLISTS[watchlist]
    
    if st.button("📡 Generate Signals", use_container_width=True, type="primary"):
        with st.spinner("Analyzing..."):
            results = scan_market(symbols, max_results=len(symbols))
            
            if results:
                st.success(f"{len(results)} signals generated")
                
                for r in results:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"**{r['symbol']}**")
                    with col2:
                        st.markdown(f"${r['price']:.2f}")
                    with col3:
                        emoji = "📈" if r['direction'] == 'UP' else "📉"
                        st.markdown(f"{emoji} {r['direction']}")
                    with col4:
                        st.markdown(f"{r['confidence']:.1%}")
                    
                    st.markdown("---")
            else:
                st.warning("No signals")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9CA3AF; padding: 2rem;'>
    <strong>JEXA</strong> | AI Trading Intelligence
</div>
""", unsafe_allow_html=True)