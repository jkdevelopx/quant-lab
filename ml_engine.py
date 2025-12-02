# ============================================================================
# JEXA ML Engine - Complete Working Version
# ============================================================================

import yfinance as yf
import pandas as pd
import numpy as np
import lightgbm as lgb
from typing import Dict, Optional, List
import warnings
warnings.filterwarnings('ignore')

class MLEngine:
    """Machine Learning Engine for predictions"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = None
        self.accuracy = 0.0
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer features"""
        df = df.copy()
        close = df['Close']
        
        # Returns
        df['returns'] = close.pct_change()
        df['returns_5'] = close.pct_change(5)
        df['returns_10'] = close.pct_change(10)
        
        # Moving Averages
        df['sma_5'] = close.rolling(5).mean()
        df['sma_10'] = close.rolling(10).mean()
        df['sma_20'] = close.rolling(20).mean()
        df['sma_50'] = close.rolling(50).mean()
        
        # Ratios
        df['price_to_sma20'] = close / (df['sma_20'] + 1e-10)
        df['price_to_sma50'] = close / (df['sma_50'] + 1e-10)
        
        # RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / (loss + 1e-10)
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = close.ewm(span=12, adjust=False).mean()
        exp2 = close.ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        
        # Volatility
        df['volatility'] = df['returns'].rolling(20).std()
        
        # Volume
        df['volume_ratio'] = df['Volume'] / (df['Volume'].rolling(20).mean() + 1e-10)
        
        # Target
        df['target'] = (close.shift(-1) > close).astype(int)
        
        return df.dropna()
    
    def train(self, symbol: str, period: str = "1y") -> bool:
        """Train model"""
        try:
            df = yf.download(symbol, period=period, progress=False, auto_adjust=True)
            
            if df.empty or len(df) < 100:
                return False
            
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            
            df = self.prepare_features(df)
            
            if len(df) < 50:
                return False
            
            self.feature_columns = [col for col in df.columns 
                                   if col not in ['target', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
            X = df[self.feature_columns]
            y = df['target']
            
            split_idx = int(len(X) * 0.8)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            self.model = lgb.LGBMClassifier(
                objective='binary',
                n_estimators=100,
                learning_rate=0.05,
                num_leaves=31,
                random_state=42,
                verbose=-1
            )
            
            self.model.fit(X_train, y_train)
            self.accuracy = self.model.score(X_test, y_test)
            
            return True
            
        except Exception as e:
            print(f"Training error: {e}")
            return False
    
    def predict(self, symbol: str) -> Optional[Dict]:
        """Generate prediction"""
        try:
            df = yf.download(symbol, period="6mo", progress=False, auto_adjust=True)
            
            if df.empty or len(df) < 100:
                return None
            
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            
            df = self.prepare_features(df)
            
            if len(df) < 10:
                return None
            
            latest = df[self.feature_columns].iloc[-1:]
            current_price = df['Close'].iloc[-1]
            
            proba = self.model.predict_proba(latest)[0]
            direction = "UP" if proba[1] > 0.5 else "DOWN"
            confidence = proba[1] if direction == "UP" else proba[0]
            
            rsi = df['rsi'].iloc[-1]
            volume_ratio = df['volume_ratio'].iloc[-1]
            
            return {
                'symbol': symbol,
                'price': current_price,
                'direction': direction,
                'confidence': confidence,
                'up_probability': proba[1],
                'down_probability': proba[0],
                'model_accuracy': self.accuracy,
                'rsi': rsi,
                'volume_ratio': volume_ratio
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None


class JEXAPredictor:
    """Main predictor class"""
    
    def __init__(self):
        self.models = {}
    
    def get_prediction(self, symbol: str) -> Optional[Dict]:
        """Get prediction for symbol"""
        if symbol in self.models:
            engine = self.models[symbol]
        else:
            engine = MLEngine()
            if not engine.train(symbol):
                return None
            self.models[symbol] = engine
        
        return engine.predict(symbol)
    
    def batch_predict(self, symbols: List[str], max_symbols: int = 20) -> List[Dict]:
        """Predict multiple symbols"""
        results = []
        
        for i, symbol in enumerate(symbols[:max_symbols]):
            print(f"Analyzing {symbol} ({i+1}/{min(len(symbols), max_symbols)})...")
            
            prediction = self.get_prediction(symbol)
            
            if prediction and prediction['confidence'] > 0.60:
                results.append(prediction)
        
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results
    
    def find_next_nvda(self, symbols: List[str], min_confidence: float = 0.70) -> List[Dict]:
        """Find high-potential stocks"""
        print("\n🔍 Finding next NVDA...\n")
        
        candidates = []
        
        for i, symbol in enumerate(symbols[:30], 1):
            print(f"[{i}/30] {symbol}...", end=" ")
            
            try:
                prediction = self.get_prediction(symbol)
                
                if not prediction:
                    print("❌")
                    continue
                
                if (prediction['direction'] == 'UP' and 
                    prediction['confidence'] >= min_confidence and
                    prediction['model_accuracy'] > 0.60):
                    
                    score = self._calculate_score(prediction)
                    prediction['nvda_score'] = score
                    
                    candidates.append(prediction)
                    print(f"✅ {score:.0f}")
                else:
                    print(f"⚠️  {prediction['confidence']:.1%}")
                    
            except Exception as e:
                print("❌")
                continue
        
        candidates.sort(key=lambda x: x['nvda_score'], reverse=True)
        return candidates
    
    def _calculate_score(self, prediction: Dict) -> float:
        """Calculate NVDA-like score"""
        score = 0
        
        score += prediction['confidence'] * 40
        score += prediction['model_accuracy'] * 20
        
        rsi = prediction.get('rsi', 50)
        if 45 < rsi < 65:
            score += 20
        elif 40 < rsi < 70:
            score += 15
        
        vol_ratio = prediction.get('volume_ratio', 1.0)
        if vol_ratio > 2.0:
            score += 20
        elif vol_ratio > 1.5:
            score += 15
        elif vol_ratio > 1.2:
            score += 10
        
        return min(100, score)


# Global predictor instance
_predictor = None

def get_predictor() -> JEXAPredictor:
    """Get predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = JEXAPredictor()
    return _predictor


# Public API functions
def get_ml_signal(symbol: str) -> Optional[Dict]:
    """Get ML signal for symbol"""
    predictor = get_predictor()
    return predictor.get_prediction(symbol)


def scan_market(symbols: List[str], max_results: int = 20) -> List[Dict]:
    """Scan market for signals"""
    predictor = get_predictor()
    return predictor.batch_predict(symbols, max_results)


def find_next_nvda(symbols: List[str], min_confidence: float = 0.70) -> List[Dict]:
    """Find next NVDA"""
    predictor = get_predictor()
    return predictor.find_next_nvda(symbols, min_confidence)