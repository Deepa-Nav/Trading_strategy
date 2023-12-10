import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import quantstats as qs
import yfinance as yf
import datetime as dt 



class Backtest_LongShort_SMA_Crossover_Strategy:
    def init(self,ticker,start_date,end_date,short_ma,long_ma):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.short_ma = short_ma
        self.long_ma = long_ma
        
        # Automatically executes the function upon object creation
        self.fetch_data()
        self.indicators()
        self.signals()
        self.positions()
        self.returns()
    
    def fetch_data(self):
        self.df = yf.download(self.ticker,self.start_date,self.end_date)
        
    def indicators(self):
        self.df['short_ma'] = self.df['Adj Close'].rolling(window = self.short_ma,min_periods = 1,center = False).mean()
        self.df['long_ma'] = self.df['Adj Close'].rolling(window = self.long_ma,min_periods = 1,center = False).mean()
        self.df['previous_short_ma'] = self.df['short_ma'].shift(1)
        self.df['previous_long_ma'] = self.df['long_ma'].shift(1)
        self.df.dropna(inplace = True)
        
    def signals(self):
        self.df['signal'] = np.where((self.df['short_ma'] > self.df['long_ma']) & (self.df['previous_short_ma'] < self.df['previous_long_ma'],1,0))
        self.df['signal'] = np.where((self.df['short_ma'] < self.df['long_ma']) & (self.df['previous_short_ma'] > self.df['previous_long_ma'],-1,self.df['signal']))
        
    def positions(self):
        self.df['position'] = self.df['signal'].replace(to_replace = 0,method = 'ffill')
        
    def returns(self):
        self.df['bnh_returns'] = np.log(self.df['Adj Close']/self.df['Adj Close'].shift(1))
        self.df['strategy_returns'] = self.df['bnh_returns'] * self.df['position'].shift(1)
        self.df.dropna(inplace = True)
        print("Total_returns:",np.round(self.df['strategy_returns'].cumsum()[-1]),2)
        return self.df['strategy_returns'].cumsum()[-1]
    
    def analysis(self):
        self.df['short_ma','long_ma','positions'].plot(subplots = True,layout = (3,1),figsize = (15,10))
        plt.show()
        
        self.df[['bnh_returns','strategy_returns']].cumsum().plot(figsize = (15,10))
        plt.show()
        
        qs.reports.full(self.df['strategy_returns'].cumsum()[-1])
        
    # main function
    def main():
        end_date = dt.datetime(2023,11,5).date()
        start_date =end_date - dt.timedelta(days = 365*5)
        nifty_10_20 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,10,20)
        nifty_5_20 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,5,20)
        nifty_5_10 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,5,10)
        nifty_5_50 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,5,50)
        nifty_10_50 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,10,50)
        
        nifty_10_20.analysis()
        
    if __name__ == '__main__':
        main()
        
        
        
    
        
        
    
        

        
    