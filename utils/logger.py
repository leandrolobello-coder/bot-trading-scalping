import csv
import os
import pandas as pd
from datetime import datetime
from config.settings import LOGS_PATH

class Logger:
    """Sistema de logging para operaciones"""
    
    def __init__(self, log_file='operations.csv'):
        os.makedirs(LOGS_PATH, exist_ok=True)
        self.log_file = os.path.join(LOGS_PATH, log_file)
        self.ensure_header()
    
    def ensure_header(self):
        """Asegura que el archivo CSV tenga headers"""
        if not os.path.exists(self.log_file):
            headers = [
                'timestamp', 'coin', 'direction', 'entry_price', 'exit_price',
                'stop_loss', 'take_profit', 'position_size', 'leverage',
                'pnl', 'pnl_pct', 'exit_type', 'score', 'risk_level', 'duration_minutes'
            ]
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
    
    def log_trade(self, trade_data):
        """Registra una operación en el log"""
        trade_data['timestamp'] = datetime.now().isoformat()
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=trade_data.keys())
            writer.writerow(trade_data)
    
    def get_logs_df(self):
        """Lee el archivo de logs como DataFrame"""
        if not os.path.exists(self.log_file):
            return None
        return pd.read_csv(self.log_file)
