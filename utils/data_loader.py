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
        Maneja archivos con o sin delimitador
        """
        filename = f"{coin}_{timeframe}.csv"
        filepath = os.path.join(self.data_path, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️ Archivo no encontrado: {filepath}")
            return None
        
        try:
            # Intentar cargar con coma como delimitador
            df = pd.read_csv(filepath, sep=',', engine='python')
            
            # Si solo hay una columna, es que está mal delimitado
            if len(df.columns) == 1:
                print(f"⚠️ Formato CSV incorrecto para {filename}, intentando parsearlo...")
                df = self._parse_malformed_csv(filepath)
            
            if df is None or df.empty:
                print(f"❌ No se pudo cargar {filename}")
                return None
            
            # Renombrar columnas al formato esperado
            df = self._normalize_columns(df)
            
            # Verificar columnas necesarias
            required_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            if not all(col in df.columns for col in required_cols):
                print(f"❌ Archivo {filename} no tiene columnas esperadas")
                print(f"   Columnas encontradas: {df.columns.tolist()}")
                return None
            
            # Convertir timestamp a datetime
            # Si está en milisegundos (13 dígitos), convertir a segundos
            if df['timestamp'].iloc[0] > 1e12:
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            else:
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            
            df = df.set_index('timestamp')
            df = df.sort_index()
            
            # Convertir a tipos numéricos
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            print(f"✅ Cargados {len(df)} registros de {coin} en {timeframe}")
            return df
        
        except Exception as e:
            print(f"❌ Error cargando {filename}: {e}")
            return None
    
    def _parse_malformed_csv(self, filepath):
        """Parsea archivos CSV mal formateados (sin delimitador adecuado)"""
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            if not lines:
                return None
            
            # Procesar cada línea
            data = []
            headers = None
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                # Primera línea es header
                if i == 0:
                    headers = line.split(',')
                    continue
                
                # Parsear cada línea separada por comas
                values = line.split(',')
                if len(values) == len(headers):
                    data.append(values)
            
            if not data:
                return None
            
            df = pd.DataFrame(data, columns=headers)
            return df
        
        except Exception as e:
            print(f"❌ Error parseando CSV malformado: {e}")
            return None
    
    def _normalize_columns(self, df):
        """Normaliza nombres de columnas al formato esperado"""
        column_mapping = {
            'time': 'timestamp',
            'timestamp': 'timestamp',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume'
        }
        
        # Convertir nombres a minúsculas para matching
        df.columns = df.columns.str.lower().str.strip()
        
        # Renombrar según mapping
        df = df.rename(columns=column_mapping)
        
        return df
    
    def list_available_coins(self):
        """Lista monedas disponibles en la carpeta de datos"""
        if not os.path.exists(self.data_path):
            print(f"❌ Carpeta no existe: {self.data_path}")
            return []
        
        files = os.listdir(self.data_path)
        csv_files = [f for f in files if f.endswith('.csv')]
        coins = list(set([f.split('_')[0] for f in csv_files]))
        
        return sorted(coins)
