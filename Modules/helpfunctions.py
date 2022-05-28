import json, time, math
import datetime
from six.moves import urllib
from dateutil.parser import parse
import re
import time

# import ex_functions as ef

# import data 
# import data



ls_priceaction = []
ls_portfolio = []
ls_preselect = []
ls_select = []
ls_change = []
selection = []
maxReadAttempts = 4

# errormessages

error_calculate_profit = 'not enough datapoints'
error_coin_not_found = 'Messari coin price not found'
error_read_messari = 'read error Messari'






 
def ReadVortex(st):
	# end_index = len(st)
	start = st.find('(')
	end = st.find(')')
	coin = st[start+1:end]
	epoch = int(time.time())
	if st.find('rose') > 0:
		direction = 'long'
	else:
		direction = 'short'
	signal = (coin, direction, epoch)
	return signal




def AddCoinToPreselect(c):
	if ls_preselect.count(c) == 0:
		ls_preselect.append(c)
		timestamp = TimeStamp()
		print('%s: %s coin added to preselection' %(timestamp, c.upper()))



def CoinInPortfolio(c, ls): # checks if coin is in portfolio
	ls_coin = [x[0] for x in ls]
	if ls_coin.count(c) > 0:
		return True
	else:
		return False
	
def AddCoinToPortfolio(c,i,ls):
	# global ls_portfolio
	if CoinInPortfolio(c, ls) == False: #coin is not in portfolio
		coin = c
		action = ef.PriceAction(coin)
		datetime  = action[1]
		epoch = action[2]
		currentPrice = action[3]
		investment = i
		if currentPrice > 0:
			amount = investment / currentPrice
		tup = (coin, datetime, epoch, currentPrice, amount)
		ls.append(tup)
		timestamp = TimeStamp()
		print('%s: %s coin added to portfolio' %(timestamp, c.upper()))
	else:
		print('%s coin already in portfolio' %c.upper())





def UpdatePriceAction(s):
	global ls_priceaction
	coin = s[0].lower()

	
	# update priceaction list for all preselect coins
	if len(ls_preselect) > 0:
		for coin in ls_preselect:
			action = ef.PriceAction(coin)
			if isinstance(action, tuple):
				ls_priceaction.append(action)
			else:
				break
			

	else:
		print('no coins in preselection')




def SellSignal(s,p,t):
	if not ls_preselect:
		print ('no coins in preselection')
	# calculate profit during last t periods for all preselect coins
	for c in ls_preselect:
		profit = CalculateProfit(ls_priceaction,c,t)
		print('sellsignal loop')
		






def CheckCoinOnMessari(c):
	try:
		url = "https://data.messari.io/api/v1/assets/%s/metrics/market-data" %c
		result = urllib.request.urlopen(url).read()
	except:
		timestamp = TimeStamp()
		result = timestamp + ': ' + error_read_messari
		print(result)
		exit()

	dic = json.loads(result)


	price = dic['data']['market_data']['price_usd']
	if isinstance(price, float):
		return True
	else:
		return False

def TradeFunction(s,p,l,t,h):
	global ls_preselect
	global ls_portfolio

	if (s[1] == 'long'):
	# add to preselection if coin is new
		
		coin = s[0].lower()
		AddCoinToPreselect(coin)
		UpdatePriceAction(s)
		LongTrade(s,p,t)

	if (s[1] == 'short'):
		coin = s[0].lower()
		timestamp = TimeStamp()
		print('%s: %s has dropped on Vortex' %(timestamp,coin.upper()))


	# sell after holding period
	if len(ls_portfolio) > 0:
		
		for tup in ls_portfolio:
			coin = tup[0]
			epoch = tup[1]
			now = int(time.time())

			if epoch < (now - h):
				sellPrice = [x for x in ls_priceaction if x[0] == coin][-1][3] #latest price for c
				timestamp = TimeStamp()
				print('%s: SELL %s at %f' %(timestamp,coin, sellPrice))
				print('%s: %s coin has been removed from portfolio' %(timestamp,coin.upper()))
				ls_portfolio.remove(tup)
				





def CalculateProfit(ls,c,t):
	now = int(time.time())
	for i in reversed(ls):
		coin = i[0]
		epoch = i[2]
		if (c == coin) and (epoch > (now - t)):
			selection.append(i)
	
	# check if enough datapoints are gathered
	if (len(selection) > 1):

		open_price = selection[0][3]
		# print('open_price = %f' %open_price)
		close_price = selection[-1][3]
		# print('close_price = %f' %close_price)
		profit = round(((close_price - open_price) / open_price) * 100, 2)
		return (profit)
	else:
		return error_calculate_profit


def SignalChange(s):
	global ls_change
	if (ls_change == []) or (ls_change[-1] != s): #new signal
		ls_change.append(s) # add new signal to ls_change
		return True
	if ls_change[-1] == s: #signal is already known
		return False

def TimeStamp():
	now = int(time.time())
	result = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M')
	return result




def TimeStampEpoch():
	now = int(time.time())
	return now

def TimeStampEpochMS():
	now = int(time.time())
	return now * 1000

def StringToDatetime(st):
	return datetime.datetime.strptime(st, '%Y-%m-%d %H:%M:%S')


# print(StringToDatetime('2022-05-22 22:08:15'))


def EpochmsToDatetime(epoch):
	epoch = epoch / 1000 #convert to epoch in seconds
	return datetime.datetime.fromtimestamp(epoch)


def EpochmsToString(epoch):
	epoch = epoch / 1000 #convert to epoch in seconds
	return str(datetime.datetime.fromtimestamp(epoch))[0:19]

# print(EpochmsToString(1653084014524))

def CheckLoss(l):
	ls_coins_with_loss = []
	for i in ls_portfolio:
		coin = i[0]
		buyPrice = i[2]
		currentPrice = [x for x in ls_priceaction if x[0] == coin][-1][3]
		loss = ((buyPrice - currentPrice) / buyPrice) * 100
		if loss < l:
			ls_coins_with_loss.append(coin)
	return ls_coins_with_loss
		

def Checkprofit(p):
	ls_coins_with_profit = []
	for i in ls_portfolio:
		coin = i[0]
		buyPrice = i[2]
		currentPrice = [x for x in ls_priceaction if x[0] == coin][-1][3]
		profit = ((buyPrice - currentPrice) / buyPrice) * 100
		if profit > p:
			ls_coins_with_profit.append(coin)
	return ls_coins_with_profit


		
def SellOrder(ls, r):
	global ls_portfolio
	for c in ls:
		sellPrice = [x for x in ls_priceaction if x[0] == c][-1][3] #latest price for c
		timestamp = TimeStamp()
		print('%s: SELL %s because of %s at %f' %(timestamp,c ,r ,sellPrice))

		print('%s: %s has been removed from portfolio' %(timestamp,c))
		ls_portfolio = [x for x in ls_portfolio if x[0] != c]




def ShowCoinsInPreselection():
	ls_show = []
	if len(ls_preselect) > 0: 
		for coin in ls_preselect:
			ls_show.append(coin)

		timestamp = TimeStamp()
		text = '%s: In preselection: ' %timestamp

		print(text)
		print(ls_preselect)




def round_decimals_down(number:float, decimals:int=2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor

# x = 0.103700
# print(type(x))
# print(round_decimals_down(x, 5))
# print(type(round_decimals_down(x, 5)))


def round_decimals_up(number:float, decimals:int=2):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor




