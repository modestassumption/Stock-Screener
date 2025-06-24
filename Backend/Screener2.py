#!/usr/bin/env python
# coding: utf-8

# In[3]:


import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
import time

today = date.today().isoformat()
pd.set_option('display.max_rows', 20)
ticker_df = pd.read_csv("Tickers_NSE200")
ticker_original = ticker_df
ticker_df = ticker_df.drop(ticker_df.columns[0], axis=1)
ticker_df['Ticker'] = ticker_df['Ticker'].astype(str) + '.NS' 
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

def SMA (ticker, day = None):
    data = historical_data[str(ticker)]
    if day is None:
        average = (sum(data['Close']))/num_rows

    else:
        average = (sum(data['Close'][:day]))/(day)
    return average

def EMA (ticker, span = 12):
    data = historical_data[str(ticker)]
    ema = data['Close'].ewm(span = span, adjust = False).mean()
    return ema.iloc[-1] 

def MACD(ticker, span1 = 12, span2 = 26):
    EMA_12 = EMA(ticker, span1)
    EMA_26 = EMA(ticker, span2)
    return (EMA_12 - EMA_26)

def sig_line(ticker, customnum=9):
    signal_line = EMA(ticker, int(customnum))
    return signal_line

def Rel_str(ticker,period=14):
    data = historical_data[str(ticker)].copy() 
    gain_loss = []
    days = len(data)
    for i in range(days):
        gain_loss.append(data['Close'].iloc[i] - data['Close'].iloc[i-1] if i > 0 else 0)
    data['Gain/Loss'] = gain_loss
    gain_data=[]
    loss_data=[]
    RSI=[None]*days
    for i in range(days):
        gainloss = data['Gain/Loss'].iloc[i]
        gain_data.append(max(0,gainloss))
        loss_data.append(abs(min(0,gainloss)))
    average_gain = sum(gain_data)/len(gain_data)
    average_loss = sum(loss_data)/len(loss_data)
    RSI[int(period)]=100 - (100/(1 + average_gain/average_loss))
    for i in range(period + 1, days):
        average_gain = (average_gain*(period-1) + gain_data[i])/period  #+(gain_data[i]/data['Close'].iloc[i-1])*100)
        average_loss = (average_loss*(period-1) + loss_data[i])/period  #+(loss_data[i]/data['Close'].iloc[i-1])*100) as per doc
        RSI[i] = (100-(100/(1+average_gain/average_loss)))

    return RSI
        
        

            


    
        

