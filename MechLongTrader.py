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



def MechLong(coin, base, tradingBudgetPerc, takeProfit, stopLimitSellPerc, quantityPrecision, pricePrecision):
	symbol = coin + base
	currentPrice = ef.PriceAction2(symbol)[3]
	if currentPrice != False:
		baseQuantity = ef.CheckBalance(base)
		quantity = baseQuantity / currentPrice
		tradeQuantity = hp.round_decimals_down((baseQuantity / currentPrice) * (tradingBudgetPerc/100), quantityPrecision)
		order = ef.SimpleBuy(coin, base, tradeQuantity)
		if order != False: #sell order succeeded, set oco order
			buyPrice = float(order['fills'][0]['price'])
			orderId = order['orderId']
			sellPrice = hp.round_decimals_down(buyPrice * (1 + (takeProfit/100)),pricePrecision)
			status = 'OPEN'
			stopLimitSellPrice = hp.round_decimals_down(buyPrice * (1 - (stopLimitSellPerc/100)), pricePrecision)
			stopLimitStatus = 'OPEN'
			ocoSellOrderId = ef.OCOSellOrder(symbol, tradeQuantity, sellPrice, stopLimitSellPrice)
		# 	print('\n')
		# if ocoBuyOrderId != False: #oco order succeeded
		# 	db.SQLInsertShortTrade(symbol, interval, orderId, timestamp, sellPrice, 0, 'NONE', buyPrice, status, quantity, ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus)
		# else:
		# 	ocoBuyOrderId = 0

#####
takeProfit = 0.5
stopLimitSellPerc = 5
quantityPrecision = 5
pricePrecision = 2
coin = 'BTC'
base = 'USDC'
tradingBudgetPerc = 33
#####

MechLong(coin, base, tradingBudgetPerc, takeProfit, stopLimitSellPerc, quantityPrecision, pricePrecision)

