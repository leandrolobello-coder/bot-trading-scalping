import pandas as pd
import numpy as np

class BacktestAnalyzer:
    """Analiza resultados del backtest"""
    
    @staticmethod
    def analyze(trades_df):
        """Calcula métricas de performance"""
        
        if trades_df.empty:
            print("❌ Sin trades para analizar")
            return None
        
        trades = trades_df.copy()
        
        # Métricas básicas
        total_trades = len(trades)
        winning_trades = len(trades[trades['pnl'] > 0])
        losing_trades = len(trades[trades['pnl'] < 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # Ganancias/Pérdidas
        total_pnl = trades['pnl'].sum()
        total_pnl_pct = trades['pnl_pct'].sum()
        avg_win = trades[trades['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades[trades['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        
        # Profit Factor
        gross_profit = trades[trades['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(trades[trades['pnl'] < 0]['pnl'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Drawdown máximo
        cumsum = trades['pnl'].cumsum()
        cummax = cumsum.cummax()
        drawdown = cumsum - cummax
        max_drawdown = drawdown.min()
        max_drawdown_pct = (max_drawdown / cumsum.max()) * 100 if cumsum.max() > 0 else 0
        
        # Por moneda
        by_coin = trades.groupby('coin').agg({
            'pnl': 'sum',
            'direction': 'count'
        }).rename(columns={'direction': 'trades'})
        
        results = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'max_drawdown_pct': max_drawdown_pct,
            'by_coin': by_coin
        }
        
        return results
    
    @staticmethod
    def print_results(results):
        """Imprime resultados de forma legible"""
        print("\n" + "="*60)
        print("📊 RESULTADOS DEL BACKTEST")
        print("="*60)
        
        print(f"\n📈 Estadísticas Generales:")
        print(f"  Total de operaciones: {results['total_trades']}")
        print(f"  Operaciones ganadoras: {results['winning_trades']}")
        print(f"  Operaciones perdedoras: {results['losing_trades']}")
        print(f"  Win Rate: {results['win_rate']:.2f}%")
        
        print(f"\n💰 Ganancias/Pérdidas:")
        print(f"  PnL Total: ${results['total_pnl']:.2f}")
        print(f"  PnL Total %: {results['total_pnl_pct']:.2f}%")
        print(f"  Promedio por trade ganador: ${results['avg_win']:.2f}")
        print(f"  Promedio por trade perdedor: ${results['avg_loss']:.2f}")
        
        print(f"\n📊 Ratios:")
        print(f"  Profit Factor: {results['profit_factor']:.2f}")
        print(f"  Max Drawdown: ${results['max_drawdown']:.2f} ({results['max_drawdown_pct']:.2f}%)")
        
        if not results['by_coin'].empty:
            print(f"\n🪙 Por Moneda:")
            print(results['by_coin'].to_string())
        
        print("\n" + "="*60)
