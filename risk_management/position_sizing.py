import numpy as np
from config.settings import INITIAL_CAPITAL, RISK_PER_TRADE_LOW, RISK_PER_TRADE_HIGH, MAX_LEVERAGE

class PositionSizing:
    """Calcula tamaño de posición basado en riesgo adaptativo"""
    
    def __init__(self, capital=INITIAL_CAPITAL):
        self.initial_capital = capital
        self.current_capital = capital
    
    def calculate_position_size(self, entry, stop_loss, risk_level='low', leverage=1):
        """
        Calcula cantidad de contratos/coins a operar
        
        risk_level: 'low' (1%) o 'high' (2%)
        """
        
        # Determinar % de riesgo
        risk_pct = RISK_PER_TRADE_LOW if risk_level == 'low' else RISK_PER_TRADE_HIGH
        
        # Dinero a riesgar
        risk_amount = self.current_capital * risk_pct
        
        # Distancia SL
        sl_distance = abs(entry - stop_loss)
        
        if sl_distance == 0:
            return 0
        
        # Tamaño de posición sin leverage
        position_size = risk_amount / sl_distance
        
        # Aplicar leverage (multiplicar por leverage)
        position_size_leveraged = position_size * leverage
        
        return {
            'position_size': position_size,
            'position_size_leveraged': position_size_leveraged,
            'risk_amount': risk_amount,
            'leverage': leverage,
            'sl_distance': sl_distance
        }
    
    def calculate_leverage(self, score):
        """
        Calcula leverage adaptativo según score de confluencia
        Score 3-5: 1x-5x
        """
        if score < 3:
            return 1
        elif score == 3:
            return 2
        elif score == 4:
            return 3
        else:  # score >= 5
            return min(5, MAX_LEVERAGE)
    
    def update_capital(self, pnl):
        """Actualiza capital después de operación"""
        self.current_capital += pnl
        return self.current_capital
