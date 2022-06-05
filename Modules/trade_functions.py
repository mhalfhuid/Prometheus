# trade_functions
import ex_functions as ef
import helpfunctions as hp
import talib_functions as ta
import configdb as db
from datetime import datetime, timedelta

# initialise
controlFlowShort = 0
buyPrice = 0
tradingBudget = 90 #percentage of total balance involved in each trade


def TradeFunctionShort15M(coin, base, takeProfit, bbUpperBoundTreshold, mfiShortTreshold):
	# short strategy 15 min interval: sell phase I
	symbol = coin + base
	interval = '15M'
	timestamp = hp.TimeStamp()
	symbol = coin + base
	currentPrice = ef.PriceAction2(symbol)

	
	if currentPrice != False:
		currentPrice = hp.round_decimals_down(currentPrice[3],0)
		bb15 = ta.BBANDS_15M(coin, base)
		bbUpperBound = ta.BBRangeToPercent(bb15, bbUpperBoundTreshold)
		lastOrder = db.SQLLastShortTransaction()	
		status = lastOrder[3]
		buyPrice = hp.round_decimals_down(db.SQLLookupBuyPrice(),0)

		if currentPrice > bbUpperBound and status == 'FILLED': #start new trade
			mfi15 = ta.MFI_15M(coin, base)
			

			if mfi15 > mfiShortTreshold:
				quantity = ef.CheckBalance(coin)
				quantity = ef.RoundStepSize(symbol, quantity, tradingBudget)
				print('%s PHASE I SHORT: MARKET SELL %s at %f quantity %f' %(timestamp, coin, currentPrice, quantity))
				order = ef.SimpleSell(coin, base, quantity)
				sellPrice = float(order['fills'][0]['price'])
				orderId = order['orderId']
				buyPrice = hp.round_decimals_down(sellPrice * (1 - (takeProfit/100)),0)
				status = 'OPEN'
				db.SQLInsertShortTrade(symbol, interval, orderId, timestamp, sellPrice, 0, 'NONE', buyPrice, status, quantity)


		#short strategy 15 min interval: buy back phase
		lastOrder = db.SQLLastShortTransaction()
		buyPrice = lastOrder[0]
		sellPrice = lastOrder[1]
		quantity = lastOrder[2]

		if currentPrice < buyPrice and status == 'OPEN':

			print('%s PHASE II SHORT: MARKET BUY %s with profit %f percent at %f quantity %f' %(timestamp,coin, takeProfit, currentPrice, quantity))
			order = ef.SimpleBuy(coin, base, quantity)
			buyPrice = float(order['fills'][0]['price'])
			orderId = order['orderId'] 
			status = 'FILLED'
			db.SQLUpdateBuyBack(orderId, timestamp, buyPrice, status)


def TradeFunctionLong15M(coin, base, takeProfit, bbLowerBoundTreshold, mfiLongTreshold):
	# long strategy 15 min interval: buy phase I
	symbol = coin + base
	interval = '15M'
	timestamp = hp.TimeStamp()
	symbol = coin + base
	currentPrice = ef.PriceAction2(symbol)	

	if currentPrice != False:
		currentPrice = hp.round_decimals_down(currentPrice[3],0)
		bb15 = ta.BBANDS_15M(coin, base)
		bbLowerBound = ta.BBRangeToPercent(bb15, bbLowerBoundTreshold)
		lastOrder = db.SQLLastLongTransaction()
		status = lastOrder[3]
		buyPrice = hp.round_decimals_down(db.SQLLookupBuyPrice(),0)
	
		if currentPrice < bbLowerBound and status == 'FILLED': #start new trade
			mfi15 = ta.MFI_15M(coin, base)

			if mfi15 < mfiLongTreshold:
				quantity = ef.CheckBalance(coin)
				quantity = ef.RoundStepSize(symbol, quantity, tradingBudget)
				print('%s PHASE I LONG: MARKET BUY %s at %f quantity %f' %(timestamp, coin, currentPrice, quantity))
				order = ef.SimpleBuy(coin, base, quantity)
				buyPrice = float(order['fills'][0]['price'])
				orderId = order['orderId']
				sellPrice = hp.round_decimals_down(buyPrice * (1 + (takeProfit/100)),0)
				status = 'OPEN'
				db.SQLInsertLongTrade(symbol, interval, orderId, timestamp, buyPrice, 0, 'NONE', sellPrice, status, quantity)


		#short strategy 15 min interval: buy back phase
		orderData = db.SQLLastLongTransaction()
		buyPrice = orderData[0]
		sellPrice = orderData[1]
		quantity = orderData[2]

		if currentPrice > sellPrice and status == 'OPEN':

			print('%s PHASE II LONG: MARKET SELL %s with profit %f percent at %f quantity %f' %(timestamp, coin, takeProfit, currentPrice, quantity))
			order = ef.SimpleSell(coin, base, quantity)
			sellPrice = float(order['fills'][0]['price'])
			orderId = order['orderId'] 
			status = 'FILLED'
			db.SQLUpdateSellBack(orderId, timestamp, sellPrice, status)




