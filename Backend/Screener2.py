#!/usr/bin/env python
# coding: utf-8

# In[3]:


import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
import time


# In[4]:


today = date.today().isoformat()
pd.set_option('display.max_rows', 20)


# In[5]:


ticker_df = pd.read_csv("Tickers_NSE200")
ticker_original = ticker_df


# In[6]:


ticker_df = ticker_df.drop(ticker_df.columns[0], axis=1)


# In[7]:


ticker_df['Ticker'] = ticker_df['Ticker'].astype(str) + '.NS' 


# In[8]:


historical_data={}
print('Wait for a minute or two. Processing request.')

for tick in ticker_df['Ticker'][:1]:
        try:
            ticker = yf.Ticker(tick)
            data = ticker.history(start = '1999-01-01', end = today)
            df = pd.DataFrame(data)
            df.to_csv(f'{tick}_data.csv')
            historical_data[tick] = df
            num_rows = data.shape[0]

        except Exception as e:
            print(f"Error for ticker '{tick}': {e}")
    
print('Completed.')


# In[17]:


def SMA (ticker, day = None):
    data = historical_data[str(ticker)]
    if day is None:
        average = (sum(data['Close']))/num_rows

    else:
        average = (sum(data['Close'][:day]))/(day)
    return average


# In[18]:


def EMA (ticker, span = 12):
    data = historical_data[str(ticker)]
    ema = data['Close'].ewm(span = span, adjust = False).mean()
    return ema.iloc[-1] 


# In[19]:


def MACD(ticker, span1 = 12, span2 = 26):
    EMA_12 = EMA(ticker, span1)
    EMA_26 = EMA(ticker, span2)
    return (EMA_12 - EMA_26)

def sig_line(ticker):
    signal_line = EMA(ticker, 9)
    return signal_line

