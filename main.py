#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Trading Scalping - Professional Edition
Entry point principal
"""

import sys
import pandas as pd
from utils.data_loader import DataLoader
from backtester.engine import BacktestEngine
from backtester.analyzer import BacktestAnalyzer
from config.settings import BACKTEST_MODE, VERBOSE

def main():
    print("\n" + "="*60)
    print("🤖 BOT TRADING SCALPING - PROFESSIONAL EDITION")
    print("="*60)
    
    # Cargar datos
    loader = DataLoader()
    coins = loader.list_available_coins()
    
    if not coins:
        print("❌ No hay datos en la carpeta especificada")
        return
    
    print(f"\n✅ Monedas disponibles: {', '.join(coins[:10])}...")
    print(f"Total: {len(coins)} monedas")
    
    # Ejecutar backtest
    if BACKTEST_MODE:
        print("\n🔄 Iniciando BACKTEST...")
        backtester = BacktestEngine()
        
        all_trades = []
        
        # Backtestear primeras monedas para análisis rápido
        test_coins = coins[:5] if len(coins) > 5 else coins
        
        for coin in test_coins:
            df = loader.load_coin_data(coin, '5m')
            if df is not None:
                trades = backtester.backtest(df, coin=coin)
                all_trades.extend(trades)
        
        # Analizar resultados
        if all_trades:
            trades_df = pd.DataFrame(all_trades)
            results = BacktestAnalyzer.analyze(trades_df)
            BacktestAnalyzer.print_results(results)
            
            # Guardar trades
            trades_df.to_csv('./logs/backtest_results.csv', index=False)
            print(f"\n💾 Resultados guardados en ./logs/backtest_results.csv")
        else:
            print("\n❌ Sin trades generados en el backtest")
    
    print("\n✅ Proceso completado")

if __name__ == '__main__':
    main()
