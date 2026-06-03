import pandas as pd
import numpy as np
from config.settings import RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD, FACTORS

class ConfluenceAnalyzer:
    """Detecta confluencia de múltiples factores para score de probabilidad"""
    
    def __init__(self):
        self.factors = FACTORS
    
    def calculate_rsi(self, df, period=RSI_PERIOD):
        """Calcula RSI"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def detect_rsi_extreme(self, rsi):
        """Detecta RSI en zona de sobreventa/sobrecompra"""
        last_rsi = rsi.iloc[-1]
        if last_rsi < RSI_OVERSOLD:
            return 'oversold', 1
        elif last_rsi > RSI_OVERBOUGHT:
            return 'overbought', 1
        return None, 0
    
    def detect_support_resistance(self, df, lookback=20):
        """Detecta soportes y resistencias recientes"""
        recent = df.tail(lookback)
        resistance = recent['high'].max()
        support = recent['low'].min()
        current = df['close'].iloc[-1]
        
        # Detecta si está cerca de soporte/resistencia
        range_pct = (resistance - support) / support * 100
        
        if (current - support) / support * 100 < 0.5:
            return 'support', 1
        elif (resistance - current) / current * 100 < 0.5:
            return 'resistance', 1
        return None, 0
    
    def calculate_confluence_score(self, df):
        """Calcula score de confluencia (0-5)"""
        score = 0
        signals = {}
        
        # RSI Extreme
        rsi = self.calculate_rsi(df)
        rsi_signal, rsi_score = self.detect_rsi_extreme(rsi)
        score += rsi_score
        signals['rsi'] = {'signal': rsi_signal, 'score': rsi_score}
        
        # Support/Resistance
        sr_signal, sr_score = self.detect_support_resistance(df)
        score += sr_score
        signals['support_resistance'] = {'signal': sr_signal, 'score': sr_score}
        
        # Volume
        volume_signal, volume_score = self.detect_volume_spike(df)
        score += volume_score
        signals['volume'] = {'signal': volume_signal, 'score': volume_score}
        
        return score, signals
    
    def detect_volume_spike(self, df, lookback=20):
        """Detecta picos de volumen"""
        avg_volume = df['volume'].tail(lookback).mean()
        last_volume = df['volume'].iloc[-1]
        
        if last_volume > avg_volume * 1.5:
            return 'volume_spike', 1
        return None, 0
