# Fundamental Stock Analysis Using Python APIs

This article will look at 10 fundamental indicators for stock selection.

Disclaimer: The information provided here is for informational purposes only and is not intended to be personal financial, investment, or other advice.

Key indicators:

EPS (Earnings Per Share) — portion of a company’s profit that is assigned to each share of its stock
P/E (Price to Earnings) — relationship between the stock price of a company and its per-share earnings. It helps investors determine if a stock is undervalued or overvalued relative to others in the same sector.
PEG (Projected Earnings Growth) — calculated by dividing a stock’s P/E by its projected 12-month forward revenue growth rate. In general, a PEG lower than 1 is a good sign, and a PEG higher than 2 indicates that a stock may be overpriced
FCFY (Free Cash Flow Yield) — a financial solvency ratio that compares the free cash flow per share a company is expected to earn against its market value per share. A lower ratio indicates a less attractive investment opportunity.
PB (Price to Book) — a ratio of 1 indicates the company’s shares are trading in line with its book value. A P/B higher than 1 suggests the company is trading at a premium to book value, and a P/B lower than 1 indicates a stock that may be undervalued relative to the company’s assets.
ROE (Return on Equity) — provides a way for investors to evaluate how effectively a company is using its equity to generate profits. A higher ROE indicates a more efficient use of shareholder equity, which can lead to increased demand for shares and higher stock price, as well as increase in company’s profits in the future.
P/S (Price to Sales) — determines the fair value of a stock by utilizing a company’s market capitalization and revenue. It shows how much the market values the company’s sales, which can be effective in valuing growth stocks that have yet to turn a profit or aren’t performing as expected due to a temporary setback.
DPR (Dividend Payment Ratio) — a ratio of the total amount of dividends paid out to shareholders relative to the net income of the company.
DY (Dividend Yield Ratio) — a ratio looks at the amount paid by a company in dividends every year relative to its share price. It is an estimate of the dividend-only return of a stock investment.
CR (Current Ratio) — measures a company’s ability to pay off its current liabilities (payable within one year) with its current assets, such as cash, accounts receivable, and inventories. The higher the ratio, the better the company’s liquidity position.
Beta — is a measure of a stock’s volatility in relation to the overall market. A stock that swings more than the market over time has a beta above 1.0. If a stock moves less than the market, the stock’s beta is less than 1.0.
Data Access
We will use the yfinance API to obtain data from Yahoo Finance. We will focus on the info component of a ticker, which is one of many components (e.g., Income Statement, Cash Flow etc.) provided by the API.

Note:
However, as of October/November 2023, accessing the info component results in a 404 error. To get past this problem, I’m using a workaround suggested on Github. However, only use this solution if you are receiving the 404 error; others have indicated that the problem is region-specific. Furthermore, I’ll use files obtained via a separate program to reduce API calls to YF, which may throttle heavy usage. This software, in addition to the workaround, can be found on Github.

Approach
Download data for each stock symbol to a directory
Use Jupyter notebook to analyze the data
Only Part 2 (analysis) is discussed here, as Part 1 is a simple program to download and save data in JSON format to a directory.

A utility program to download data, a module as a workaround, and a Jupyter notebook are available on GitHub.

Python Libraries
The required Python libraries are:

pandas — use Data Frame
numpy — to access np.nan
json — to work with json data
Import Libraries
import json

# For DataFrame
import pandas as pd
import numpy as np
Configuration
# List of stock symbols we need to run fundamental analysis on - any symbol added here must have the json file
# containing stock info from YF
SYMBOLS = ['INTU','CDNS','WDAY','ROP','TEAM','ADSK','DDOG','ANSS','ZM','PTC',\
           'BSY','GRAB','SSNC','APP','AZPN','MANH','ZI','NICE']

# Path to read stock data from YF
DATA_PATH = 'path to accesss json files'

# Dictionary to collect data to create a DF later
data = {
    'Symbol': [],
    'Name': [],
    'Industry': [],
    'EPS (fwd)': [],
    'P/E (fwd)': [],
    'PEG': [],
    'FCFY' : [],
    'PB': [],
    'ROE' : [],
    'P/S (trail)': [],
    'DPR' : [],
    'DY' : [],
    'CR' : [],
    'Beta': [],
    'Price': [],
    '52w Low': [],
    '52w High': []
    }
Loads data
This is a utility method to extract indicators from the given JSON data and populate the data dictionary

