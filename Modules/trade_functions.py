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
sellStopLoss = 2.0
buyStopLoss = 2.0


def TradeFunctionShort15M(coin, base, takeProfit, bbUpperBoundTreshold, mfiShortTreshold):
	# short strategy 15 min interval: sell
	symbol = coin + base
	interval = '15M'
	timestamp = hp.TimeStamp()
	symbol = coin + base
	currentPrice = ef.PriceAction2(symbol)

	
	if currentPrice != False:
		currentPrice = hp.round_decimals_down(currentPrice[3],1)
		bb15 = ta.BBANDS_15M(coin, base)
		bbUpperBound = ta.BBRangeToPercent(bb15, bbUpperBoundTreshold)
		# buyPrice = hp.round_decimals_down(db.SQLLookupBuyPrice(),0)
		
		lastOrder = db.SQLLastShortTransaction(symbol)			
		if lastOrder == False:
			buyPrice = 0
			status = 'FILLED'
			stopLimitStatus = 'CLOSED'
			buyOrderId = 0
			ocoBuyOrderId = 0

		else:
			buyPrice = lastOrder[0]
			status = lastOrder[3]
			stopLimitStatus = lastOrder[4]
			buyOrderId = lastOrder[5]
			ocoBuyOrderId = lastOrder[6]


		lastLongOrder = db.SQLLastLongTransaction(symbol)
		if lastLongOrder == False:
			statusLong = 'FILLED'
			stopLimitStatus = 'CLOSED'
		else:
			statusLong = lastLongOrder[3]
			stopLimitStatus = lastOrder[4]
		



		if currentPrice > bbUpperBound and status == 'FILLED' and statusLong == 'FILLED' \
			and stopLimitStatus == 'CLOSED': #start new trade
			mfi15 = ta.MFI_15M(coin, base)
			

			if mfi15 > mfiShortTreshold:
				quantity = ef.CheckBalance(coin)
				quantity = ef.RoundStepSize(symbol, quantity, tradingBudget)
				print('%s MARKET SELL %s at %f quantity %f' %(timestamp, coin, currentPrice, quantity))
				order = ef.SimpleSell(coin, base, quantity)
				if order != False: #sell order succeeded, set oco order
					sellPrice = float(order['fills'][0]['price'])
					orderId = order['orderId']
					buyPrice = hp.round_decimals_down(sellPrice * (1 - (takeProfit/100)),1)
					status = 'OPEN'
					stopLimitBuyPerc = buyStopLoss
					stopLimitBuyPrice = hp.round_decimals_down(sellPrice * (1 + (stopLimitBuyPerc/100)),1)
					stopLimitStatus = 'OPEN'
					ocoBuyOrderId = ef.OCOBuyOrder(symbol, quantity, buyPrice, stopLimitBuyPrice)
					print('\n')
					if ocoBuyOrderId != False: #oco order succeeded
						db.SQLInsertShortTrade(symbol, interval, orderId, timestamp, sellPrice, 0, 'NONE', buyPrice, status, quantity, ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus)
					else:
						ocoBuyOrderId = 0

		status = ef.CheckOrderStatus(symbol, ocoBuyOrderId)
		if status != 'NEW': # oco is filled or closed
			db.SQLCloseBuyOCO(symbol, status)



def TradeFunctionLong15M(coin, base, takeProfit, bbLowerBoundTreshold, mfiLongTreshold):
# long strategy 15 min interval: buy
	symbol = coin + base
	interval = '15M'
	timestamp = hp.TimeStamp()
	symbol = coin + base
	currentPrice = ef.PriceAction2(symbol)

	
	if currentPrice != False:
		currentPrice = hp.round_decimals_down(currentPrice[3],1)
		bb15 = ta.BBANDS_15M(coin, base)
		bbLowerBound = ta.BBRangeToPercent(bb15, bbLowerBoundTreshold)
		# buyPrice = hp.round_decimals_down(db.SQLLookupBuyPrice(),0)
		
		lastOrder = db.SQLLastLongTransaction(symbol)			
		if lastOrder == False:
			sellPrice = 0
			status = 'FILLED'
			stopLimitStatus = 'CLOSED'
			sellOrderId = 0
			ocoSellOrderId = 0
		else:
			sellPrice = lastOrder[0]
			status = lastOrder[3]
			stopLimitStatus = lastOrder[4]
			sellOrderId = lastOrder[5]
			ocoSellOrderId = lastOrder[6]

		lastShortOrder = db.SQLLastShortTransaction(symbol)
		if lastShortOrder == False:
			statusShort = 'FILLED'
			stopLimitStatus = 'CLOSED'
		else:
			statusShort = lastShortOrder[3]
			stopLimitStatus = lastShortOrder[4]
		

		if currentPrice < bbLowerBound and status == 'FILLED' and statusShort == 'FILLED' \
			and stopLimitStatus == 'CLOSED' : #start new trade
			mfi15 = ta.MFI_15M(coin, base)

			if mfi15 < mfiLongTreshold:
				quantity = ef.CheckBalance(coin)
				quantity = ef.RoundStepSize(symbol, quantity, tradingBudget)
				print('%s MARKET BUY %s at %f quantity %f' %(timestamp, coin, currentPrice, quantity))
				order = ef.SimpleBuy(coin, base, quantity)
				if order != False: #buy order succeeded set oco order
					buyPrice = float(order['fills'][0]['price'])
					orderId = order['orderId']
					sellPrice = hp.round_decimals_down(buyPrice * (1 + (takeProfit/100)),1)
					status = 'OPEN'
					stopLimitSellPerc = sellStopLoss
					stopLimitSellPrice = hp.round_decimals_down(buyPrice * (1 - (stopLimitSellPerc/100)),1)
					stopLimitStatus = 'OPEN'
					ocoSellOrderId = ef.OCOSellOrder(symbol, quantity, sellPrice, stopLimitSellPrice)
					print('\n')
					if ocoSellOrderId != False: #oco order succeeded
						db.SQLInsertLongTrade(symbol, interval, orderId, timestamp, buyPrice, 0, 'NONE', sellPrice, status, quantity, ocoSellOrderId, stopLimitSellPerc, stopLimitSellPrice, stopLimitStatus)



		status = ef.CheckOrderStatus(symbol, ocoSellOrderId)
		if status != 'NEW': #OCO is closed or filled
			db.SQLCloseSellOCO(symbol, status)



	


def UpdateBalance(coin, base, updateInterval):
	symbol = coin + base
	lastBalance = db.SQLLastBalance()

	try:
	
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
			if datetime.now() > lastTime + timedelta(hours = updateInterval):
				coinBalance = ef.CheckBalanceTotal(coin)
				baseBalance = ef.CheckBalanceTotal(base)
				totalCoinBalance = hp.round_decimals_down(coinBalance[0] + coinBalance[1],5)
				currentPrice = ef.PriceAction2(symbol)[3]
				totalBaseBalance = hp.round_decimals_down(baseBalance[0] + baseBalance[1],2) 
				totalValue = hp.round_decimals_down(totalBaseBalance + (totalCoinBalance * currentPrice),2)
				epoch = hp.TimeStampEpochMS()
				balanceTime = hp.EpochmsToString(epoch)
				db.SQLInsertBalance(symbol, balanceTime, totalCoinBalance, totalBaseBalance, totalValue)
	except:
		print('UpdateBalance function failed...')


