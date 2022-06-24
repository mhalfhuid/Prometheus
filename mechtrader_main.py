# MechTrader


import sys, os


os.chdir('Modules')
path = os.getcwd()


sys.path.insert(0, path)
import ex_functions as ef
import helpfunctions as hp
import talib_functions as ta
import trade_functions as tf
import configdb as db


takeProfit = 0.5
stopLimitBuyPerc = 2

#####
coin = 'XMR'
base = 'BUSD'
tradingBudgetPerc = 30
#####

def MechShort(coin, base,tradingBudgetPerc, takeProfit, stopLimitBuyPerc):
	symbol = coin + base
	currentPrice = ef.PriceAction2(symbol)
	if currentPrice != False:
		coinQuantity = ef.CheckBalance(coin)
		tradeQuantity = hp.round_decimals_down(quantity * (tradingBudgetPerc/100),5)
		baseQuantity = ef.CheckBalance(base)
		if baseQuantity > 0.1 * coinQuantity * currentPrice:
			order = ef.SimpleSell(coin, base, tradeQuantity)
			if order != False: #sell order succeeded, set oco order
				sellPrice = float(order['fills'][0]['price'])
				orderId = order['orderId']
				buyPrice = hp.round_decimals_down(sellPrice * (1 - (takeProfit/100)),1)
				status = 'OPEN'
				stopLimitBuyPrice = hp.round_decimals_down(sellPrice * (1 + (stopLimitBuyPerc/100)),1)
				stopLimitStatus = 'OPEN'
				ocoBuyOrderId = ef.OCOBuyOrder(symbol, tradeQuantity, buyPrice, stopLimitBuyPrice)
		else:
			print('not enough base currency for the buy OCO order')
	else:
		print('PriceAction2 error')
			# print('\n')
			# if ocoBuyOrderId != False: #oco order succeeded
			# 	db.SQLInsertShortTrade(symbol, interval, orderId, timestamp, sellPrice, 0, 'NONE', buyPrice, status, quantity, ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus)
			# else:
			# 	ocoBuyOrderId = 0


def MechLong(coin, base, quantity, takeProfit, stopLimitSellPerc):
	symbol = coin + base
	order = ef.SimpleBuy(coin, base, quantity)
	if order != False: #sell order succeeded, set oco order
		buyPrice = float(order['fills'][0]['price'])
		orderId = order['orderId']
		sellPrice = hp.round_decimals_down(buyPrice * (1 + (takeProfit/100)),1)
		status = 'OPEN'
		stopLimitSellPrice = hp.round_decimals_down(buyPrice * (1 - (stopLimitSellPerc/100)),1)
		stopLimitStatus = 'OPEN'
		ocoSellOrderId = ef.OCOSellOrder(symbol, quantity, sellPrice, stopLimitSellPrice)
		# print('\n')
		# if ocoBuyOrderId != False: #oco order succeeded
		# 	db.SQLInsertShortTrade(symbol, interval, orderId, timestamp, sellPrice, 0, 'NONE', buyPrice, status, quantity, ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus)
		# else:
		# 	ocoBuyOrderId = 0



takeProfit = 0.5
stopLimitBuyPerc = 2

#####
coin = 'BTC'
base = 'USDC'

#####
# MechShort(coin, base, 30, takeProfit, stopLimitBuyPerc)

# takeProfit = 0.5
# stopLimitSellPerc = 2
# MechLong(coin, base, quantity, takeProfit, stopLimitSellPerc)
order = ef.SimpleBuy(coin, base, 0.02)