def load_data(json_data):
    data['Symbol'].append(json_data['symbol'])
    data['Name'].append(json_data['longName'])
    data['Industry'].append(json_data['industry'])
    data['Price'].append(json_data['currentPrice'])

    # Could be that some indicators are not available; use NaN if this is the case
    
    if 'forwardEps' in json_data:
        data['EPS (fwd)'].append(json_data['forwardEps'])
    else:
        data['EPS (fwd)'].append(np.nan)
        
    if 'forwardPE' in json_data:
        data['P/E (fwd)'].append(json_data['forwardPE'])
    else:
        data['P/E (fwd)'].append(np.nan)
        
    if 'pegRatio' in json_data:
        data['PEG'].append(json_data['pegRatio'])
    else:
        data['PEG'].append(np.nan)

    if ('freeCashflow' in json_data) and ('marketCap' in json_data):
        fcfy = (json_data['freeCashflow']/json_data['marketCap']) * 100
        data['FCFY'].append(round(fcfy, 2))
    else:
        data['FCFY'].append(np.nan)

    if 'priceToBook' in json_data:
        data['PB'].append(json_data['priceToBook'])
    else:
        data['PB'].append(np.nan)

    if 'returnOnEquity' in json_data:
        data['ROE'].append(json_data['returnOnEquity'])
    else:
        data['ROE'].append(np.nan)
        
    if 'priceToSalesTrailing12Months' in json_data:
        data['P/S (trail)'].append(json_data['priceToSalesTrailing12Months'])
    else:
        data['P/S (trail)'].append(np.nan)

    data['DPR'].append(json_data['payoutRatio'] * 100)

    if 'dividendYield' in json_data:
        data['DY'].append(json_data['dividendYield'])
    else:
        data['DY'].append(0.0)

    if 'beta' in json_data:
        data['Beta'].append(json_data['beta'])
    else:
        data['Beta'].append(np.nan)

    if 'currentRatio' in json_data:
        data['CR'].append(json_data['currentRatio'])
    else:
        data['CR'].append(np.nan)

    if 'fiftyTwoWeekLow' in json_data:
        data['52w Low'].append(json_data['fiftyTwoWeekLow'])
    else:
        data['52w Low'].append(np.nan)
        
    if 'fiftyTwoWeekHigh' in json_data:    
        data['52w High'].append(json_data['fiftyTwoWeekHigh'])
    else:
        data['52w High'].append(np.nan)
Notes:

No additional computations are required except for Cash Flow Yield
Numpy NaN is inserted for any missing indicator; later, we will remove these records from the analysis
Loads stock data from json files
for symbol in SYMBOLS:
    # Specify the full path to load JSON data
    file_name = f'{DATA_PATH}/{symbol}.json'    
    try:
        # Open the file in read mode
        with open(file_name, 'r') as file:
            # Use json.load() to parse the JSON data from the file
            load_data(json.load(file))
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
Loops through the SYMBOLS declared in the Configuration section and calls the load_data method to populate the data dictionary

Create a Data Frame
Any stock with NaN value for an indicator is moved to a separate Data Frame. We’ll also add a new column to allow for a subsequent visualization via styles to show which stocks are near their 52-week low and which are near their 52-week high. A score of 90%, for example, indicates that the present price is very near its 52-week high.

# Create a DF using the dictionary
df = pd.DataFrame(data)

# Save any stocks with NaN values
df_exceptions = df[df.isna().any(axis=1)]

# Remove any stocks with NaN values
df=df.dropna()

# Reset index after dropping rows with NaN values
df.reset_index(drop=True, inplace=True)

# Add 52 week price range
df['52w Range'] = ((df['Price'] - df['52w Low'])/(df['52w High'] - df['52w Low']))*100

df_exceptions
Here is a partial output after creating a Data Frame.


Result of loading data from JSON files
As shown below, the two stocks with NaN values are moved to a different exception Data Frame.


Exceptions — indicators with NaN values
Adds styles
A utility method to add styles to the Data Frame created earlier

