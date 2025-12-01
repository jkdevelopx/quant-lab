import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import warnings
warnings.filterwarnings("ignore")

# รายชื่อหุ้น + คริปโต (เหมือนเดิม)
STOCKS = ["NVDA","TSLA","AAPL","AMD","SMCI","META","MSFT","GOOGL","AMZN"]
CRYPTO = ["BTC-USD","ETH-USD","SOL-USD"]
ALL_ASSETS = STOCKS + CRYPTO

# สร้าง/โหลดโมเดล LSTM
def create_lstm_model():
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(60, 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(50))
    model.add(Dense(1, activation='sigmoid'))  # 0 = Sell, 1 = Buy
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

scaler = MinMaxScaler(feature_range=(0,1))

def get_lstm_signal(symbol, period="2y", interval="1d"):
    try:
        # ดึงข้อมูล
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        if len(df) < 100:
            return None
            
        data = df[["Close"]].values
        
        # เตรียมข้อมูล
        scaled = scaler.fit_transform(data)
        X, y = [], []
        for i in range(60, len(scaled)):
            X.append(scaled[i-60:i])
            # Label: ถ้าวันถัดไปขึ้น = 1, ลง = 0
            y.append(1 if data[i][0] > data[i-1][0] else 0)
        
        X, y = np.array(X), np.array(y)
        
        # Train/Test Split (ใช้ข้อมูลล่าสุดเป็น test)
        split = int(0.9 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        # สร้างและเทรนโมเดล
        model = create_lstm_model()
        early_stop = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)
        model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0, callbacks=[early_stop])
        
        # ทำนายวันล่าสุด
        last_60 = scaled[-60:].reshape(1, 60, 1)
        pred = model.predict(last_60, verbose=0)[0][0]
        
        # แปลงเป็น confidence
        confidence = float(pred if pred > 0.5 else 1-pred)
        signal = "BUY" if pred > 0.5 else "SELL"
        
        if confidence < 0.60:  # กรองของไม่ชัวร์
            return None
            
        return {
            "symbol": symbol,
            "signal": signal,
            "confidence": round(confidence, 3),
            "price": round(df["Close"].iloc[-1], 2),
            "model": "LSTM"
        }
    except:
        return None

# ฟังก์ชันสำหรับ Streamlit เรียกใช้
def scan_all():
    results = []
    for symbol in ALL_ASSETS:
        sig = get_lstm_signal(symbol)
        if sig:
            results.append(sig)
    return sorted(results, key=lambda x: x["confidence"], reverse=True)