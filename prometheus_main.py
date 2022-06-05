# prometheus_main.py

# general modules
import requests
import sys, os
import sqlite3
from datetime import datetime, timedelta
import time


os.chdir('Modules')
path = os.getcwd()


sys.path.insert(0, path)
import ex_functions as ef
import helpfunctions as hp
import talib_functions as ta
import trade_functions as tf


url = 'https://api.binance.com' #binance server
programVersion = '0.1 gamma'
trade_interval = 60
timeout = 5
programDuration = 24
program_end = datetime.now() + timedelta(hours = programDuration)
coin = 'XMR'
base = 'BUSD'
symbol = coin + base
takeProfit = 0.3
controlFlowLong = 0
sellPrice = 0

# short trading
bbUpperBoundTreshold = 60 #price has to be above treshold factor times upperbound for a sell signal in a shor trade
mfiShortTreshold = 60 # mfi has to be higher then treshold for a mfi sell signal in a short trade

# long trading
bbLowerBoundTreshold = 20
mfiLongTreshold = 20

tradePoolPercentage = 80 #trade with x% of total balance 



# start main program
programStart = hp.TimeStamp()
print('%s: Starting Prometheus version %s' %(programStart, programVersion))

tf.UpdateBalance(coin, base)

while datetime.now() < program_end:
	
	try:
		request = requests.get(url, timeout=timeout)


		##############################
		# timestamp = hp.TimeStamp()
		# currentPrice = hp.round_decimals_down(ef.PriceAction2(symbol)[3],0)
		# print('%s: currentPrice: %f' %(timestamp,currentPrice))
		# mfi15 = ta.MFI_15M(coin, base)
		# print('mfi: %f | upper treshold %f | lower treshold %f' %(mfi15, mfiShortTreshold, mfiLongTreshold))
		# bb15 = ta.BBANDS_15M(coin, base)
		# bbpercentage = ta.PercOfBBrange(currentPrice, bb15)
		# print('bbpercentage: %f | upper treshold %f | lower treshold %f' %(bbpercentage, bbUpperBoundTreshold, bbLowerBoundTreshold))
		# print('\n')


		##############################

		# tradeQuantity = ef.CheckBalance(coin) * (tradePoolPercentage/100)
		tf.TradeFunctionShort15M(coin, base, takeProfit, bbUpperBoundTreshold, mfiShortTreshold)
		tf.TradeFunctionLong15M(coin, base, takeProfit, bbLowerBoundTreshold, mfiLongTreshold)
		

	except (requests.ConnectionError, requests.Timeout) as exception:
		print("Internet connection lost..")

	time.sleep(trade_interval)