def make_pretty(styler):
    # Column formatting
    styler.format({'EPS (fwd)': '${:.2f}', 'P/E (fwd)': '{:.2f}', 'PEG': '{:.2f}',
                   'FCFY': '{:.2f}%', 'PB' : '{:.2f}', 'ROE' : '{:.2f}', 'P/S (trail)': '{:.2f}',
                   'DPR': '{:.2f}%', 'DY': '{:.2f}%', 'CR' : '{:.2f}', 'Beta': '{:.2f}', '52w Low': '${:.2f}',
                   'Price': '${:.2f}', '52w High': '${:.2f}', '52w Range': '{:.2f}%'
                  })
    # Set the bar visualization
    styler.bar(subset = ['52w Range'], align = "mid", color = ["salmon", "cornflowerblue"])

    # Grid
    styler.set_properties(**{'border': '0.1px solid black'})

    # Set background gradients
    styler.background_gradient(subset=['EPS (fwd)'], cmap='Greens')
    styler.background_gradient(subset=['P/E (fwd)'], cmap='Greens')
    styler.background_gradient(subset=['PEG'], cmap='Greens')
    styler.background_gradient(subset=['FCFY'], cmap='Greens')
    styler.background_gradient(subset=['PB'], cmap='Greens')
    styler.background_gradient(subset=['ROE'], cmap='Greens')
    styler.background_gradient(subset=['P/S (trail)'], cmap='Greens')
    styler.background_gradient(subset=['DPR'], cmap='Greens')
    styler.background_gradient(subset=['DY'], cmap='Greens')
    styler.background_gradient(subset=['CR'], cmap='Greens')

    # No index
    styler.hide(axis='index')

    # Tooltips
    styler.set_tooltips(
        ttips, css_class='tt-add',
        props=[
            ('visibility', 'hidden'),
            ('position', 'absolute'),
            ('background-color', 'salmon'),
            ('color', 'black'),
            ('z-index', 1),
            ('padding', '3px 3px'),
            ('margin', '2px')
        ]
    )
    # Left text alignment for some columns
    styler.set_properties(subset=['Symbol', 'Name', 'Industry'], **{'text-align': 'left'})
    return styler
Adds Tool Tips
A utility method to add tool tips to the Data Frame created earlier

def populate_tt(df, tt_data, col_name):
    stats = df[col_name].describe()
    
    per25 = round(stats.loc['25%'], 2)
    per50 = round(stats.loc['50%'], 2)
    per75 = round(stats.loc['75%'], 2)

    # Get position based on the column name
    pos = df.columns.to_list().index(col_name)
    
    for index, row in df.iterrows():
        pe = row[col_name]
        if pe == stats.loc['min']:
            tt_data[index][pos] = 'Lowest'
        elif pe == stats.loc['max']:
            tt_data[index][pos] = 'Hightest'
        elif pe <= per25:
            tt_data[index][pos] = '25% of companies under {}'.format(per25)
        elif pe <= per50:
            tt_data[index][pos] = '50% of companies under {}'.format(per50)
        elif pe <= per75:
            tt_data[index][pos] = '75% of companies under {}'.format(per75)
        else:
            tt_data[index][pos] = '25% of companies over {}'.format(per75)    
Apply styles and tool tips
# Initialize tool tip data - each column is set to '' for each row
tt_data = [['' for x in range(len(df.columns))] for y in range(len(df))]

# Gather tool tip data for indicators
populate_tt(df, tt_data, 'EPS (fwd)')
populate_tt(df, tt_data, 'P/E (fwd)')
populate_tt(df, tt_data, 'PEG')
populate_tt(df, tt_data, 'FCFY')
populate_tt(df, tt_data, 'PB')
populate_tt(df, tt_data, 'ROE')
populate_tt(df, tt_data, 'P/S (trail)')
populate_tt(df, tt_data, 'DPR')
populate_tt(df, tt_data, 'DY')
populate_tt(df, tt_data, 'CR')

# Create a tool tip DF
ttips = pd.DataFrame(data=tt_data, columns=df.columns, index=df.index)

# Add table caption and styles to DF
df.style.pipe(make_pretty).set_caption('Fundamental Indicators').set_table_styles(
    [{'selector': 'th.col_heading', 'props': 'text-align: center'},
     {'selector': 'caption', 'props': [('text-align', 'center'),
                                       ('font-size', '11pt'), ('font-weight', 'bold')]}])
Here is the sample output after applying the styles and tool tips:


Results after applying the styles and tool tips
Conclusion
This article describes an alternative approach for visualizing fundamental indicators using Pandas’ Data Frame.

It is critical to choose a group of related equities for the purpose of analysis. A high or low PE, for example, is only relevant within a group of similar equities. Also, data files must be kept up-to-date because Jupyter notebook relies on them.

I hope you found the information interesting and value your feedback.