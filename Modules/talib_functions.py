import numpy, pandas
import talib
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import signature as sig
from datetime import datetime, timedelta, timezone
import pytz
import csv, os
import pandas as pd
import helpfunctions as hp
import ex_functions as ef


import matplotlib.pyplot as plt

# init
BASE_URL = 'https://api.binance.com' # production base url
client = Client(sig.KEY, sig.SECRET)


# set working directory
os.chdir('../')
root = os.getcwd()
# ana = '\Analysis'

# init dataframe
# real = talib.MFI(high, low, close, volume, timeperiod=14)

amsterdam_time = pytz.timezone("Europe/Amsterdam")
standard_time = pytz.timezone("Africa/Abidjan")

def EpochToDate(epoch):
	# ts = datetime.datetime.fromtimestamp(epoch/1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
	ts = datetime.fromtimestamp(epoch/1000, amsterdam_time)
	return ts


def GetRSI(coin, base):
	symbol = coin.upper() + base.upper()
	candles = client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_1MINUTE)

	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})
	# extract rsi from dataframe
	df_rsi  = talib.RSI(df.loc[:,'close'], timeperiod = 14)

	# get last value of series
	return float(df_rsi.values[-1])


def GetRSI_1H(coin, base, startDate, endDate):
	symbol = coin.upper() + base.upper()
	scale = '1H'

	candles = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, startDate, endDate)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})
	df['time'] = df['time'].apply(EpochToDate)
	df['asset'] = coin
	df['base'] = base
	df['scale'] = scale
	# extract rsi from dataframe
	df['rsi']  = talib.RSI(df.loc[:,'close'], timeperiod = 14)

	# get last value of series
	return df[['asset','base','scale','time','rsi']]


def GetOHLCV_1M(coin, base, startDate, endDate):
	symbol = coin.upper() + base.upper()
	scale = '1M'
	
	candles = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, startDate, endDate)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})
	df['time'] = df['time'].apply(EpochToDate)
	df['asset'] = coin
	df['base'] = base
	df['scale'] = scale
	return df[['asset','base','scale','time','open','high','low', 'close', 'volume']]


def GetOHLCV_1H(coin, base, startDate, endDate):
	symbol = coin.upper() + base.upper()
	scale = '1H'
	
	candles = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, startDate, endDate)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})
	df['time'] = df['time'].apply(EpochToDate)
	df['asset'] = coin
	df['base'] = base
	df['scale'] = scale
	return df[['asset','base','scale','time','open','high','low', 'close', 'volume']]


def RSI_15M(coin, base):
	symbol = coin.upper() + base.upper()
	candles = client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_15MINUTE)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})

	# extract rsi from dataframe
	df_rsi  = talib.RSI(df.loc[:,'close'], timeperiod = 14)

	# get last value of series
	result = hp.round_decimals_down(df_rsi.iloc[-1], 2)

	return result


def MFI_15M(coin, base):
	symbol = coin.upper() + base.upper()
	candles = client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_15MINUTE)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})

	# extract mfi from dataframe
	df_mfi = talib.MFI(df.high, df.low, df.close, df.volume, timeperiod=14)

	# get last value of series rounded down
	result = hp.round_decimals_down(df_mfi.iloc[-1], 2)

	return result


def MFI_01M(coin, base):
	symbol = coin.upper() + base.upper()
	candles = client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_1MINUTE)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})

	# extract mfi from dataframe
	df_mfi = talib.MFI(df.high, df.low, df.close, df.volume, timeperiod=14)

	# get last value of series rounded down
	result = hp.round_decimals_down(df_mfi.iloc[-1], 2)

	return result

def LastMFI(coin, base, n,m):
	symbol = coin.upper() + base.upper()
	candles = client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_1MINUTE)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})
	df_mfi = talib.MFI(df.high, df.low, df.close, df.volume, timeperiod=14)
	ls = df_mfi.tail(n).values.tolist()
	belowM = [1 for x in ls if x < m ] 
	return sum(belowM)




def VOL_15M(coin, base):
	symbol = coin.upper() + base.upper()
	candles = client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_15MINUTE)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={5:'volume'})

	# extract mfi from dataframe
	volume = float(df.volume.values[-1])

	# get last value of series rounded down
	# result = hp.round_decimals_down(df_mfi.iloc[-1], 2)

	return volume



def BBANDS_01M(coin, base):
	symbol = coin.upper() + base.upper()
	candles = client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_1MINUTE)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})
	close = df.close
	upper, middle, lower = talib.BBANDS(close, timeperiod = 20 , matype = 0)

	lowerBand = lower.values[-1]
	currentPrice = ef.PriceAction(coin, base)
	if currentPrice > 0:
		indicator = (((currentPrice - lowerBand) / lowerBand)*100)
		return (indicator, currentPrice, lowerBand)
	else:
		return 100



def BBANDS_15M(coin, base):
	symbol = coin.upper() + base.upper()
	candles = client.get_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_15MINUTE)
	df = pandas.DataFrame(candles)
	df = df.rename(columns={0: 'time', 1: 'open', 2:'high', 3:'low', 4:'close', 5:'volume'})
	close = df.close
	upper, middle, lower = talib.BBANDS(close, timeperiod = 20 , matype = 0)

	return (upper.values[-1], middle.values[-1], lower.values[-1])


def Correlation(coin1, coin2, base):
	symbol1 = coin1 + base
	symbol2 = coin2 + base
	
	candles = client.get_klines(symbol = symbol1, interval = Client.KLINE_INTERVAL_15MINUTE)
	df_coin1 = pandas.DataFrame(candles)
	df_coin1 = df_coin1.rename(columns={0: 'time1', 1: 'open1', 2:'high1', 3:'low1', 4:'close1', 5:'volume1'})
	df_close1 = df_coin1.close1
	df1 = df_close1.to_frame()
	df1['close1'] = pd.to_numeric(df1['close1'], downcast="float")


	candles = client.get_klines(symbol = symbol2, interval = Client.KLINE_INTERVAL_15MINUTE)
	df_coin2 = pandas.DataFrame(candles)
	df_coin2 = df_coin2.rename(columns={0: 'time2', 1: 'open2', 2:'high2', 3:'low2', 4:'close2', 5:'volume2'})
	df_close2 = df_coin2.close2
	df2 = df_close2.to_frame()
	df2['close2'] = pd.to_numeric(df2['close2'], downcast="float")

	# df = df_close1.rename(columns={0: 'coin1'})
	# df = df_close1.to_frame()
	df1['close2'] = df2['close2']


	# return df1

	return df1.corr(method='pearson')



# print(Correlation('BTC', 'USDC', 'USDT'))



