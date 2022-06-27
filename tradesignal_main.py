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

# event = 'hello'
# parameters = {
# 	'chat_id': '-798640779', 
# 	'text': event
# }


trade_interval = 60
timeout = 5
programDuration = 36
url = 'https://api.binance.com' #binance server
program_end = datetime.now() + timedelta(hours = programDuration)
coin = 'BTC'
base = 'USDC'
signal = 0
event = 'Starting signaller..'


# start main program
programStart = hp.TimeStamp()
print('%s: Trade signaller' %programStart)



symbol = 'BTCUSDC'

while datetime.now() < program_end:
	
	try:
		request = requests.get(url, timeout=timeout)

		mfi15 = ta.MFI_15M(coin, base)
		mfi01 = ta.MFI_01M(coin, base)


		
		# parameters = {
		# 	'chat_id': '-798640779', 
		# 	'text': event
		# }

			


		if mfi15 < 30 or mfi15 > 70:
			event = 'mfi15 exceeds threshold'
			parameters = {
				'chat_id': '-798640779', 
				'text': event
			}

			response = requests.get(base_url + api_key + POST_REQUEST, data = parameters)


		if mfi01 < 30 or mfi01 > 70:
			event = 'mfi01 exceeds threshold'
			parameters = {
				'chat_id': '-798640779', 
				'text': event
			}

			response = requests.get(base_url + api_key + POST_REQUEST, data = parameters)



			# btcBalance = ef.CheckBalanceTotal('BTC')
			# event = 'btc total balance: ' + str(hp.round_decimals_down(btcBalance[1] + btcBalance[0],5))
			# parameters = {
			# 	'chat_id': '-798640779', 
			# 	'text': event
			# }
			# response = requests.get(base_url + api_key + POST_REQUEST, data = parameters)

			# time.sleep(10)



			# usdcBalance = ef.CheckBalanceTotal('USDC')
			# event = 'usdc total balance: ' + str(hp.round_decimals_down(usdcBalance[1] + usdcBalance[0],2))
			# parameters = {
			# 	'chat_id': '-798640779', 
			# 	'text': event
			# }
			# response = requests.get(base_url + api_key + POST_REQUEST, data = parameters)



			

	except (requests.ConnectionError, requests.Timeout) as exception:
		timestamp = hp.TimeStamp()
		print("%s: Internet connection lost.." %timestamp)

	time.sleep(trade_interval)