def UpdateBalance(coin, base):
	symbol = coin + base
	lastBalance = db.SQLLastBalance()
	
	if lastBalance == 'empty balance':
		lastTime = hp.TimeStamp()
		coinBalance = ef.CheckBalanceTotal(coin)
		baseBalance = ef.CheckBalanceTotal(base)
		totalCoinBalance = hp.round_decimals_down(coinBalance[0] + coinBalance[1],5)
		currentPrice = ef.PriceAction2(symbol)[3]
		totalBaseBalance = hp.round_decimals_down(baseBalance[0] + baseBalance[1],2) 
		totalValue = hp.round_decimals_down(totalBaseBalance + (totalCoinBalance * currentPrice),2)
		epoch = hp.TimeStampEpochMS()
		balanceTime = hp.EpochmsToString(epoch)
		db.SQLInsertBalance(symbol, balanceTime, totalCoinBalance, totalBaseBalance, totalValue)

	else:
		lastBalance = db.SQLLastBalance()
		lastTime = hp.StringToDatetimesec(lastBalance[2])
		if datetime.now() > lastTime + timedelta(hours = 4):
			coinBalance = ef.CheckBalanceTotal(coin)
			baseBalance = ef.CheckBalanceTotal(base)
			totalCoinBalance = hp.round_decimals_down(coinBalance[0] + coinBalance[1],5)
			currentPrice = ef.PriceAction2(symbol)[3]
			totalBaseBalance = hp.round_decimals_down(baseBalance[0] + baseBalance[1],2) 
			totalValue = hp.round_decimals_down(totalBaseBalance + (totalCoinBalance * currentPrice),2)
			epoch = hp.TimeStampEpochMS()
			balanceTime = hp.EpochmsToString(epoch)
			db.SQLInsertBalance(symbol, balanceTime, totalCoinBalance, totalBaseBalance, totalValue)



UpdateBalance('BTC', 'USDT')

##################################################
# update balance

# sql_last_balance = """SELECT buyPrice, sellPrice, quantity, status
# FROM LONGTRADE WHERE buyTransactTime IN (
# SELECT MAX(buyTransactTime)
# FROM LONGTRADE
# ) """

# 		if lastTime == None:
# 			coinBalance = ef.CheckBalanceTotal(coin)
# 			baseBalance = ef.CheckBalanceTotal(base)
# 			totalCoinBalance = coinBalance[0] + coinBalance[1]
# 			currentPrice = ef.PriceAction2(symbol)[3]
# 			totalBalance = baseBalance[0] + baseBalance[1] + (totalCoinBalance * currentPrice)
# 			totalBalance = hp.round_decimals_down(totalBalance, 2)
# 			epoch = hp.TimeStampEpochMS()
# 			balanceTime = hp.EpochmsToString(epoch)
# 			db.SQLInsertBalance(strategy, symbol, balanceTime, totalBalance)

# 		else:
# 			lastTime = db.SQLLastBalance()
# 			if datetime.now() > hp.StringToDatetime(lastTime) + timedelta(hours = 4):
# 				coinBalance = ef.CheckBalanceTotal(coin)
# 				baseBalance = ef.CheckBalanceTotal(base)
# 				totalCoinBalance = coinBalance[0] + coinBalance[1]
# 				currentPrice = ef.PriceAction2(symbol)[3]
# 				totalBalance = baseBalance[0] + baseBalance[1] + (totalCoinBalance * currentPrice)
# 				totalBalance = hp.round_decimals_down(totalBalance, 2)
# 				epoch = hp.TimeStampEpochMS()
# 				balanceTime = hp.EpochmsToString(epoch)
# 				db.SQLInsertBalance(strategy, symbol, balanceTime, totalBalance)


