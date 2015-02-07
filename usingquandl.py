# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 12:01:14 2015

@author: krisan
"""

#USING QUANDL

import pandas as pd
import urllib
import json
%matplotlib inline

def read_quandl(url):
    d = json.loads(urllib.urlopen(url).read())
    df = pd.DataFrame(d['data'], columns=d['column_names']).set_index('Date').sort()
    return df
    
url = "https://www.quandl.com/api/v1/datasets/BCHAIN/TOTBC.json"
url="https://www.quandl.com/api/v1/datasets/LIFFE/ZH2015.json"
url1='https://www.quandl.com/api/v1/datasets/OFDP/FUTURE_VX1.json?trim_start=2008-01-01'
url2='https://www.quandl.com/api/v1/datasets/YAHOO/INDEX_GSPC.json?trim_start=2008-01-01'
#number = read_quandl(url)

VX1=read_quandl(url1)
SPX=read_quandl(url2)

v1=SPX.join(VX1,how='outer',rsuffix='_1')
