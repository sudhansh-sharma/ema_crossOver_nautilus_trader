# EagleQ Algorithmic Trading Strategy

A Moving Average Crossover Strategy implementation for E-mini S&P 500 futures trading, built with Nautilus Trader and Databento.

## Overview

This project implements a simple yet effective algorithmic trading strategy based on moving average crossovers. The strategy uses two moving averages (20-period fast and 50-period slow) to generate buy and sell signals for E-mini S&P 500 futures.

## Strategy Details

- **Fast Moving Average**: 20 periods
- **Slow Moving Average**: 50 periods
- **Instrument**: E-mini S&P 500 futures (ES)
- **Timeframe**: 1-minute bars
- **Signal Logic**: 
  - Buy when fast MA crosses above slow MA
  - Sell when fast MA crosses below slow MA

## Project Structure

```
ema_crossOver_nautilus_trader/
├── src/                    # Source code
│   ├── __init__.py
│   ├── loaders/           # Data loading modules
│   │   ├── __init__.py
│   │   └── databento_loader.py  # Databento data integration
│   └── run_backtest.py    # Main backtest script
├── data/                  # Data storage
│   ├── GLBX.MDP3_ES.FUT_2024-01-01T00:00:00-2024-12-31T23:59:59.ohlcv-1m.csv
│   └── GLBX.MDP3_ES.FUT_2024-01-01T00:00:00-2024-12-31T23:59:59.ohlcv-1m.dbn.zst
├── logs/                  # Execution logs
│   └── es_ema_cross_backtest.log
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Quick Start

### 1. Prerequisites

- Python 3.10 or higher
- Databento API key (free account available at [databento.com](https://databento.com))

### 2. Installation

```bash
# Clone or download the project
cd ema_crossOver_nautilus_trader

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

#### Setting up Databento API Key

The project requires a Databento API key to fetch market data. You can set it up in several ways:

**Environment Variable (Recommended)**
```bash
export DATABENTO_API_KEY=your_api_key_here
```

### 4. Data Pipeline Workflow

#### Step 1: Download Market Data (First Time Setup)

Before running the backtest, you need to download the market data using the databento_loader.py:

```bash
# Navigate to the loaders directory
cd src/loaders

# Run the data loader (requires DATABENTO_API_KEY to be set)
python databento_loader.py
```

This script will:
- Connect to Databento API using your API key
- Download E-mini S&P 500 futures data for 2024 (1-minute OHLCV bars)
- Save two files in the `data/` directory:
  - `GLBX.MDP3_ES.FUT_2024-01-01T00:00:00-2024-12-31T23:59:59.ohlcv-1m.dbn.zst` (binary format for Nautilus Trader)
  - `GLBX.MDP3_ES.FUT_2024-01-01T00:00:00-2024-12-31T23:59:59.ohlcv-1m.csv` (human-readable format)

**Note**: The `.dbn.zst` file is the compressed Databento native format that Nautilus Trader uses directly for high-performance backtesting.

#### Step 2: Run the Backtest

Once the data is downloaded, run the backtest:

```bash
# From the project root
cd src
python run_backtest.py
```

The backtest script will:
- Load the `.dbn.zst` file using Nautilus Trader's DatabentoDataLoader
- Apply the EMA crossover strategy (20-period fast, 50-period slow)
- Generate comprehensive performance reports
- Log all execution details to `logs/es_ema_cross_backtest.log`