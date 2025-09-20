"""
Data Handler for E-mini S&P 500 Futures Data

This module handles data loading and preparation from Databento for the backtest.
"""

import os
import pandas as pd
from typing import Optional
import databento as db


class DataBento:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the data handler.

        Args:
            api_key: Databento API key. If None, will try to get from environment variable.
        """
        self.api_key = api_key or os.getenv('DATABENTO_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Databento API key is required. Set DATABENTO_API_KEY environment variable or pass it directly.")

        self.client = db.Historical(self.api_key)

    def get_and_store_data(self,
                 start="2024-01-01T00:00:00",
                 end="2024-12-31T23:59:59",
                 dataset="GLBX.MDP3",
                 symbols=["ES.FUT"],
                 stype_in='parent',
                 schema='ohlcv-1m',
                 **kwargs):
        # Fetching Data for the Time Range
        data = self.client.timeseries.get_range(start=start,
                                                  end=end,
                                                  dataset=dataset,
                                                  symbols=symbols,
                                                  stype_in=stype_in,
                                                  schema=schema,
                                                  **kwargs)

        # Cleaning and preparing the Data for the Backtest
        data.to_file(f"data/{dataset}_{symbols[0]}_{start}-{end}.{schema}.dbn.zst")

        df = data.to_df()
        df.reset_index(inplace=True)
        df = df.rename(columns={
            'ts_event': 'timestamp',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume'
        })
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        df = df[df['symbol'] == 'ESH4']
        df = df.drop_duplicates(subset=['timestamp'], keep='last')

        # Adding 1 minute, so timestamp represents the closing time of the bar
        df['timestamp'] = pd.to_datetime(df['timestamp']) + pd.Timedelta(minutes=1)
        df.to_csv(f"data/{dataset}_{symbols[0]}_{start}-{end}.{schema}.csv", index=False)
        return df

if __name__ == "__main__":
    db = DataBento()

    datasets = db.client.metadata.list_datasets()
    print(f"Datesets: {datasets}")

    publishers = db.client.metadata.list_publishers()
    print(f"Publishers: {publishers}")

    schemas = db.client.metadata.list_schemas(dataset="GLBX.MDP3")
    print(f"Schemas: {schemas}")

    fields = db.client.metadata.list_fields(schema="ohlcv-1m", encoding="dbn")
    print(f"Fields: {fields}")

    count = db.client.metadata.get_record_count(
        dataset="GLBX.MDP3",
        symbols=["ES.FUT"],
        stype_in="parent",
        schema="ohlcv-1m",
        start="2024-01-01T00:00:00",
        end="2024-12-31T23:59:59"
    )
    print(f"Count: {count}")

    df = db.get_and_store_data()
    print(df.head(5))
