# ============================================================================
# JEXA Stock Scanner - Simplified
# ============================================================================

import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict

class StockScanner:
    """Simple stock scanner"""
    
    def __init__(self, symbols: List[str]):
        self.symbols = symbols
    
    def calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate indicators"""
        try:
            close = df['Close']
            
            # Basic metrics
            current_price = close.iloc[-1]
            price_change_5d = ((close.iloc[-1] / close.iloc[-5]) - 1) * 100
            
            # Volume
            volume = df['Volume'].iloc[-1]
            avg_volume_20 = df['Volume'].rolling(20).mean().iloc[-1]
            volume_ratio = volume / avg_volume_20 if avg_volume_20 > 0 else 1.0
            
            # Moving Averages
            sma_20 = close.rolling(20).mean().iloc[-1]
            sma_50 = close.rolling(50).mean().iloc[-1]
            
            # RSI
            delta = close.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = -delta.where(delta < 0, 0).rolling(14).mean()
            rs = gain / (loss + 1e-10)
            rsi = (100 - 100 / (1 + rs)).iloc[-1]
            
            return {
                'current_price': current_price,
                'price_change_5d': price_change_5d,
                'volume_ratio': volume_ratio,
                'rsi': rsi,
                'sma_20': sma_20,
                'sma_50': sma_50,
            }
        except:
            return None
    
    def scan(self, scan_type: str = "momentum") -> List[Dict]:
        """Run scan"""
        results = []
        
        for symbol in self.symbols[:20]:  # Limit to 20 for speed
            try:
                df = yf.download(symbol, period="6mo", progress=False, auto_adjust=True)
                
                if df.empty or len(df) < 50:
                    continue
                
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                
                indicators = self.calculate_indicators(df)
                
                if not indicators:
                    continue
                
                # Simple scoring
                score = 50
                
                if indicators['rsi'] > 50:
                    score += 20
                if indicators['current_price'] > indicators['sma_20']:
                    score += 15
                if indicators['volume_ratio'] > 1.5:
                    score += 15
                
                if score >= 70:
                    results.append({
                        'symbol': symbol,
                        'price': indicators['current_price'],
                        'change_5d': f"{indicators['price_change_5d']:+.1f}%",
                        'volume_ratio': f"{indicators['volume_ratio']:.1f}x",
                        'rsi': f"{indicators['rsi']:.0f}",
                        'signal': 'BUY' if score > 80 else 'WATCH',
                        'score': score,
                        'reason': scan_type.title()
                    })
                
            except Exception as e:
                continue
        
        return sorted(results, key=lambda x: x['score'], reverse=True)