# Configuration Central del Bot

# Capital y Riesgo
INITIAL_CAPITAL = 1000  # USD
RISK_PER_TRADE_LOW = 0.01  # 1% - bajo confluencia
RISK_PER_TRADE_HIGH = 0.02  # 2% - alta confluencia
MAX_LEVERAGE = 5  # Máximo apalancamiento
MIN_LEVERAGE = 1

# Timeframes
PRIMARY_TIMEFRAME = '5m'  # Timeframe de entrada
HTF_TIMEFRAMES = ['1h', '4h', '1D']  # HTF para contexto

# Indicadores
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
ATR_PERIOD = 14
ATR_MULTIPLIER = 1.5  # Para SL
EMA_PERIODS = [9, 20, 50, 200]

# Confluencia (Score)
CONFLUENCE_THRESHOLD_LOW = 3  # Mínimo 3 factores para entrar
CONFLUENCE_THRESHOLD_HIGH = 4  # 4+ = riesgo 2%
FACTORS = {
    'order_block': 1,
    'rsi_extreme': 1,
    'support_resistance': 1,
    'volume_profile': 1,
    'trend_alignment': 1
}

# TP/SL
RISK_REWARD_RATIO = 2  # Buscamos 1:2 mínimo
TP_MULTIPLIER_ATR = 2.5  # TP = entrada + (2.5 × ATR)

# Gestión de Operaciones
MAX_OPEN_POSITIONS = 3  # Máximo 3 operaciones simultáneas
MAX_DAILY_LOSS = 0.05  # 5% de loss diario = pause
MAX_CONSECUTIVE_LOSSES = 3  # 3 pérdidas seguidas = pause 1h

# Horarios (UTC)
TRADING_START = 0  # Hora de inicio (24h format)
TRADING_END = 23  # Hora de fin
SKIP_HOURS = []  # Horas a saltar (ej: [15, 16] para NY apertura volatile)

# Datos
DATA_PATH = r'D:\Desktop\mi_bot\cache'  # Ruta de datos
LOGS_PATH = './logs'

# Bybit
BYBIT_TESTNET = True  # Cambiar a False para producción
BYBIT_CATEGORY = 'linear'  # linear = futuros perpetuos

# Debug
VERBOSE = True
BACKTEST_MODE = True  # True = backtesting, False = live trading
