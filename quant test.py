# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 00:31:55 2018

@author: Elum franklin

This script shows how the prices of some stocks and commodities
are correlated. All data were obtained from yahoo finance, using the yahoo finance
API by pip install fix-yahoo-finance, and pip install pandas-datareader.
for analysis, the pandas library was used, and for visualization, the seaborn
library was used. codes were written with python 3.6, on a spyder notebook.
btc_crypto = bitcoin crypto currency
Nigeria_ETF = NSE
comex_gold = COMEX GOLD
brent_crude_oil= brent crude oil
"""

#import the necessary libraries
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data, wb
import fix_yahoo_finance as yf
yf.pdr_override()
import datetime
import seaborn as sns


#get the data for bitcoin USD from jan 1-1-2018 to june 29-1-2018
start = datetime.datetime(2018, 1,1 )
end = datetime.datetime(2018, 6, 29)
btc_crypto = data.get_data_yahoo('BTC-USD', start, end)
print ('\n**********************  DATA FOR BITCOIN ***************************')
print(btc_crypto)
#to display only the head
#print(btc_crypto.head())

#get the data for Nigeria ETF from jan 1-1-2018 to june 29-1-2018
start = datetime.datetime(2018, 1,1 )
end = datetime.datetime(2018, 6, 29)
Nigeria_ETF = data.get_data_yahoo('NGE', start, end)
print ('\n**********************  DATA FOR NIGERIA ETF ***************************')
print(Nigeria_ETF)
#to get the head
#print(Nigeria_ETF.head())


#get the data for comex gold from jan 1-1-2018 to june 29-1-2018
start = datetime.datetime(2018, 1,1 )
end = datetime.datetime(2018, 6, 29)
comex_gold=data.get_data_yahoo('GCZ18.CMX', start, end)
print ('\n**********************  DATA FOR COMEX GOLD ***************************')
print(comex_gold)
#to get the head
#print(comex_gold.head())

##get the data for crude from jan 1-1-2018 to june 29-1-2018
start = datetime.datetime(2018, 1,1 )
end = datetime.datetime(2018, 6, 29)
crude_oil=data.get_data_yahoo('CL=F', start, end)
print ('\n**********************  DATA FOR CRUDE OIL ***************************')
print(crude_oil)
#to get the head
#print(brent_crude_oil.head())

#to get the correlation matrix, the Adj Close column is used for comparison.
#i deleted the other columns so as to get the Adj Close column only

del btc_crypto['Open']
del btc_crypto['High']
del btc_crypto['Low']
del btc_crypto['Close']
del btc_crypto['Volume']

#now i am left with only the Adj close column. hence i can now rename btc_crypto to a variable of 
#my choice and calculate the daily percentage change in price for normalization

New_name= btc_crypto.pct_change(1)

#Instead of calling these columns all Adj Close, I am going to call them their actual commodity name 
#so i can compare easily

New_name.rename(columns={'Adj Close': 'btc_crypto'}, inplace=True)

#i now  have just one column for Adj Close for btc_crypto. i can now implement the same for all other
#commodities and get the daily changes in price for normalization

New_name['comex_gold'] = comex_gold['Adj Close'].pct_change(1)
New_name['crude_oil'] = crude_oil['Adj Close'].pct_change(1)
New_name['Nigeria_ETF']=Nigeria_ETF['Adj Close'].pct_change(1)
print ('\n********************** DAILY PERCENTAGE CHANGE ***************************')
print(New_name)


#print out the corellation matrix of all the commodities
print ('\n**********************  EXPLAINED CORRELATED MATRIX ***************************')
print(New_name.corr())

#visualization of the correlation matrix using a heatmap
print ('\n********************** HEATMAP VISUALIZATION ***************************')
sns.heatmap(New_name.corr(), annot=True)
