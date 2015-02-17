# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 19:44:26 2015

@author: krisan
"""

#the following script aim to investigate overnight trading

#https://code.google.com/p/trading-with-python/source/browse/trunk/lib/functions.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import neighbors
import tradingWithPython.lib.yahooFinance as yf
import tradingWithPython.lib as lb1
#https://www.tradingview.com/v/EVXQPaR9/
# we first need ot get data.

ohlc=yf.getHistoricData('SPY')

ohlc['cc']=(ohlc['close']/ohlc['open'])-1
ohlc['co']=(ohlc['open']/ohlc['close'].shift(1))-1

#ret1=np.cumsum(ohlc['cc']).plot()
##ret2=np.cumsum(ohlc['co']).plot()

plt.plot(ohlc['co'].index,np.cumsum((ohlc['cc'])),'r')
plt.plot(ohlc['co'].index,np.cumsum(ohlc['co']),'b')

train=pd.DataFrame(columns=ohlc.columns)
test=pd.DataFrame(columns=ohlc.columns)

train=train.append(ohlc.iloc[0:1000])
test=test.append(ohlc.iloc[1000:])

# looking at the plots they clearly show there is an close to open effect.
# we want to try an optimise this though
# So lets add MA_200, Ma_5 and RSI2

ohlc['MA200']=pd.rolling_mean(ohlc['close'],200)
ohlc['MA5']=pd.rolling_mean(ohlc['close'],5)

# RSI2  formula
# we calculate this on the close price.
n=2
delta=ohlc['close'].diff()
dUp, dDown = delta.copy(), delta.copy()
dUp[dUp < 0] = 0
dDown[dDown > 0] = 0

RolUp = pd.rolling_mean(dUp, n)
RolDown = pd.rolling_mean(dDown, n).abs()
RS = RolUp / RolDown
RSI=100-100/(1.0+RS)

ohlc['RSI']=RSI

#we now have our signals. We should create a trigger colum

ohlc['trigger']=np.where((ohlc['close']>ohlc['MA200']) & (ohlc['close']<ohlc['MA5']) & (ohlc['RSI']<11.0),1,0) 

ohlc['trigger']=np.where((ohlc['close']<ohlc['MA200'])&(ohlc['close']>ohlc['MA5'])& (ohlc['RSI']>89.0),-1,ohlc['trigger'])

ohlc1=ohlc.dropna()

# so we have the ohlc1 dataframe from which we need to carry out the data analysis
trade=0
entry_price=[]
date_enter=[]
date_exit=[]
exit_price=[]
direction=[]

for x in ohlc1.index:
    if ohlc1['trigger'].loc[x]==1 and trade==0:
        trade=1
        entry_price.append(ohlc1['close'].loc[x])
                
        date_enter.append(x)
        direction.append(ohlc1['trigger'].loc[x])
    elif trade==1 and (ohlc1['close'].loc[x]>ohlc1['MA5'].loc[x]):
        exit_price.append(ohlc1['close'].loc[x])
        date_exit.append(x)
        trade=0
    elif trade==0 and ohlc1['trigger'].loc[x]==-1:
        entry_price.append(ohlc1['close'].loc[x])
        date_enter.append(x)
        trade=-1
        direction.append(ohlc1['trigger'].loc[x])        
    elif trade==-1 and (ohlc1['close'].loc[x]<ohlc1['MA5'].loc[x]):
        exit_price.append(ohlc1['close'].loc[x])
        date_exit.append(x)
        trade=0
        
if trade !=0:
    exit_price.append(ohlc1['close'][-1])
    date_exit.append(ohlc1.index[-1])
    direction.append(ohlc1['trigger'].loc[x])    
results=pd.DataFrame(columns=['Entry_Date','Exit_Date','Entry_Price','Exit_Price','Direction'])
        
results['Entry_Date']=date_enter
results['Exit_Date']=date_exit
results['Entry_Price']=entry_price
results['Exit_Price']=exit_price
results['Direction']=direction

PNL=np.where(results['Direction']==1,results['Exit_Price']/results['Entry_Price']-1,results['Entry_Price']/results['Exit_Price']-1)        
        

plt.plot(results['Exit_Date'],np.cumsum(PNL))
