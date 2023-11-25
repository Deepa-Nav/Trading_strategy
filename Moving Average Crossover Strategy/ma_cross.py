# ma_cross.py

import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pandas.io.data import DataReader
from backtest import Strategy, Portfolio

class MovingAverageCrossoverStrategy(Strategy):
    """    
    Requires:
    symbol - A stock symbol on which to form a strategy on.
    bars - A DataFrame of bars for the above symbol.
    short_window - Lookback period for short moving average.
    long_window - Lookback period for long moving average.
    """
    
    def init(self,symbol,bars,short_window=100,long_window=400):
        self.symbol = symbol
        self.bars = bars
        self.short_window = short_window
        self.long_window = long_window
        
        
    def generate_signals(self):
        """Returns the DataFrame of symbols containing the signals
        to go long, short or hold (1, -1 or 0)."""
        signals = pd.DataFrame(index=self.bars.index)
        signals['signal'] = 0.0
        
        # Create a set of short and long simple moving averages
        signals['short_ma'] = pd.rolling_mean(self.bars['Close'],self.short_window,min_periods = 1)
        signals['long_ma'] = pd.rolling_mean(self.bars['Close'],self.long_window,min_periods = 1)
        
        # Create a 'signal' (invested or not invested) when the short moving average crosses the long
        # moving average, but only for the period greater than the shortest moving average window
        signals['signal'][self.short_window:] = np.where(signals['short_ma'][self.short_window:]>signals['long_ma'][self.short_window:],1.0,0.0) 
        
        # Take the difference of the signals in order to generate actual trading orders
        signals['positions'] = signals['signal'].diff()
        
        return signals
        
        
        #return super().generate_signals()    

if __name__ == "__main__":
    pass
    