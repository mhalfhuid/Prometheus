'''
tradesignal program sends mfi buy and sell signals via Telegram
for code see: https://www.youtube.com/watch?v=EQKGTpS8t9E

'''

# general modules
import requests
import sys, os
import sqlite3
from datetime import datetime, timedelta
import telegram, requests
import time

os.chdir('Modules')
path = os.getcwd()


sys.path.insert(0, path)
import ex_functions as ef
import helpfunctions as hp
import talib_functions as ta
import trade_functions as tf




api_key = '5520000262:AAHld11tzeG4C2SCGtquoCNhUlGJ7JSzspo'
base_url = 'https://api.telegram.org/bot'
POST_REQUEST = '/sendMessage'
parameters = {
	'chat_id': '-798640779', 
	'text':'mfi bandwith overshoot'
}


trade_interval = 20
timeout = 5
programDuration = 1
url = 'https://api.binance.com' #binance server
program_end = datetime.now() + timedelta(hours = programDuration)
coin = 'BTC'
base = 'USDC'
signal = 0


# start main program
programStart = hp.TimeStamp()
print('%s: Trade signaller' %programStart)



while datetime.now() < program_end:
	
	try:
		request = requests.get(url, timeout=timeout)

		mfi15 = ta.MFI_15M(coin, base)
		mfi01 = ta.MFI_01M(coin, base)

		if (mfi01 > 80 or mfi01 < 20) and signal < 2:
			response = requests.get(base_url + api_key + POST_REQUEST, data = parameters )
			print(response.text)
			print('mfi01: %f' %mfi01)
			print('mfi15: %f' %mfi15)
			signal += 1 

		

		

	except (requests.ConnectionError, requests.Timeout) as exception:
		timestamp = hp.TimeStamp()
		print("%s: Internet connection lost.." %timestamp)

	time.sleep(trade_interval)
