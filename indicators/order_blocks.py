import pandas as pd
import numpy as np

class OrderBlockDetector:
    """Detecta Order Blocks (zonas de absorción de órdenes institucionales)"""
    
    def __init__(self, lookback=50):
        self.lookback = lookback
    
    def detect_ob(self, df):
        """Detecta Order Blocks recientes"""
        recent = df.tail(self.lookback)
        
        # Detecta cambios de dirección (potencial OB)
        recent['direction_change'] = (recent['close'] > recent['open']).astype(int).diff()
        
        # Busca zonas donde hubo reversión (potencial OB)
        obs = []
        for i in range(1, len(recent) - 1):
            if recent['direction_change'].iloc[i] != 0:  # Cambio de dirección
                # OB en el rango de la vela anterior
                ob = {
                    'time': recent.index[i-1],
                    'high': recent['high'].iloc[i-1],
                    'low': recent['low'].iloc[i-1],
                    'close': recent['close'].iloc[i-1]
                }
                obs.append(ob)
        
        return obs
    
    def check_ob_touch(self, current_price, obs):
        """Verifica si el precio actual toca un OB reciente"""
        if not obs:
            return None, 0
        
        # Último OB
        last_ob = obs[-1]
        
        if last_ob['low'] <= current_price <= last_ob['high']:
            return last_ob, 1
        
        return None, 0
