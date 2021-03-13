'''
From python.plainenglish.io Sofien Kaabar Oct 20, 2020
https://python.plainenglish.io/combining-candlestick-patterns-with-technical-indicators-a-python-study-77492ea8673
From www.oreilly.com Yves Hilpisch Jan 18, 2017
https://www.oreilly.com/content/algorithmic-trading-in-less-than-100-lines-of-python-code/
'''
import pandas as pd
import numpy as np
import json

# Defining the barriers
lower = 45
upper = 55

def doji_strategy(Candles, trigger):
    '''
    From python.plainenglish.io Sofien Kaabar Oct 20, 2020
    The variable [Candles] refers to the OHLC Historical Data array.
    The variable indicator refers to RSI's location.
    The variable buy refers to where the long order is triggered.
    The variable sell refers to where the short order is triggered.
    changed to trigger = 'buy' or 'sell'
    Candles: 0 = Open, 1 = High, 2 = Low, 3 = Close, 4 = trigger, 5 = indicator
    '''
    for i in range(len(Candles)):
            
        if Candles[i, 5] < lower and Candles[i, 3] == Candles[i, 0]:
            Candles[i, trigger] = 'buy'
                
        if Candles[i, 5] > upper and Candles[i, 3] == Candles[i, 0]:
            Candles[i, trigger] = 'sell'


def harami_strategy(Candles, trigger):
    '''
    From python.plainenglish.io Sofien Kaabar Oct 20, 2020
    The variable [Candles] refers to the OHLC Historical Data array.
    The variable indicator refers to RSI's location.
    The variable buy refers to where the long order is triggered.
    The variable sell refers to where the short order is triggered.
    changed to trigger = 'buy' or 'sell'
    Candles: 0 = Open, 1 = High, 2 = Low, 3 = Close, 4 = trigger, 5 = indicator 
    '''
    for i in range(len(Candles)):
            
        if Candles[i, 5] < lower and \
            Candles[i - 1, 3] < Candles[i - 1, 0] and \
            Candles[i, 3] > Candles[i, 0] and \
            Candles[i - 1, 3] < Candles[i, 2] and \
            Candles[i - 1, 0] > Candles[i, 1]:
            Candles[i, trigger] = 'buy'
                
        if Candles[i, 5] > upper and \
            Candles[i - 1, 3] > Candles[i - 1, 0] and \
            Candles[i, 3] < Candles[i, 0] and \
            Candles[i - 1, 3] > Candles[i, 1] and \
            Candles[i - 1, 0] < Candles[i, 2]:
            Candles[i, trigger] = 'sell'


def piercing_cloud_strategy(Candles, trigger):
    '''
    From python.plainenglish.io Sofien Kaabar Oct 20, 2020
    The variable [Candles] refers to the OHLC Historical Data array.
    The variable indicator refers to RSI's location.
    The variable buy refers to where the long order is triggered.
    The variable sell refers to where the short order is triggered.
    changed to trigger = 'buy' or 'sell'
    Candles: 0 = Open, 1 = High, 2 = Low, 3 = Close, 4 = trigger, 5 = indicator 
    '''

    for i in range(len(Candles)):
        
        if Candles[i, 5] < lower and \
            Candles[i - 1, 3] < Candles[i - 1, 0] and \
            Candles[i, 3] > Candles[i, 0] and \
            Candles[i, 0] < Candles[i - 1, 3] and \
            Candles[i, 3] > Candles[i - 1, 3] and \
            Candles[i, 3] < Candles[i - 1, 0]:
            Candles[i, trigger] = 'buy'
        
        if Candles[i, 5] > upper and \
            Candles[i - 1, 3] > Candles[i - 1, 0] and \
            Candles[i, 3] < Candles[i, 0] and \
            Candles[i, 0] > Candles[i - 1, 3] and \
            Candles[i, 3] < Candles[i - 1, 3] and \
            Candles[i, 3] > Candles[i - 1, 0]:
            Candles[i, trigger] = 'sell'


def mean_log_return(Candles, trigger):
    '''
    From www.oreilly.com Yves Hilpisch Jan 18, 2017
    [F]ormalize the momentum strategy by telling Python to take the mean log return 
    over the last 15, 30, 60, and 120 minute bars to derive the position in the 
    instrument. For example, the mean log return for the last 15 minute bars gives 
    the average value of the last 15 return observations. If this value is positive, 
    we go/stay long the traded instrument; if it is negative we go/stay short. 
    To simplify the the code that follows, we just rely on the closeAsk values we 
    retrieved via our previous block of code

    Candles: 0 = Open, 1 = High, 2 = Low, 3 = Close, 4 = trigger, 5 = indicator 
    '''
    for i in range(len(Candles)):
        Candles[i, 5] = np.log(Candles[i, 3] / Candles[i, 3].shift(1))
    for i in range(len(Candles)):
        if  (Candles[i, 5].shift(1) >= 0 and Candles[i, 5] >= 0) or \
            (Candles[i, 5].shift(1) < 0 and Candles[i, 5] < 0):
            Candles[i + 1, 4] = 'wait'
        elif Candles[i, 5].shift(1) >= 0 and Candles[i, 5] < 0:
            Candles[i + 1, 4] = 'buy'
        else:
            Candles[i + 1, 4] = 'sell'
    
    cols = []
    for momentum in [15, 30, 60, 120]:
        col = 'position_%s' % momentum
        Candles[col] = np.sign(Candles[5].rolling(momentum).mean())
        cols.append(col)

    # %matplotlib inline
    import seaborn as sns; sns.set()

    strats = [5] 

    for col in cols:
        strat = 'strategy_%s' % col.split('_')[1]
        Candles[strat] = Candles[col].shift(1) * Candles[5]
        strats.append(strat)

    Candles[strats].dropna().cumsum().apply(np.exp).plot()

def prepare_Candle_data(filename):
    '''
    Accept JSON file from Oanda princing history.
    Convert into format for analysis/back-testing.
    '''
    try:
        df = pd.read_json(filename)
    except:
        print(Exception)
        
    df = df.set_index('time')

    analysis_set = []
    for i in df.iterrows():
        mid = i[1]['mid']
        open, high, low, close = mid['o'], mid['h'], mid['l'], mid['c']
        trigger = 'wait'
        indicator = 0
        analysis_set.append((i[0],open,high, low, close, trigger, indicator))
    return analysis_set

filename = "/tmp/EUR_USD.M15.json"
prepare_Candle_data(filename)