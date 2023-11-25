                                    # W - Pattern Bollinger Band Trading_strategy
                                                ****Abstract****
This research provides the trading strategy using the Bollinger Bands, a widely acclaimed 
technical analysis tool, that has become an indispensable asset for traders seeking to navigate the 
turbulent waters of financial markets. These bands offer a unique perspective on price volatility, helping 
traders make informed decisions. As a rule, touching and crossing of Bollinger Bands is interpreted as 
the beginning of a trend movement. In order to visualize the “squeezing ” and “expansion” of the prices, 
it is always used along with a trading signal such as Bottom W, Top M, Head-Shoulder-Bottom. In this 
discussion we discuss only Bottom ‘W’. Top ‘M’ is an inverse of bottom ’W’.


**BOLLINGER BANDS “W” PATTERN TRADING STRATEGY**
(Refer Picture Below) Bollinger Bands consist of a band of three lines which are plotted in 
relation to security prices. The Dotted line in the middle is usually a Simple Moving Average (SMA) set to 
a period of 20 days (The type of trend line and period can be changed by the trader; however a 20 day 
moving average is by far the most popular). The SMA then serves as a base for the Upper and Lower 
Bands. The Upper and Lower Bands are used as a way to measure volatility by observing the relationship 
between the Bands and price. Typically the Upper and Lower Bands are set to two standard deviations 
away from the SMA (The Middle Line); however the number of standard deviations can also be adjusted 
by the trader.



**Strategy** 
**BB CALCULATION**
There are three bands when using Bollinger Bands
Middle Band – 20 Day Simple Moving Average
Upper Band – 20 Day Simple Moving Average + (Standard Deviation x 2)
Lower Band – 20 Day Simple Moving Average - (Standard Deviation x 2)

**W PATTERN STRATEGY** : The formation’s first bottom is characterized by a sharp price pullback that 
closes outside of the lower Bollinger Band. These kinds of moves usually result in what is known as an 
“automatic rally.” The automatic rally’s high usually serves as the first level of resistance in the basebuilding process before the stock moves higher. After the rally begins, the price attempts to retest the 
most recent lows in order to test the strength of the buying pressure that came in at that bottom. The 5 
nodes of the W shape has certain conditions set that determines when to enter and exit the trade.

**Pattern Recognition:**
The code goes through the DataFrame row by row (represented by the loop variable top_right) 
and attempts to identify a specific pattern that resembles the letter 'W'. This 'W' pattern is associated 
with a trading signal.

• **Bottom W Pattern Recognition**: Conditions 1, 2, 3, and 4 are checked in a nested 
manner to identify the 'W' pattern. Conditions involve checking the relationship 
between the price and the Bollinger Bands at various points in the 'W' pattern. If all 
conditions are met, a signal is generated, and the coordinates of the 'W' pattern are 
stored in the 'coordinates' column.
• **Contraction Period Recognition**: If the 'W' pattern is not identified, the code checks 
if the current row is in a contraction period. This is determined by checking if the 
standard deviation (STD) is smaller than beta. If true, a signal is generated indicating a 
contraction period.

**Output**: The resulting DataFrame (df) contains the original data along with the 'signals' column 
indicating buy (1), sell (-1), or no action (0) signals, and the 'coordinates' column storing the coordinates 
of the identified 'W' patterns.

**Function Logic to Plot**
1. **Selecting Data for Plotting**:
• The code selects a subset of the input DataFrame (plot_df) based on the first two nonzero entries in the 'signals' column. These entries are assumed to represent the entry 
and exit points for a trading position.

• The selected subset is expanded to include 85 rows before the entry point and 30 rows 
after the exit point.
2. **Plotting**:
• A matplotlib figure is created.
• Subplots are added, and the main plot (axis) is assigned to the first subplot.
3.**Price Series and Bollinger Bands**:
• The price series is plotted in black.
• The moving average ('mid band') is plotted with a dashed line.
• The upper and lower Bollinger Bands are plotted in green and red, respectively.
• The area between the upper and lower bands is filled with a yellow color to highlight the 
Bollinger Bands range.
4. **Trading Signals**:
• Long (buy) signals are marked with an upward-pointing triangle ('^') at the 
corresponding price points.
• Short (sell) signals are marked with a downward-pointing triangle ('v') at the 
corresponding price points.
5. **Plotting the "W" Shape**:
• The coordinates of the 'W' pattern are extracted from the 'coordinates' column for long 
signals.
• The 'W' shape is then plotted in a thicker line with a pink color.
6. **Displaying the Plot**:
• The plot is displayed using plt.show()
