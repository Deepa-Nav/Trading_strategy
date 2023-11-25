# ma_cross.py

import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pandas_datareader import DataReader
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

class MarketOnClosePortfolio(Portfolio):
    '''
    Encapsulates the portfolio of positions that is based on the signals that is provided by the strategy class
    Requires:
    symbol - A stock symbol which forms the basis of portfolio
    bar - A dataframe of bars for a symbol set
    signals - Dataframe of signals that inculde (1,0,-1) for long, hold and short respectively
    initial_investment - The amount in cash at the start of the portfolio
    '''
    def init(self,symbol,bars,signals,initial_investment= 100000.0):
        self.symbol = symbol
        self.bars = bars
        self.signals = signals
        self.initial_investment = float(initial_investment)
        self.positions = self.generate_positions()
        
    def generate_positions(self):
        positions = pd.DataFrame(index = self.signals.index).fillna(0.0)
        positions[self.symbol] = 100*self.signals['signal']
        return positions
    
    def backtest_portfolio(self):
        portfolio = self.positions*self.bars['Close']
        pos_diff = self.positions.diff()
        portfolio['holdings'] = (self.positions * self.bars['Close']).sum(axis=1)
        portfolio['cash'] = self.initial_investment -(pos_diff * self.bars['Close']).sum(axis=1).cumsum()
        
        portfolio['total'] = portfolio['cash']+portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        return portfolio
        
        
if __name__ == "__main__":
    symbol = 'AAPL'
    bars = DataReader(symbol,"yahoo",datetime.datetime(1990,1,1),datetime.datetime(2002,1,1))
    # Create a Moving Average Cross Strategy instance with a short moving
    # average window of 100 days and a long window of 400 days
    mac = MovingAverageCrossoverStrategy(symbol,bars,short_window = 100,long_window = 400)
    signals = mac.generate_signals()
    
    # Create a portfolio of AAPL, with $100,000 initial capital
    portfolio = MarketOnClosePortfolio(symbol,bars,signals,initial_investment = 100000.0)
    returns = portfolio.backtest_portfolio()
    
    # Plot two charts to assess trades and equity curve
    fig = plt.figure()
    fig.patch.set_facecolor('white')     # Set the outer colour to white
    ax1 = fig.add_subplot(211, ylabel = 'Price in $')
      
    # Plot the AAPL closing price overlaid with the moving averages
    bars['Close'].plot(ax=ax1, color='r', lw=2.)
    signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

    # Plot the "buy" trades against AAPL
    ax1.plot(signals.ix[signals.positions == 1.0].index, 
             signals.short_mavg[signals.positions == 1.0],
             '^', markersize=10, color='m')

    # Plot the "sell" trades against AAPL
    ax1.plot(signals.ix[signals.positions == -1.0].index, 
             signals.short_mavg[signals.positions == -1.0],
             'v', markersize=10, color='k')

    # Plot the equity curve in dollars
    ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
    returns['total'].plot(ax=ax2, lw=2.)

    # Plot the "buy" and "sell" trades against the equity curve
    ax2.plot(returns.ix[signals.positions == 1.0].index, 
             returns.total[signals.positions == 1.0],
             '^', markersize=10, color='m')
    ax2.plot(returns.ix[signals.positions == -1.0].index, 
             returns.total[signals.positions == -1.0],
             'v', markersize=10, color='k')

    # Plot the figure
    fig.show()
    
    
    
    