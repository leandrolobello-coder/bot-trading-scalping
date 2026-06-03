import pandas as pd
import os
from config.settings import DATA_PATH

class DataLoader:
    """Carga datos históricos desde archivos CSV"""
    
    def __init__(self, data_path=DATA_PATH):
        self.data_path = data_path
    
    def load_coin_data(self, coin, timeframe='5m'):
        """
        Carga datos de una moneda específica
        Espera archivos con formato: {coin}_{timeframe}.csv
        """
        filename = f"{coin}_{timeframe}.csv"
        filepath = os.path.join(self.data_path, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️ Archivo no encontrado: {filepath}")
            return None
        
        try:
            df = pd.read_csv(filepath)
            
            # Asegurar que tenemos las columnas necesarias
            required_cols = ['time', 'open', 'high', 'low', 'close', 'volume']
            if not all(col in df.columns for col in required_cols):
                print(f"❌ Archivo {filename} no tiene columnas esperadas")
                return None
            
            # Convertir time a datetime
            df['time'] = pd.to_datetime(df['time'])
            df = df.set_index('time')
            df = df.sort_index()
            
            print(f"✅ Cargados {len(df)} registros de {coin} en {timeframe}")
            return df
        
        except Exception as e:
            print(f"❌ Error cargando {filename}: {e}")
            return None
    
    def list_available_coins(self):
        """Lista monedas disponibles en la carpeta de datos"""
        if not os.path.exists(self.data_path):
            print(f"❌ Carpeta no existe: {self.data_path}")
            return []
        
        files = os.listdir(self.data_path)
        csv_files = [f for f in files if f.endswith('.csv')]
        coins = list(set([f.split('_')[0] for f in csv_files]))
        
        return sorted(coins)
