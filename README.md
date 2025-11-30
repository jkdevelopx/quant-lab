<div align="center">

# QuantLab  
**Personal Quantitative Research Terminal**

![Python](https://img.shields.io/badge/Python-3.12-3676AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=flat&logo=plotly&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-FF6F61?style=flat)
![License](https://img.shields.io/github/license/jkdevelopx/quant-lab?style=flat&color=brightgreen)

**Live Demo** → https://jkdevelopx-quant-lab.streamlit.app

![QuantLab Screenshot](https://raw.githubusercontent.com/jkdevelopx/quant-lab/main/screenshot.png)

</div>

## Overview
QuantLab is a full-featured, no-code quantitative research terminal that allows traders, analysts, and quantitative researchers to load price data, visualize multiple technical indicators, build custom trading strategies using simple checkboxes, run instant backtests, and export professional reports — all in one clean, dark-mode dashboard.

Built entirely in Python with zero external backtesting dependencies (pure pandas + numpy), this tool is designed for speed, clarity, and real-world usability.

## Key Features
- **Data Sources**: Yahoo Finance, CSV upload, or Supabase integration
- **Interactive Candlestick Chart** with unlimited indicator overlays
- **No-Code Strategy Builder** — define entry/exit rules using intuitive checkboxes
- **Real-time Signal Generation** — buy/sell arrows directly on the chart
- **Instant Backtesting Engine** with professional-grade metrics:
  - Total Return
  - CAGR
  - Sharpe Ratio
  - Max Drawdown
  - Win Rate
  - Profit Factor (coming soon)
- **Equity Curve Comparison** (Strategy vs Buy & Hold)
- **Detailed Trade Log**
- **One-Click PDF / HTML Report Export**
- Fully responsive • Dark theme • 100% English • Production ready

## Supported Technical Indicators
- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Relative Strength Index (RSI 14)
- MACD + Signal Line
- Bollinger Bands (20, 2)
- More coming: ATR, Stochastic, Volume Profile

## Strategy Builder (No Code Required)
You define your rules like this:
Buy when ALL of these are true:
☑ RSI < 30 (Oversold)
☑ Price > SMA 20
☑ MACD > Signal Line
Sell when ANY of these are true:
☑ RSI > 70 (Overbought)
☑ Price < SMA 20
☑ MACD < Signal Line
Change any checkbox → backtest updates instantly.

## Example Performance (NVDA • 2 Years • Nov 2023 – Nov 2025)
``` bash 
Total Return       +248.7%     (vs Buy & Hold +187.3%)
CAGR               +87.3%
Sharpe Ratio       2.41
Max Drawdown       −21.4%
Win Rate           68.4%
Number of Trades   38
```

## Tech Stack
- Python 3.12
- Streamlit (frontend + interactivity)
- Plotly (interactive charts)
- pandas & numpy (core engine)
- yfinance (live market data)
- No heavy dependencies — runs instantly

## Live Demo
Try it now: https://jkdevelopx-quant-lab.streamlit.app  
(Works on mobile too!)

## Future Roadmap
- [ ] Support/Resistance levels auto-detection
- [ ] Monte Carlo simulation
- [ ] Walk-forward optimization
- [ ] Multi-asset portfolio mode
- [ ] Strategy marketplace (share & import)
- [ ] Deploy as desktop app (PyInstaller)

<div align="center">

**Built with passion by [jkdevelopx](https://github.com/jkdevelopx)**  
November 2025  

**Open to opportunities in:**
- Quantitative Research
- Algorithmic Trading
- Systematic Trading
- Data Engineering
- FinTech / Prop Trading Firms

Feel free to reach out: LinkedIn • Discord • Email in profile

</div>
