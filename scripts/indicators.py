import pandas as pd
import ta

def add_all_indicators(df: pd.DataFrame, selected: list):
    df = df.copy()
    if "SMA 20" in selected: df["SMA 20"] = ta.trend.sma_indicator(df.Close, window=20)
    if "SMA 50" in selected: df["SMA 50"] = ta.trend.sma_indicator(df.Close, window=50)
    if "EMA 20" in selected: df["EMA 20"] = ta.trend.ema_indicator(df.Close, window=20)
    if "EMA 50" in selected: df["EMA 50"] = ta.trend.ema_indicator(df.Close, window=50)
    if "RSI 14" in selected: df["RSI 14"] = ta.momentum.rsi(df.Close, window=14)
    if "MACD" in selected:
        macd = ta.trend.MACD(df.Close)
        df["MACD"] = macd.macd()
        df["MACD Signal"] = macd.macd_signal()
    if "Bollinger Bands" in selected:
        bb = ta.volatility.BollingerBands(df.Close)
        df["BB Upper"] = bb.bollinger_hband()
        df["BB Lower"] = bb.bollinger_lband()
    if "ATR 14" in selected: df["ATR 14"] = ta.volatility.average_true_range(df.High, df.Low, df.Close, window=14)
    return df
