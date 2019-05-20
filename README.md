# **Jim Crammer Call Data**

This code starts with a raw dataset of Jim Crammer's stock calls gotten from the Mad Money website and does some manipulation to get more data 
related to the dataset. The workflow for this project was:

1. Get the raw data
    - https://madmoney.thestreet.com/screener/index.cfm?showview=stocks&showrows=25000, this was just copied and pasted into excel
    - consist of Company Name (ticker), Date of the call, Segement the call was made on, the price of the company at the time of the call  
    - rawdata.xlsx

2. Clean the data
    - change the date format --> it was initially missing the year in the date column
    - cleandata.xlsx
    - date.txt

3. Read into pandas and do preprocessing 
    - number of uniques companies 
    - the company with the most and least calls 
    - the segement with the most calls 

4. Get the company EOD data and Sector/Industry data
    - each company's historical EOD 
    - clean the date in the EOD data (epoch to '%#m/%#d/%Y')
    - each company's Sector and Industry  
    - stocks_data folder contains stock data for the companies 
    - used previous built webscrapers 'yahooEODscraper' & yahoo_stats_scraper

5. Get the other data and append to existing dataframe 
    - drop the rows where there is no historical data exists 
    - get date, price, and price change information for:
      - next day after call
      - one week after the call
      - one month after the call 
      - three months after the call 
    - get the next day volume change 
    - get the annualized standard deviation
    - Backtest.csv
