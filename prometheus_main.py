# prometheus_main.py

# general modules
import requests
import sys, os
import sqlite3
from datetime import datetime, timedelta
import time



'''
BACKLOG:

-20220605-1 modify UpdateBalance to update based on last update time AND symbol
-20220605-2 implement stop limit buy order for short trade
-20220605-3 implement stop limit sell order for long trade
+20220605-4 adjust database to stop limit buy order for short trade
+20220605-5 adjust database to stop limit sell order for long trade
-20220607-1 start long trade if short trade has finished
-20220607-2 start short trade if long trade has finished
-20220607-3 create settings table with tradingbudget, mfiShortTreshold etc.
-20220611-1 adjust database to oco limit buy order for short trade
-20220611-2 adjust database to oco limit sell order for short trade



'''
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
takeProfit = 0.5
controlFlowLong = 0
sellPrice = 0
updateInterval = 4

# short trading
bbUpperBoundTreshold = 70 #price has to be above treshold factor times upperbound for a sell signal in a shor trade
mfiShortTreshold = 70 # mfi has to be higher then treshold for a mfi sell signal in a short trade

# long trading
bbLowerBoundTreshold = 30
mfiLongTreshold = 30

# tradePoolPercentage = 80 #trade with x% of total balance 



# start main program
programStart = hp.TimeStamp()
print('%s: Starting Prometheus version %s' %(programStart, programVersion))



while datetime.now() < program_end:
	
	try:
		request = requests.get(url, timeout=timeout)

		# tradeQuantity = ef.CheckBalance(coin) * (tradePoolPercentage/100)
		tf.TradeFunctionShort15M(coin, base, takeProfit, bbUpperBoundTreshold, mfiShortTreshold)
		tf.TradeFunctionLong15M(coin, base, takeProfit, bbLowerBoundTreshold, mfiLongTreshold)

		tf.UpdateBalance('BTC', 'USDT', updateInterval)
		

	except (requests.ConnectionError, requests.Timeout) as exception:
		print("Internet connection lost..")

	time.sleep(trade_interval)
