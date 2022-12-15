# Import necessary librairess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st

# Load in data from yahoo finnce
df = yf.Ticker('ES=F').history(period='1y')
dfnq = yf.Ticker('NQ=F').history(period='1y')
dfvix = yf.Ticker('^vix').history(period='6mo')

# Calculate returns and the Moving Averages
df['Return'] = df['Close'].pct_change()
df['MA20'] = df['Close'].rolling(20).mean()
df['MA50'] = df['Close'].rolling(50).mean()
df['MA13'] = df['Close'].rolling(13).mean()
df['MA200'] = df['Close'].rolling(200).mean()
df['Weekly Trend'] = df['Close'] > df['MA200']

dfnq['Return'] = dfnq['Close'].pct_change()
dfnq['MA20'] = dfnq['Close'].rolling(20).mean()
dfnq['MA50'] = dfnq['Close'].rolling(50).mean()
dfnq['MA13'] = dfnq['Close'].rolling(13).mean()
dfnq['MA200'] = dfnq['Close'].rolling(200).mean()

#Caclulate metrics for dashboard
Close = df['Close'].iat[-1]
index = df.index[-1]

vixclose = round(dfvix['Close'].iat[-1],2)
vixclose_change = round(dfvix['Close'] - dfvix['Close'].shift()).iat[-1]

MA13 = round(df['MA13'].iat[-1],2)
MA20 = round(df['MA20'].iat[-1],2)
MA50 = round(df['MA50'].iat[-1],2)
MA200 = round(df['MA200'].iat[-1],2)
Close_MA13 = round(Close - MA13)
Close_MA20 = round(Close - MA20)
Close_MA50 = round(Close - MA50)
Close_MA200 = round(Close - MA200)
Close_Change = (df['Close'] - df['Close'].shift()).iat[-1]

nqClose = dfnq['Close'].iat[-1]
nqMA13 = round(dfnq['MA13'].iat[-1],2)
nqMA20 = round(dfnq['MA20'].iat[-1],2)
nqMA50 = round(dfnq['MA50'].iat[-1],2)
nqMA200 = round(dfnq['MA200'].iat[-1],2)
nqClose_MA13 = round(nqClose - nqMA13)
nqClose_MA20 = round(nqClose - nqMA20)
nqClose_MA50 = round(nqClose - nqMA50)
nqClose_MA200 = round(nqClose - nqMA200)
nqClose_Change = (dfnq['Close'] - dfnq['Close'].shift()).iat[-1]

#Calculate Slope in the Moving Average for the Trend
df.loc[(df['MA200'] > df['MA200'].shift()), 'MA200 Slope'] = 'Up'
df.loc[(df['MA200'] < df['MA200'].shift()), 'MA200 Slope'] = 'Down'
MA200Slope = df['MA200 Slope'].iat[-1]

dfnq.loc[(dfnq['MA200'] > dfnq['MA200'].shift()), 'MA200 Slope'] = 'Up'
dfnq.loc[(dfnq['MA200'] < dfnq['MA200'].shift()), 'MA200 Slope'] = 'Down'
nqMA200Slope = dfnq['MA200 Slope'].iat[-1]

# ------------------------------This section uses Highs and lows to determine the trend

# Reset index so that there's numbers and not Datetime in the index
dfNewIndex = df.reset_index()
dfnqNewIndex = dfnq.reset_index()

# create a list of our conditions
conditions = [
    (dfNewIndex['Close'].loc[:63].max() > dfNewIndex['Close'].loc[64:127].max()) & (dfNewIndex['Close'].loc[64:127].max() > dfNewIndex['Close'].loc[128:191].max()) & (dfNewIndex['Close'].loc[128:191].max() > dfNewIndex['Close'].loc[192:253].max()) & (dfNewIndex['Close'].loc[:84].min() > dfNewIndex['Close'].loc[84:169].min()) & (dfNewIndex['Close'].loc[84:169].min() > dfNewIndex['Close'].loc[169:].min()),
    (dfNewIndex['Close'].loc[:63].max() < dfNewIndex['Close'].loc[64:127].max()) & (dfNewIndex['Close'].loc[64:127].max() < dfNewIndex['Close'].loc[128:191].max()) & (dfNewIndex['Close'].loc[128:191].max() < dfNewIndex['Close'].loc[192:253].max()) & (dfNewIndex['Close'].loc[:84].min() < dfNewIndex['Close'].loc[84:169].min()) & (dfNewIndex['Close'].loc[84:169].min() < dfNewIndex['Close'].loc[169:].min())
    ]

