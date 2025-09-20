"""
Moving Average Crossover Strategy Backtest

This script implements a Moving Average Crossover Strategy for E-mini S&P 500 futures
using the Nautilus Trader framework.

Using Databento for Fetching the 1m close data for ES.FUT symbol
from 2024-01-01T00:00:00 to 2024-12-31T23:59:59
"""

import time
import pandas as pd

from nautilus_trader.backtest.config import BacktestEngineConfig
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.adapters.databento import DatabentoDataLoader
from nautilus_trader.config import LoggingConfig, RiskEngineConfig
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import BarType
from nautilus_trader.model.enums import AccountType, OmsType
from nautilus_trader.model.identifiers import TraderId, Venue
from nautilus_trader.model.objects import Money
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.examples.strategies.ema_cross import EMACross, EMACrossConfig

if __name__ == "__main__":
    print("Moving Average Crossover Strategy Backtest FMA: 20, SMA:50")
    print("=" * 60)
    
    # Configure backtest engine
    config = BacktestEngineConfig(
        trader_id=TraderId("BACKTESTER-001"),
        logging=LoggingConfig(log_level="INFO"),
        risk_engine=RiskEngineConfig(bypass=True),
    )
    bt_engine = BacktestEngine(config=config)

    GLBX_VENUE = Venue("GLBX")
    bt_engine.add_venue(
        venue=GLBX_VENUE,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=USD,
        starting_balances=[Money(100_000.0, USD)],
    )

    # Add E-mini S&P 500 futures instrument
    ES_CME = TestInstrumentProvider.es_future(expiry_year=2024,
                                              expiry_month=3)
    bt_engine.add_instrument(ES_CME)
    
    # Load the Bars into the Backtest Engine
    loader = DatabentoDataLoader()
    filename = 'data/GLBX.MDP3_ES.FUT_2024-01-01T00:00:00-2024-12-31T23:59:59.ohlcv-1m.dbn.zst'

    bars = loader.from_dbn_file(path=filename, instrument_id=ES_CME.id)
    bt_engine.add_data(bars)
    
    # Configure the Moving Average Crossover strategy
    ema_cross_config = EMACrossConfig(
        instrument_id=ES_CME.id,
        bar_type=BarType.from_str(f"{ES_CME.id}-1-MINUTE-LAST-EXTERNAL"),
        fast_ema_period=20,
        slow_ema_period=50,
        trade_size=1
    )
    ema_cross_strategy = EMACross(config=ema_cross_config)
    bt_engine.add_strategy(ema_cross_strategy)
    
    print("\nStrategy Configuration:")
    print(f"Instrument: {ES_CME.id}")
    print(f"Fast MA Period: 20")
    print(f"Slow MA Period: 50")
    print(f"Trade Size: 1")
    print(f"Starting Capital: $100,000")
    
    time.sleep(0.1)
    input("\nPress Enter to start the backtest...")
    
    # Run the backtest engine
    print("\nRunning backtest...")
    bt_engine.run()
    
    # Generate and display reports
    print("\n" + "=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)
    
    with pd.option_context(
        "display.max_rows", 100,
        "display.max_columns", None,
        "display.width", 300,
    ):
        print("\nAccount Report:")
        print(bt_engine.trader.generate_account_report(GLBX_VENUE))
        
        print("\nOrder Fills Report:")
        print(bt_engine.trader.generate_order_fills_report())
        
        print("\nPositions Report:")
        print(bt_engine.trader.generate_positions_report())
    
    print("\nBacktest completed!")
    
    # Clean up
    bt_engine.reset()
    bt_engine.dispose()
