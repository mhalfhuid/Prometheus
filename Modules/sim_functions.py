import json, time
import datetime
from six.moves import urllib
from dateutil.parser import parse
import re
import time
import helpfunctions as hp
import ex_functions as ef

import math



ls_priceaction = []
ls_portfolio = []
ls_preselect = []
ls_select = []
ls_change = []
selection = []
ls_tracker = []
maxReadAttempts = 4
cashValue = 178

# base currency
# base = 'USDT'

# error messages
error_calculate_profit = 'not enough datapoints'
error_coin_not_found = 'Messari coin price not found'
error_read_messari = 'read error Messari'

def SimpleBuy(c, a):
	coin = c
	amount = a
	timestamp = hp.TimeStamp()
	print('%s: buying %s USD of %s coin' %(timestamp, round(amount,4), coin.upper()))


def SimpleSell(c, a):
	coin = c
	amount = a
	timestamp = hp.TimeStamp()
	print('%s: selling %s USD of %s coin' %(timestamp, round(amount,4), coin.upper()))




def PortfolioValue():
	# Calculates value of all assets in ls_portfolio given their amount and real time price
	# input: ls_portfolio | output: total porfotio value in dollars
	totalValue = 0
	for i in ls_portfolio:
		coin = i[0]
		action = ef.PriceAction(coin, ef.base)
		currentPrice = action[3]
		amount = i[1]
		currentValue = currentPrice * amount
		totalValue += currentValue

	return round(totalValue,2) 



def CashValue():
	return round(cashValue,4)

def GetPortfolio():
	return ls_portfolio




def UpdatePriceData():
	global ls_portfolio
	
	lss = []
	for i in ls_portfolio:
		coin = i[0]
		amount = i[1]
		action = ef.PriceAction(coin, ef.base)
		currentPrice = action[3]
		epoch = int(time.time())
		timestamp = hp.TimeStamp() 

		tup = (coin, amount)
		lss.append(tup)
	
	ls_portfolio = lss


def PortfolioReplace(ls, c, tup):
	ls = [x for x in ls if x[0] != c] #delete c from ls
	ls = ls.append(tup)	#add tup to ls
	return ls


def PortfolioScaleUp(ls): 
# scales up porftolio with new coin c by virtually selling a fraction of each existing coin in order to buy a new coin c
# input: coin c| output: updated portfolio with new coin c
	lss = []
	totalSoldDollarValue = 0


	# only applies to coins that are not already in portfolio

	numberOfCoins = len(ls)
	if numberOfCoins > 0:
		sellFraction = 1 / (numberOfCoins + 1)

	

	lss = []
	for i in ls:
		
		coin = i[0]
		datetime = i[1]
		epoch = i[2]
		buyPrice = i[3]
		amount = i[4]

		action = ef.PriceAction(coin)
		currentPrice = action[3]
		currentValue = currentPrice * amount

		
		sellAmount = amount * sellFraction
		soldDollarValue = round(currentValue * sellFraction,4)
		soldAmount = round(soldDollarValue * (1 / currentPrice),4)
		totalSoldDollarValue += soldDollarValue
		soldDollarValue = round(soldDollarValue,4)
		
		timestamp = hp.TimeStamp()
		print('%s: splitting portfolio, selling %f USD of %s equals %f coins' %(timestamp, soldDollarValue, coin.upper(), round(soldAmount,4)))
		
		tup = (coin, datetime, epoch, currentPrice, round((amount - sellAmount),4))


		lss.append(tup)
	totalSoldDollarValue = round(totalSoldDollarValue,4)
	return (totalSoldDollarValue,lss)
	

	



def PortfolioScaleDown(c, ls):
	global ls_portfolio
	global cashValue

	coin = c

	if len(ls) == 1:
		ls_tup = [x for x in ls if x[0] == coin]
		tup = ls_tup[0]
		amount = tup[4]
		timestamp = hp.TimeStamp()
		action = ef.PriceAction(coin)
		currentPrice = action[3]
		currentDollarValue = currentPrice * amount
		print('%s: close down portfolio' %(timestamp))
		
		SimpleSell(coin, currentDollarValue)
		ls_portfolio = []
		cashValue = currentDollarValue

	else:
		timestamp = hp.TimeStamp()
		print('%s: remove %s coin from portfolio'  %(timestamp, coin.upper()))
		
		ls_tup = [x for x in ls if x[0] == coin]
		tup = ls_tup[0]
		amount = tup[4]

		action = ef.PriceAction(coin)
		currentPrice = action[3]
		currentDollarValue = currentPrice * amount

		SimpleSell(coin, currentDollarValue)
		ls_portfolio.remove(tup)

		numberOfCoins = len(ls_portfolio)
		if numberOfCoins > 0:
			buyFraction = round(currentDollarValue * (1 / numberOfCoins),4)

		# print('buy %d in USD of remaining coin(s)' %buyFraction)

		lss = []
		# lss_temp = ls_portfolio
		for i in ls_portfolio:
			coin = i[0]
			action = ef.PriceAction(coin)
			currentPrice = action[3]	
			datetime = i[1]
			epoch = i[2]
			oldAmount = i[4]
			amount = (buyFraction * (1 / currentPrice)) + oldAmount
			SimpleBuy(coin, buyFraction)

			tup = (coin, datetime, epoch, currentPrice, round(amount,4))
			lss.append(tup)

		ls_portfolio = lss







def TradeFunction(s,m):
	global ls_preselect
	global ls_portfolio
	global cashValue


	coin = s[0]
	direction = s[1]
	mode = m
	# amount = a

	print('TradeFunction activated')

	# ls_portfolio = [ ('bnb',4),('ksm',2)] #TESTING!!!
	
	if (direction == 'rose') and (len(ls_portfolio) == 0): # adding new coin to new portfolio
		initialInvestment = cashValue
		cashValue = 0
		free_balance  = ef.CheckBalance(ef.base)
		if initialInvestment < free_balance:
			ef.MarketBuy(coin, ef.base, initialInvestment, mode)
			ls_portfolio = ef.AddCoinToPortFolio2(coin,ls_portfolio, mode)


		else:
			print ('Initial investment of %f exceeds free balance of %f on exchange, exit program...' %(initialInvestment, free_balance))
			exit()
		
	elif (direction == 'rose') and (len(ls_portfolio) > 0): # adding new coin to existing portfolio
		if hp.CoinInPortfolio(coin, ls_portfolio) == False:	#coin is not in portfolio
			ls_portfolio = ef.PortfolioScaleUp2(ls_portfolio, coin, mode)
			

		else: 
			print('%s coin already in portfolio' %coin.upper() )

	elif (direction == 'dropped') and (len(ls_portfolio) > 1): # deleting existing coin to existing portfolio
		if hp.CoinInPortfolio(coin, ls_portfolio) == True:	#coin is in portfolio
			print('scaling down %s coin' %coin)
			ls_portfolio = ef.PortfolioScaleDown2(ls_portfolio, coin, mode)

	elif (direction == 'dropped') and (len(ls_portfolio) == 1): # deleting existing coin to existing portfolio
		if hp.CoinInPortfolio(coin, ls_portfolio) == True:	#coin is in portfolio
			print('closing down portfolio')
			cashValue = ef.ClosePortfolio(ls_portfolio, mode)
			ls_portfolio = []
			
			












