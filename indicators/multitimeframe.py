import pandas as pd
from config.settings import HTF_TIMEFRAMES

class MultiTimeframeAnalyzer:
    """Analiza contexto de mayor timeframe (HTF)"""
    
    def __init__(self, htf_list=HTF_TIMEFRAMES):
        self.htf_list = htf_list
    
    def get_htf_trend(self, df_dict):
        """Obtiene tendencia en HTF (1h, 4h, 1D)"""
        trends = {}
        
        for timeframe in self.htf_list:
            if timeframe in df_dict:
                df = df_dict[timeframe]
                ema9 = df['close'].ewm(span=9).mean()
                ema20 = df['close'].ewm(span=20).mean()
                
                if ema9.iloc[-1] > ema20.iloc[-1]:
                    trends[timeframe] = 'bullish'
                elif ema9.iloc[-1] < ema20.iloc[-1]:
                    trends[timeframe] = 'bearish'
                else:
                    trends[timeframe] = 'neutral'
        
        return trends
    
    def check_trend_alignment(self, trends):
        """Verifica alineamiento de tendencia entre timeframes"""
        if not trends:
            return None, 0
        
        bullish_count = sum(1 for t in trends.values() if t == 'bullish')
        bearish_count = sum(1 for t in trends.values() if t == 'bearish')
        
        if bullish_count >= 2:
            return 'bullish_aligned', 1
        elif bearish_count >= 2:
            return 'bearish_aligned', 1
        else:
            return 'mixed', 0