conditionsnq = [
    (dfnqNewIndex['Close'].loc[:63].max() > dfnqNewIndex['Close'].loc[64:127].max()) & (dfnqNewIndex['Close'].loc[64:127].max() > dfnqNewIndex['Close'].loc[128:191].max()) & (dfnqNewIndex['Close'].loc[128:191].max() > dfnqNewIndex['Close'].loc[192:253].max()) & (dfnqNewIndex['Close'].loc[:84].min() > dfnqNewIndex['Close'].loc[84:169].min()) & (dfnqNewIndex['Close'].loc[84:169].min() > dfnqNewIndex['Close'].loc[169:].min()),
    (dfnqNewIndex['Close'].loc[:63].max() < dfnqNewIndex['Close'].loc[64:127].max()) & (dfnqNewIndex['Close'].loc[64:127].max() < dfnqNewIndex['Close'].loc[128:191].max()) & (dfnqNewIndex['Close'].loc[128:191].max() < dfnqNewIndex['Close'].loc[192:253].max()) & (dfnqNewIndex['Close'].loc[:84].min() < dfnqNewIndex['Close'].loc[84:169].min()) & (dfnqNewIndex['Close'].loc[84:169].min() < dfnqNewIndex['Close'].loc[169:].min()),
    ]

# create a list of the values we want to assign for each condition
values = ['Down', 'Up']
valuesnq = ['Down', 'Up']

# create a new column and use np.select to assign values to it using our lists as arguments
dfNewIndex['Trend'] = np.select(conditions, values)
dfnqNewIndex['Trend'] = np.select(conditionsnq, valuesnq)

# Get the most recent value from Trend column
EsWeeklyTrend = dfNewIndex['Trend'].iat[-1]
NqWeeklyTrend = dfnqNewIndex['Trend'].iat[-1]





# Calculate ATR
high_low = df['High'] - df['Low']
high_close = np.abs(df['High'] - df['Close'].shift())
low_close = np.abs(df['Low'] - df['Close'].shift())
ranges = pd.concat([high_low, high_close, low_close], axis=1)
true_range = np.max(ranges, axis=1)
atr = round((true_range.rolling(10).sum()/10).iat[-1],2)
# Calculate NQ ATR
nqhigh_low = dfnq['High'] - dfnq['Low']
nqhigh_close = np.abs(dfnq['High'] - dfnq['Close'].shift())
nqlow_close = np.abs(dfnq['Low'] - dfnq['Close'].shift())
nqranges = pd.concat([nqhigh_low, nqhigh_close, nqlow_close], axis=1)
nqtrue_range = np.max(nqranges, axis=1)
nqatr = round((nqtrue_range.rolling(10).sum()/10).iat[-1],2)

# Make charts

fig = plt.figure()
plt.title('ES Close vs Various MA')
df['Close'].plot()
df['MA13'].plot()
df['MA20'].plot()
df['MA50'].plot()
df['MA200'].plot()
plt.xticks(rotation=360)
plt.xlabel(None)
plt.legend()

fig1 = plt.figure()
plt.title('NQ Close vs Various MA')
dfnq['Close'].plot()
dfnq['MA13'].plot()
dfnq['MA20'].plot()
dfnq['MA50'].plot()
dfnq['MA200'].plot()
plt.xticks(rotation=360)
plt.xlabel(None)
plt.legend()

fig2 = plt.figure()
dfvix['Close'].plot(figsize=(3,1), title='VIX', fontsize='5')
plt.xticks(rotation=360)
plt.xlabel(None)

# ---------------------------Streamlit content below:

# Set page width to wide
st.set_page_config(layout="wide")

st.subheader("Dashboard - Trend, Volatility, Strategy & Leading Indicators")
st.text(index)

col1, col2, col3 = st.columns(3)
col1.subheader("ES Metrics")
col1.metric('Weekly Trend:', (EsWeeklyTrend))
col1.metric("Weekly Trend (MA):", (MA200Slope))
col1.metric("ES Close", (Close), (Close_Change))
col1.metric("13 Day MA", (MA13), (Close_MA13))
col1.metric("20 Day MA", (MA20),(Close_MA20))
col1.metric("50 Day MA", (MA50), (Close_MA50))
col1.metric("200 Day MA", (MA200), (Close_MA200))
col1.pyplot(fig)

col2.subheader('NQ Metrics')
col2.metric('Weekly Trend:', (NqWeeklyTrend))
col2.metric("Weekly Trend (MA):", (nqMA200Slope))
col2.metric("NQ Close", (nqClose), (nqClose_Change))
col2.metric("13 Day MA", (nqMA13), (nqClose_MA13))
col2.metric("20 Day MA", (nqMA20), (nqClose_MA20))
col2.metric("50 Day MA", (nqMA50), (nqClose_MA50))
col2.metric("200 Day MA", (nqMA200), (nqClose_MA200))
col2.pyplot(fig1)

col3.subheader('Volatility Metrics')
col3.metric("VIX", (vixclose), (vixclose_change))
col3.metric("ES ATR", (atr))
col3.metric("NQ ATR", (nqatr))
col3.pyplot(fig2)
