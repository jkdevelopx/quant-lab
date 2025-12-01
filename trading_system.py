# trading_system.py
import yfinance as yf
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

class AlphaSignal:
    def __init__(self):
        self.exchange = ccxt.binance()
        self.models = {}

    def get_data(self, symbol):
        if "/" in symbol:  # Crypto
            ohlcv = self.exchange.fetch_ohlcv(symbol, '1d', limit=730)
            df = pd.DataFrame(ohlcv, columns=['ts','Open','High','Low','Close','Volume'])
            df['timestamp'] = pd.to_datetime(df['ts'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df[['Open','High','Low','Close','Volume']]
        else:  # Stock
            return yf.download(symbol, period="2y", progress=False, auto_adjust=True)

    def add_features(self, df):
        df = df.copy()
        df['returns'] = df['Close'].pct_change()
        for i in [5,10,20,50]:
            df[f'sma_{i}'] = df['Close'].rolling(i).mean()
        delta = df['Close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = -delta.clip(upper=0).rolling(14).mean()
        rs = gain / loss.replace(0, np.nan)
        df['rsi'] = 100 - (100 / (1 + rs))
        exp1 = df['Close'].ewm(span=12).mean()
        exp2 = df['Close'].ewm(span=26).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df = df.dropna()
        df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        return df

    def generate(self):
        signals = []
        assets = config["stocks"] + config["crypto"]

        for symbol in assets:
            try:
                df = self.get_data(symbol)
                df = self.add_features(df)
                if len(df) < 100: continue

                features = [col for col in df.columns if col not in ['Open','High','Low','Close','Volume','target']]
                X = df[features]
                y = df['target']

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
                model = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.05, max_depth=6, verbose=-1)
                model.fit(X_train, y_train)

                pred = model.predict_proba(X.iloc[-1:])[0]
                confidence = pred[1]
                if confidence > 0.68:
                    price = df['Close'].iloc[-1]
                    signals.append({
                        'symbol': symbol.replace('/USDT',''),
                        'direction': 'BUY',
                        'confidence': confidence,
                        'current_price': price,
                        'take_profit': price * 1.18,
                        'stop_loss': price * 0.93
                    })
            except:
                continue

        signals.sort(key=lambda x: x['confidence'], reverse=True)
        return signals[:10]