# alpha_engine.py
import yfinance as yf
import ccxt
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from datetime import datetime

# === รายการหุ้น + Crypto ที่คุณต้องการ ===
# แก้แค่บรรทัดนี้ใน alpha_engine.py (แทนที่บรรทัดเดิม)

STOCKS = ["AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA","AMD","NFLX","COIN","SHOP","BLOCK","HOOD","JPM","V","MA","DIS","PYPL"]
CRYPTO = ["BTC/USDT","ETH/USDT","SOL/USDT","BNB/USDT","XRP/USDT","ADA/USDT","DOGE/USDT","AVAX/USDT"]

exchange = ccxt.binance()

def get_data(symbol):
    if "/" in symbol:
        ohlcv = exchange.fetch_ohlcv(symbol, '1d', limit=800)
        df = pd.DataFrame(ohlcv, columns=['ts','O','H','L','C','V'])
        df['Date'] = pd.to_datetime(df['ts'], unit='ms')
        df = df.set_index('Date')[['O','H','L','C','V']]
        df.columns = ['Open','High','Low','Close','Volume']
        return df
    else:
        return yf.download(symbol, period="3y", progress=False, auto_adjust=True)

def add_features(df):
    df = df.copy()
    df['rsi'] = 100 - (100 / (1 + (df['Close'].diff().clip(lower=0).rolling(14).mean() / 
                                (-df['Close'].diff().clip(upper=0).rolling(14).mean()))))
    df['sma20'] = df['Close'].rolling(20).mean()
    df['macd'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
    df['macd_sig'] = df['macd'].ewm(span=9).mean()
    df['bb_upper'] = df['sma20'] + 2*df['Close'].rolling(20).std()
    df['bb_lower'] = df['sma20'] - 2*df['Close'].rolling(20).std()
    df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    return df.dropna()

def get_ml_signal(symbol):
    try:
        df = get_data(symbol)
        df = add_features(df)
        features = ['rsi','Close','sma20','macd','macd_sig']
        X = df[features]
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        model = lgb.LGBMClassifier(n_estimators=100, max_depth=6, random_state=42, verbose=-1)
        model.fit(X_train, y_train)
        prob = model.predict_proba(X.iloc[-1:])[0][1]
        return {
            'symbol': symbol.replace('/USDT','-USD') if '/' in symbol else symbol,
            'confidence': prob,
            'price': df['Close'].iloc[-1],
            'signal': 'STRONG BUY' if prob > 0.70 else 'BUY' if prob > 0.65 else 'WATCH' if prob > 0.55 else 'AVOID'
        }
    except:
        return None