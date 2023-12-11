import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('TkAgg')
import numpy as np
import quantstats as qs
import yfinance as yf
import datetime as dt 



class Backtest_LongShort_SMA_Crossover_Strategy:
    def __init__(self,ticker,start_date,end_date,short_ma,long_ma):
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
        #print(self.df.head(50))
        
    def indicators(self):
        self.df['short_ma'] = self.df['Adj Close'].rolling(window = self.short_ma,min_periods = 1,center = False).mean()
        self.df['long_ma'] = self.df['Adj Close'].rolling(window = self.long_ma,min_periods = 1,center = False).mean()
        self.df['previous_short_ma'] = self.df['short_ma'].shift(1)
        self.df['previous_long_ma'] = self.df['long_ma'].shift(1)
        #self.df.dropna(inplace = True)
        
    def signals(self):
        self.df['signal'] = np.where((self.df['short_ma'] > self.df['long_ma']) & (self.df['previous_short_ma'] < self.df['previous_long_ma']),1,0)
        self.df['signal'] = np.where((self.df['short_ma'] < self.df['long_ma']) & (self.df['previous_short_ma'] > self.df['previous_long_ma']),-1,self.df['signal'])
        
    def positions(self):
        self.df['position'] = self.df['signal'].replace(to_replace = 0,method = 'ffill')
        
    def returns(self):
        self.df['bnh_returns'] = np.log(self.df['Adj Close']/self.df['Adj Close'].shift(1))
        self.df['strategy_returns'] = self.df['bnh_returns'] * self.df['position'].shift(1)
        self.df.dropna(inplace = True)
        #print("Total_returns:",np.round(self.df['strategy_returns'].cumsum()[-1]),2)
        return self.df['strategy_returns'].cumsum()[-1]
    
    def analysis(self,asset,short,long):
        self.df[['short_ma','long_ma','position']].plot(grid = True,secondary_y = 'position',figsize = (15,10))
        plt.title('checking if positions are generated properly')
        #plt.savefig("mygraph1.png")
        file_name = f"{asset}_{short}_{long}"
        folder_name = asset
        self.df[['bnh_returns','strategy_returns']].cumsum().plot(figsize = (15,10),secondary_y = 'position')
        plt.title(f"Buy & hold' vs 'crossover strategy' cumulative returns for {asset}")
        
        plt.savefig(f"/home/deepa/Trading_strategies/Moving Average Crossover Strategy/Report/{file_name}.png")
        plt.show()
        qs.reports.basic(self.df['strategy_returns'])
        
    def sort_returns(stock_list,short_ma_list,long_ma_list):
        end_date = dt.datetime(2023,11,5).date()
        start_date =end_date - dt.timedelta(days = 365*5)
        long_ma = []
        short_ma = []
        net_returns = []
        stock_names = []
        file_name = 'Indian_Instruments_Returns.xlsx'
        
        for stock in stock_list:
            for i in short_ma_list:
                for j in long_ma_list:
                    #print(f"For {i}-{j} time periods")
                    a = Backtest_LongShort_SMA_Crossover_Strategy(stock,start_date,end_date,i,j)
                    
                    long_ma.append(i)
                    short_ma.append(j)
                    net_returns.append(a.returns())
                    stock_names.append(stock)
                    a.analysis(a.ticker,i,j)
        results = pd.DataFrame({'stock_name':stock_names,'long_ma':long_ma,'short_ma':short_ma,'net_returns':net_returns})
        results = results.sort_values(by='net_returns',ascending=False)
        results.to_excel(file_name)
        print(results)
                        
                
        
    # main function
def main():
    
    # end_date = dt.datetime(2023,11,5).date()
    # start_date =end_date - dt.timedelta(days = 365*5)
    # nifty_10_20 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,10,20)
    # nifty_5_20 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,5,20)
    # nifty_5_10 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,5,10)
    # nifty_5_50 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,5,50)
    # nifty_10_50 = Backtest_LongShort_SMA_Crossover_Strategy('^NSEI',start_date,end_date,10,50)
    
    # nifty_10_20.analysis()
    # nifty_5_20.analysis()
    # nifty_5_10.analysis()
    # nifty_5_50.analysis()
    # nifty_10_50.analysis()
    
    # Define a list of assets
    stock_list = [  'BAJFINANCE.NS',
                    # 'TRENT.NS',
                    # 'BPCL.NS'
                    # 'BRITANNIA.NS',
                    # 'COALINDIA.NS', 
                    # 'DRREDDY.NS',
                    # 'GAIL.NS',
                    # 'ASIANPAINT.NS',
                    # 'ASHOKLEY.NS',
                    # 'L&TFH.NS',
                    # 'TCS.NS',
                    # 'LUPIN.NS',
                    # 'CUMMINSIND.NS',
                    # 'COFORGE.NS'                   
                ]
    short_ma_list = [5,10,20]
    long_ma_list = [30,50,100]
    Backtest_LongShort_SMA_Crossover_Strategy.sort_returns(stock_list,short_ma_list,long_ma_list)

        
if __name__ == '__main__':
    main()
        
        
        
    
        
        
    
        

        
    