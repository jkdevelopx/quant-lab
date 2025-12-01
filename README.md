JEXA — AI-Powered Trading Intelligence
══════════════════════════════════════════════════════════

Yeah, it's finally here.

A dead-simple, stupidly fast, insanely accurate trading research tool I built for myself first — then decided to make it pretty so I don't have to hide it anymore.

Live demo → (i will update once deployed)

What it does (no bullshit)
══════════════════════════════════════════════════════════
• Scans 18 US stocks + 8 cryptos every day with LightGBM
• Only shows signals I would actually trade (>60% confidence)
• Sends them straight to my private Discord the second I click "SCAN"
• Full backtester with real risk management (position sizing, SL/TP, % risk)
• Apple-level dark UI because I got tired of ugly Streamlit apps
• One-click CSV export for my trade journal

Stack (nothing fancy, just works)
══════════════════════════════════════════════════════════
- Streamlit (because who has time for React)
- yfinance (free data = happy wallet)
- LightGBM (still beats LSTM 9/10 times in real trading)
- Plotly (charts that don't make me want to cry)
- Python only. No Docker. No bullshit.

Run it locally in 30 seconds
══════════════════════════════════════════════════════════
git clone https://github.com/jkdevelopx/quant-lab.git
cd quant-lab
pip install -r requirements.txt
streamlit run streamlit_app.py

Want alerts in Discord?
══════════════════════════════════════════════════════════
1. Right-click channel → Create Webhook
2. Paste URL into discord_alert.py
3. Click "SCAN" → profit (or loss, your choice)

Current watchlist (feel free to hate or copy)
══════════════════════════════════════════════════════════
NVDA, TSLA, AAPL, AMD, SMCI, META, MSFT, GOOGL, AMZN
BTC-USD, ETH-USD, SOL-USD, COIN, HOOD, PLTR, MARA, RIOT

Disclaimer (gotta say it)
══════════════════════════════════════════════════════════
This is my personal tool. Not financial advice.
I'm not your financial advisor. I'm just a guy who got tired of losing money.

If it makes money → cool.
If it loses money → also part of the game.

Built in Bangkok nights with too much coffee and zero sleep • 2025

"Most people quit. Winners just keep shipping."

– me, probably

P.S. If you're a quant, trader, or just someone who hates bad UI — hit me up. I might let you in the private alpha.
