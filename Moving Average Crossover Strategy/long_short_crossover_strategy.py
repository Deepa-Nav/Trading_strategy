class Backtest_LongShort_SMA_Crossover_Strategy:
    def init(self,ticker,start_date,end_date,short_ma,long_ma):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.short_ma = short_ma
        self.long_ma = long_ma
        
    