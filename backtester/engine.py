import pandas as pd
import numpy as np
from strategy.scalping_strategy import ScalpingStrategy
from risk_management.position_sizing import PositionSizing
from config.settings import INITIAL_CAPITAL
import csv
from datetime import datetime

class BacktestEngine:
    """Motor de backtesting para la estrategia"""
    
    def __init__(self, capital=INITIAL_CAPITAL):
        self.strategy = ScalpingStrategy()
        self.risk_manager = PositionSizing(capital)
        self.capital = capital
        self.trades = []
        self.positions = []
    
    def backtest(self, df, coin='UNKNOWN', timeframe='5m'):
        """
        Ejecuta backtest en los datos
        """
        print(f"\n🔄 Backtesting {coin} en {timeframe}...")
        
        trades = []
        current_position = None
        
        for i in range(100, len(df)):  # Empezar desde vela 100 (warm-up)
            current_bar = df.iloc[i]
            window_df = df.iloc[:i]
            
            # Si no hay posición abierta
            if current_position is None:
                # Analizar señal
                signal = self.strategy.analyze_signal(window_df)
                
                if signal['has_signal'] and signal['direction']:
                    # Calcular levels
                    levels = self.strategy.calculate_position_levels(
                        window_df,
                        signal['direction'],
                        0.01 if signal['risk_level'] == 'low' else 0.02,
                        1  # leverage base
                    )
                    
                    # Calcular tamaño de posición
                    leverage = self.risk_manager.calculate_leverage(signal['score'])
                    pos_size = self.risk_manager.calculate_position_size(
                        levels['entry'],
                        levels['stop_loss'],
                        signal['risk_level'],
                        leverage
                    )
                    
                    current_position = {
                        'entry_time': current_bar.name,
                        'entry_price': levels['entry'],
                        'stop_loss': levels['stop_loss'],
                        'take_profit': levels['take_profit'],
                        'direction': signal['direction'],
                        'position_size': pos_size['position_size_leveraged'],
                        'leverage': leverage,
                        'score': signal['score'],
                        'risk_level': signal['risk_level']
                    }
            
            # Si hay posición abierta, chequear cierre
            elif current_position is not None:
                entry = current_position['entry_price']
                sl = current_position['stop_loss']
                tp = current_position['take_profit']
                direction = current_position['direction']
                current_price = current_bar['close']
                
                closed = False
                
                if direction == 'long':
                    if current_price <= sl:
                        # Hit SL
                        pnl = (sl - entry) * current_position['position_size']
                        closed = True
                        exit_type = 'SL'
                    elif current_price >= tp:
                        # Hit TP
                        pnl = (tp - entry) * current_position['position_size']
                        closed = True
                        exit_type = 'TP'
                else:  # short
                    if current_price >= sl:
                        # Hit SL
                        pnl = (entry - sl) * current_position['position_size']
                        closed = True
                        exit_type = 'SL'
                    elif current_price <= tp:
                        # Hit TP
                        pnl = (entry - tp) * current_position['position_size']
                        closed = True
                        exit_type = 'TP'
                
                if closed:
                    trade = {
                        'coin': coin,
                        'entry_time': current_position['entry_time'],
                        'exit_time': current_bar.name,
                        'entry_price': entry,
                        'exit_price': current_price,
                        'direction': direction,
                        'position_size': current_position['position_size'],
                        'leverage': current_position['leverage'],
                        'pnl': pnl,
                        'pnl_pct': (pnl / (entry * current_position['position_size'])) * 100,
                        'exit_type': exit_type,
                        'score': current_position['score'],
                        'risk_level': current_position['risk_level']
                    }
                    trades.append(trade)
                    
                    # Actualizar capital
                    new_capital = self.risk_manager.update_capital(pnl)
                    trade['capital_after'] = new_capital
                    
                    current_position = None
        
        self.trades.extend(trades)
        return trades
    
    def get_results_df(self):
        """Retorna trades como DataFrame"""
        if not self.trades:
            return pd.DataFrame()
        return pd.DataFrame(self.trades)
