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
updateInterval = 12
interval = 1
coin = 'BTC'
base = 'USDC'
takeProfit = 0.5
stopLimitSellPerc = 5
tradingBudgetPerc = 50
quantityPrecision = 5
pricePrecision = 2
#####





def MechLong(coin, base, tradingBudgetPerc, takeProfit, stopLimitSellPerc, quantityPrecision, pricePrecision):
	symbol = coin + base
	timestamp = str(hp.TimeStamp())

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
			status = 'FILLED'
			stopLimitSellPrice = hp.round_decimals_down(buyPrice * (1 - (stopLimitSellPerc/100)), pricePrecision)
			stopLimitStatus = 'OPEN'
			ocoSellOrderId = ef.OCOSellOrder(symbol, tradeQuantity, sellPrice, stopLimitSellPrice)
			if ocoSellOrderId != False: #oco order succeeded
				db.SQLInsertLongTrade(symbol, interval, orderId, timestamp, buyPrice, 0, 'NONE', sellPrice, status, tradeQuantity, ocoSellOrderId, stopLimitSellPerc, stopLimitSellPrice, stopLimitStatus)
			else:
				print('OCO SELL order not succeeded!')
		else:
			print('MechLong error: executing SimpleBuy function')
	else:
		print('MechLong error: executing PriceAction2') 


def UpdateLongOCOStatus(coin, base):
	symbol = coin + base
	openOrders = db.SQLOpenSellOCO(symbol)
	for orderId in openOrders:
		order = ef.LookupOrder(symbol, orderId)
		status = order['status']
		if status == 'NEW':
			pass
		else:
			db.SQLCloseSellOCO(status, symbol)
			print('order %f updated' %orderId)



MechLong(coin, base, tradingBudgetPerc, takeProfit, stopLimitSellPerc, quantityPrecision, pricePrecision)
UpdateLongOCOStatus(coin, base)
tf.UpdateBalance('BTC', 'USDC', updateInterval)

