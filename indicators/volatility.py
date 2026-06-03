import pandas as pd
import numpy as np
from config.settings import ATR_PERIOD, ATR_MULTIPLIER

class VolatilityAnalyzer:
    """Analiza volatilidad usando ATR y otros indicadores"""
    
    def __init__(self, period=ATR_PERIOD):
        self.period = period
    
    def calculate_atr(self, df):
        """Calcula Average True Range"""
        high = df['high']
        low = df['low']
        close = df['close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=self.period).mean()
        
        return atr
    
    def get_volatility_level(self, atr, price):
        """Clasificia volatilidad como baja/media/alta"""
        atr_pct = (atr.iloc[-1] / price.iloc[-1]) * 100
        
        if atr_pct < 0.5:
            return 'low', 1.0
        elif atr_pct < 1.0:
            return 'medium', 0.8
        else:
            return 'high', 0.6
    
    def calculate_sl_distance(self, df, atr):
        """Calcula distancia del SL basado en ATR"""
        sl_distance = atr.iloc[-1] * ATR_MULTIPLIER
        return sl_distance
    
    def calculate_tp_distance(self, atr, multiplier=2.5):
        """Calcula distancia del TP basado en ATR"""
        tp_distance = atr.iloc[-1] * multiplier
        return tp_distance
