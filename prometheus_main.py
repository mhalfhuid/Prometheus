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
import configdb as db
import talib_functions as ta


url = 'https://api.binance.com' #binance server
programVersion = '0.1 gamma'
trade_interval = 30
timeout = 5
programDuration = 24
program_end = datetime.now() + timedelta(hours = programDuration)
coin = 'BTC'
base = 'USDT'
symbol = coin + base
takeProfit = 0.5
flow1 = 0
flow2 = 0



# start main program
programStart = hp.TimeStamp()
print('%s: Starting Prometheus version %s' %(programStart, programVersion))



while datetime.now() < program_end:
	
	try:
		request = requests.get(url, timeout=timeout)
		mfi15 = ta.MFI_15M(coin, base)
		bb15 = ta.BBANDS_15M(coin, base)


		# mfi60 = ta.MFI_01H(coin, base)
		# bb60 = ta.BBANDS_01H(coin, base)
		timestamp = hp.TimeStamp()
		currentPrice = ef.PriceAction2(symbol)[3]

		
		# short strategy 15 min interval
		# print(bb15)
		bbUpperBound =  ((bb15[0] + bb15[1]) / 2)
		bbLowerBound = 	((bb15[1] + bb15[2]) / 2)
		# print(bbUpperBound)

		
		if currentPrice > bbUpperBound:
			print('%s BBANDS 15m SELL SIGNAL' %timestamp)
			if mfi15 > 70:
				print('%s MFI 15m SELL SIGNAL' % timestamp)
				print('%s SELL BTC' %timestamp)
			else:
				pass

		else:
			pass



		if currentPrice < bbLowerBound:
			print('%s BBANDS 15m BUY SIGNAL' %timestamp)
			if mfi15 < 20:
				print('%s MFI 15m BUY SIGNAL' % timestamp)
				print('%s BUY BTC' %timestamp)
			else:
				pass

		else:
			pass

§












	except (requests.ConnectionError, requests.Timeout) as exception:
		print("Internet connection lost..")

	time.sleep(trade_interval)
