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




def MechShort(coin, base,tradingBudgetPerc, takeProfit, stopLimitBuyPerc, quantityPrecision, pricePrecision):
	symbol = coin + base
	currentPrice = ef.PriceAction2(symbol)[3]
	if currentPrice != False:
		coinQuantity = ef.CheckBalance(coin)

		tradeQuantity = hp.round_decimals_down(coinQuantity * (tradingBudgetPerc/100),quantityPrecision)
		baseQuantity = ef.CheckBalance(base)
		if baseQuantity > 0.1 * tradeQuantity * currentPrice:
			order = ef.SimpleSell(coin, base, tradeQuantity)
			if order != False: #sell order succeeded, set oco order
				sellPrice = float(order['fills'][0]['price'])
				orderId = order['orderId']
				buyPrice = hp.round_decimals_down(sellPrice * (1 - (takeProfit/100)),pricePrecision)
				status = 'OPEN'
				stopLimitBuyPrice = hp.round_decimals_down(sellPrice * (1 + (stopLimitBuyPerc/100)),pricePrecision)
				stopLimitStatus = 'OPEN'
				tradeQuantity = hp.round_decimals_down(tradeQuantity * (1 + (takeProfit/100)), quantityPrecision)
				ocoBuyOrderId = ef.OCOBuyOrder(symbol, tradeQuantity, buyPrice, stopLimitBuyPrice)
			else:
				print('error when executing SimpleSell function')
		else:
			print('not enough base currency for the buy OCO order')
	# else:
	# 	print('PriceAction2 error')
			# print('\n')
			# if ocoBuyOrderId != False: #oco order succeeded
			# 	db.SQLInsertShortTrade(symbol, interval, orderId, timestamp, sellPrice, 0, 'NONE', buyPrice, status, quantity, ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus)
			# else:
			# 	ocoBuyOrderId = 0


#####
coin = 'BTC'
base = 'USDC'
takeProfit = 0.5
stopLimitBuyPerc = 5
tradingBudgetPerc = 33
quantityPrecision = 5
pricePrecision = 2
#####
MechShort(coin, base,tradingBudgetPerc, takeProfit, stopLimitBuyPerc, quantityPrecision, pricePrecision)

