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


#####
interval = 1
coin = 'BTC'
base = 'USDC'
takeProfit = 0.5
stopLimitBuyPerc = 10
tradingBudgetPerc = 33
quantityPrecision = 5
pricePrecision = 2
#####


def MechShort(coin, base,tradingBudgetPerc, takeProfit, stopLimitBuyPerc, quantityPrecision, pricePrecision):
	symbol = coin + base
	timestamp = str(hp.TimeStamp())
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
				status = 'FILLED'
				stopLimitBuyPrice = hp.round_decimals_down(sellPrice * (1 + (stopLimitBuyPerc/100)),pricePrecision)
				stopLimitStatus = 'OPEN'
				tradeQuantity = hp.round_decimals_down(tradeQuantity * (1 + (takeProfit/100)), quantityPrecision)
				ocoBuyOrderId = ef.OCOBuyOrder(symbol, tradeQuantity, buyPrice, stopLimitBuyPrice)
				if ocoBuyOrderId != False: #oco order succeeded
					db.SQLInsertShortTrade(symbol, interval, orderId, timestamp, sellPrice, 0, 'NONE', buyPrice, status, quantity, ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus)
				else:
					print('OCO SELL order not succeeded!')
			else:
				print('MechShort error: executing SimpleSell function')
		else:
			print('not enough base currency for the buy OCO order')
	else:
		print('MechShort error: executing PriceAction2')




def UpdateShortOCOStatus(coin, base):
	symbol = coin + base
	openOrders = db.SQLOpenBuyOCO(symbol)
	for orderId in openOrders:
		order = ef.LookupOrder(symbol, orderId)
		status = order['status']
		if status == 'NEW':
			pass
		else:
			db.SQLCloseBuyOCO(status, symbol)
			print('order %f updated' %orderId)


MechShort(coin, base,tradingBudgetPerc, takeProfit, stopLimitBuyPerc, quantityPrecision, pricePrecision)
UpdateShortOCOStatus(coin, base)
