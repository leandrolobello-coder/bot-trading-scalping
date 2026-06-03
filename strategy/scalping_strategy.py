import pandas as pd
import numpy as np
from indicators.confluence import ConfluenceAnalyzer
from indicators.volatility import VolatilityAnalyzer
from indicators.order_blocks import OrderBlockDetector
from indicators.multitimeframe import MultiTimeframeAnalyzer
from config.settings import (
    CONFLUENCE_THRESHOLD_LOW,
    CONFLUENCE_THRESHOLD_HIGH,
    RISK_REWARD_RATIO,
    PRIMARY_TIMEFRAME
)

class ScalpingStrategy:
    """Estrategia principal de scalping con confluencia y gestión de riesgo"""
    
    def __init__(self):
        self.confluence = ConfluenceAnalyzer()
        self.volatility = VolatilityAnalyzer()
        self.ob_detector = OrderBlockDetector()
        self.mtf_analyzer = MultiTimeframeAnalyzer()
    
    def analyze_signal(self, df, df_dict=None):
        """
        Analiza si hay una señal de entrada válida
        Retorna: (has_signal, direction, score, risk_level)
        """
        
        # Calcular confluencia
        score, signals = self.confluence.calculate_confluence_score(df)
        
        # Analizar volatilidad
        atr = self.volatility.calculate_atr(df)
        vol_level, vol_factor = self.volatility.get_volatility_level(atr, df['close'])
        
        # Detectar Order Blocks
        obs = self.ob_detector.detect_ob(df)
        current_price = df['close'].iloc[-1]
        ob_touch, ob_score = self.ob_detector.check_ob_touch(current_price, obs)
        score += ob_score
        
        # HTF Context (si hay datos)
        direction = None
        if df_dict:
            htf_trends = self.mtf_analyzer.get_htf_trend(df_dict)
            trend_alignment, trend_score = self.mtf_analyzer.check_trend_alignment(htf_trends)
            score += trend_score
            
            # Definir dirección según tendencia
            if 'bullish' in str(trend_alignment):
                direction = 'long'
            elif 'bearish' in str(trend_alignment):
                direction = 'short'
        
        # Determinar si hay señal válida
        has_signal = False
        risk_level = 'low'
        
        if score >= CONFLUENCE_THRESHOLD_HIGH:
            has_signal = True
            risk_level = 'high'  # 2% de riesgo
        elif score >= CONFLUENCE_THRESHOLD_LOW:
            has_signal = True
            risk_level = 'low'   # 1% de riesgo
        
        return {
            'has_signal': has_signal,
            'direction': direction,
            'score': score,
            'risk_level': risk_level,
            'atr': atr.iloc[-1],
            'vol_level': vol_level,
            'signals': signals,
            'ob_touch': ob_touch
        }
    
    def calculate_position_levels(self, df, direction, risk_pct, leverage):
        """
        Calcula entrada, SL y TP
        """
        atr = self.volatility.calculate_atr(df)
        current_price = df['close'].iloc[-1]
        
        # SL basado en última vela baja + ATR
        last_wick_low = df['low'].tail(5).min()
        sl_distance = atr.iloc[-1] * 1.5
        
        if direction == 'long':
            entry = current_price
            stop_loss = last_wick_low
            tp = entry + (atr.iloc[-1] * 2.5)
        else:  # short
            entry = current_price
            stop_loss = last_wick_low
            tp = entry - (atr.iloc[-1] * 2.5)
        
        return {
            'entry': entry,
            'stop_loss': stop_loss,
            'take_profit': tp,
            'atr': atr.iloc[-1]
        }
