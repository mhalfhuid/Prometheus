# setup config tables in monitor.db
import os, sys
import sqlite3
import helpfunctions as hp
import pandas as pd
from datetime import datetime, timedelta



# define connection and database
# connection = sqlite3.connect('../Database/monitor.db') # holds vortex trade tables
connection = sqlite3.connect('/Users/malcolmhalfhuid/Python/Ava2/Database/monitor.db')
cursor = connection.cursor()

#----------------------------BEGIN CONFIG TABLE------------------------------------
# creating config table
sql_config = """CREATE TABLE IF NOT EXISTS
CONFIG(config_id INTEGER PRIMARY KEY, coin TEXT, base TEXT, interval TEXT, treshold BLOB NOT NULL,  stoploss REAL, stoplossTrigger REAL, stoplossOffset REAL, tradingPause REAL, budget INTEGER, strategy TEXT)"""
cursor.execute(sql_config)

# config insert query
sql_insert_config = """INSERT INTO CONFIG (coin, base, interval, treshold, stoploss, stoplossTrigger, stoplossOffset, tradingPause, budget, strategy) VALUES (?,?,?,?,?,?,?,?,?,?)"""
sql_select_config = """SELECT * FROM CONFIG WHERE config_id = ?"""
sql_select_all_config_long = """SELECT * FROM CONFIG WHERE STRATEGY = 'LONG' """
sql_select_all_config_short = """SELECT * FROM CONFIG WHERE STRATEGY = 'SHORT' """
sql_add_column_config = """ALTER TABLE CONFIG ADD COLUMN STRATEGY 'TEXT' """
sql_update_config = """UPDATE CONFIG SET STRATEGY = 'LONG' """
sql_trade_interval = """SELECT interval FROM CONFIG WHERE config_id in  (SELECT tradestatusconfig_id FROM TRADE WHERE buyorder_id = ?)"""





# define config insert function
coin = 'BTC'
base = 'USDC'
interval = '1D'
treshold = '(30,1)'
stoploss = 30
stoplossTrigger = 4
stoplossOffset = 1
tradingPause = 1 
budget = 10
strategy = 'LONG'

def SQLInsertConfig(coin, base, interval, treshold, stoploss, stoplossTrigger, stoplossOffset, tradingPause, budget, strategy):
	cursor.execute(sql_insert_config, (coin, base, interval, treshold, stoploss, stoplossTrigger, stoplossOffset, tradingPause, budget, strategy) )
	connection.commit()	

# SQLInsertConfig(coin, base, interval, treshold, stoploss, stoplossTrigger, stoplossOffset, tradingPause, budget, strategy)

def SQLTradeInterval(orderId):
	cursor.execute(sql_trade_interval, (orderId,))
	interval = cursor.fetchall()
	if interval == []:
		return interval
	else:
		return interval[0][0]

# config show all

def GetConfig(configId):
	cursor.execute(sql_select_config, (configId,))
	ls = cursor.fetchall()
	return ls

# print(GetConfig(1))

def ReadConfigLong():
	cursor.execute(sql_select_all_config_long)
	ls = cursor.fetchall()
	return ls

def ReadConfigShort():
	cursor.execute(sql_select_all_config_short)
	ls = cursor.fetchall()
	return ls






def GetTresholdFromConfig(configId):
	cursor.execute(sql_select_config, (configId,))
	ls = cursor.fetchall()
	treshold = ls[0][4]
	treshold = treshold.replace('(','')
	treshold = treshold.replace(')','')
	treshold = treshold.split(',')
	treshold = [int(x) for x in treshold]


	return treshold


#----------------------------END CONFIG TABLE------------------------------------













#----------------------------BEGIN TRANSACTIONS TABLE------------------------------------
# creating transaction table
sql_init_transaction = """CREATE TABLE IF NOT EXISTS
TRANSACTIONS(transaction_id INTEGER PRIMARY KEY, coin TEXT, base TEXT, orderId INTEGER, transactTime TEXT, side TEXT, status TEXT, price REAL, quantity REAL, strategy TEXT, trade TEXT)"""
cursor.execute(sql_init_transaction)

# # transactioin insert query
sql_insert_transaction = """INSERT INTO TRANSACTIONS (coin, base, orderId, transactTime, side, status, price, quantity, strategy, trade) VALUES (?,?,?,?,?,?,?,?,?,'open')"""
sql_lookup_transaction = """SELECT * FROM TRANSACTIONS WHERE orderId = ?"""
sql_add_column_transactions = """ALTER TABLE TRANSACTIONS ADD COLUMN strategy 'TEXT' """
sql_last_transaction = """SELECT * from TRANSACTIONS WHERE transaction_id in (select max(transaction_id) from TRANSACTIONS where coin = ? and base = ? and strategy = ?) """
sql_purchase_price = """SELECT price FROM TRANSACTIONS WHERE transaction_id in (SELECT MIN(transaction_id) from TRANSACTIONS WHERE coin = ? and side = 'BUY' and base = ? and strategy = 'VORTEX' and trade = 'open') """
sql_close_portfolio = """UPDATE TRANSACTIONS SET trade = 'closed' where coin = ?"""
sql_all_coins = """SELECT DISTINCT coin FROM TRANSACTIONS """
sql_last_time_closed = """SELECT max(transactTime) FROM TRANSACTIONS WHERE coin = ? AND trade = 'closed' """


def SQLLastTimeClosed(coin):
	cursor.execute(sql_last_time_closed, (coin,))
	transactTime = cursor.fetchall()[0][0]
	return transactTime




def SQLAllCoins():
	coinList = []
	cursor.execute(sql_all_coins)
	ls = cursor.fetchall()
	for coin in ls:
		coinList.append(coin[0])

	return coinList




def SQLPurchasePrice(coin, base):
	cursor.execute(sql_purchase_price, (coin, base))
	result = cursor.fetchall()[0][0]
	return result

# coin = 'OCEAN'
# base = 'USDT'
# print(SQLPurchasePrice(coin, base))

def SQLClosePortfolio(coin):
	cursor.execute(sql_close_portfolio, (coin,))
	connection.commit()


# coin AR | purchasePrice 72.100000 | currentPrice 80.740000 | stopLossTriggerPrice 72.821000 | current ROI 11.980000

def SQLLastTransaction(coin, base, strategy):
	timestamp = hp.TimeStamp()
	cursor.execute(sql_last_transaction, (coin, base, strategy))
	result = cursor.fetchall()
	return result

# print(SQLLastTransaction('BTC', 'BUSD','SHORT'))


def SQLInsertTransaction(coin, base, orderId, transactTime, side, status, price, quantity, strategy):
	timestamp = hp.TimeStamp()
	cursor.execute(sql_insert_transaction, (coin, base, orderId, transactTime, side, status, price, quantity, strategy))
	connection.commit()


coin = 'YFII'
base = 'USDT'
orderId = 745364550
transactTime = '2021-11-04 12:21'
side = 'BUY'
status = 'FILLED'
price = 3958
quantity = 0.256
strategy = 'VORTEX'

# SQLInsertTransaction(coin, base, orderId, transactTime, side, status, price, quantity, strategy) 



# sellOrderId = 3537397800
# sellPrice = 61380
# statusChange = '2021-10-18 16:43'
# buyOrderId = 3536715492


#----------------------------END TRANSACTIONS TABLE------------------------------------







#----------------------------BEGIN BALANCE TABLE------------------------------------
# creating balance table
sql_balance = """CREATE TABLE IF NOT EXISTS
BALANCE(row_id INTEGER PRIMARY KEY, time_ind TEXT, coin TEXT, balance REAL)"""
cursor.execute(sql_balance)

# balance queries
sql_select_balance_time = """SELECT max(time_ind) FROM BALANCE where coin = ?"""
sql_select_last_time = """SELECT MAX(time_ind) FROM BALANCE GROUP BY coin"""
sql_insert_balance = """INSERT INTO BALANCE (time_ind, coin, balance) VALUES (?,?,?)"""



# define balance check

def SQLCheckLastBalanceTime(coin):
	cursor.execute(sql_select_balance_time,(coin,))
	result = cursor.fetchall()[0][0]
	return result


# print(SQLCheckLastBalanceTime('USDC'))
	
def SQLInsertBalance(coin, balance):
	time_ind = hp.TimeStamp()
	cursor.execute(sql_insert_balance, (time_ind, coin, balance))
	connection.commit()

# coin = 'BTC'
# freebalance = 0.003
# lockedbalance = 1.2
# SQLInsertBalance(coin, freebalance, lockedbalance)

#----------------------------END BALANCE TABLE------------------------------------








#----------------------------BEGIN TRADE TABLE------------------------------------

# defining trade status table
sql_init_trade = """CREATE TABLE IF NOT EXISTS
TRADE(trade_id INTEGER PRIMARY KEY, tradestatusconfig_id INTEGER, buyside TEXT, buyorder_id INTEGER, buyprice REAL, sellside TEXT, sellorder_id INTEGER, sellprice REAL, status INTEGER, status_change TEXT,FOREIGN KEY (tradestatusconfig_id) REFERENCES CONFIG(config_id))"""
cursor.execute(sql_init_trade)

# trade queries
sql_select_trade = """SELECT * FROM TRADE"""
sql_insert_trade = """INSERT INTO TRADE (tradestatusconfig_id, buyside, buyorder_id, buyprice, sellside, sellorder_id, sellprice, status, status_change) VALUES (?,?,?,?,?,?,?,?,?)"""
sql_adjust_trade_status = """UPDATE TRADE SET status = ?, status_change = ? WHERE buyorder_id = ? """
sql_get_trade_status = """SELECT status FROM TRADE WHERE buyorder_id = ? """
sql_get_status_change = """SELECT status_change FROM TRADE WHERE buyorder_id = ? """
sql_close_trade = """UPDATE TRADE SET sellside = 'FILLED', sellorder_id = ?, status_change = ?, sellprice = ?, status = 3 WHERE trade_id IN (SELECT max(trade_id) FROM TRADE WHERE tradestatusconfig_id = ? )  """
sql_open_trade = """INSERT INTO TRADE (tradestatusconfig_id, buyside, buyorder_id, buyprice, sellside, sellorder_id, sellprice, status, status_change, quantity) VALUES (?,?,?,?, ?, ?, ?, ?, ?, ?)"""
sql_trade_interval = """SELECT interval FROM CONFIG WHERE config_id in  (SELECT tradestatusconfig_id FROM TRADE WHERE buyorder_id = ?)"""
sql_last_trade = """SELECT * FROM TRADE WHERE trade_id IN (SELECT max(trade_id) FROM TRADE WHERE tradestatusconfig_id = ? ) """
sql_update_last_trade_status = """UPDATE TRADE SET sellorder_id = ?, status = ? WHERE trade_id IN (SELECT max(trade_id) FROM TRADE WHERE tradestatusconfig_id = ? )  """
# buyOrderId = 749057305
def SQLLastTrade(tradeStatusConfigId):
	cursor.execute(sql_last_trade, (tradeStatusConfigId,) )
	result = cursor.fetchall()
	if result == []:
		return result
	else:
		return result[0]


# print(SQLLastTrade(3))


# get status
def SQLGetTradeStatus(buyOrderId):
	cursor.execute(sql_get_trade_status, (buyOrderId,) )
	status = cursor.fetchall()[0][0]
	return status



def SQLUpdateLastTradeStatus(orderId, tradeStatusConfigId, status):
	cursor.execute(sql_update_last_trade_status,(orderId, status, tradeStatusConfigId ) )
	connection.commit()


# SQLUpdateLastTradeStatus(1, 1)

configId = 1
buyOrderId = 749967272
buyPrice = 64566.52
statusChange = '2021-11-12 02:14'
quantity = 0.00047
def SQLOpenTrade(configId, buyOrderId, buyPrice, statusChange, quantity):
	buySide = 'FILLED'
	sellSide = ''
	sellOrderId = 0
	sellPrice = 0
	status = 1
	cursor.execute(sql_open_trade, (configId, buySide, buyOrderId,buyPrice, sellSide, sellOrderId, sellPrice, status, statusChange, quantity) )
	connection.commit()

# SQLOpenTrade(configId, buyOrderId, buyPrice, statusChange, quantity)








# define close trade
def SQLCloseTrade(sellOrderId, transactTime, price, tradeStatusConfig):
	cursor.execute(sql_close_trade,(sellOrderId, transactTime, price, tradeStatusConfig ) )
	connection.commit()

# SQLCloseTrade(752570538, '2021-11-13 15:02', 63917.02000000, 3)


# sellOrderId = 3537397800
# sellPrice = 61380
# statusChange = '2021-10-18 16:43'
# buyOrderId = 3536715492
# SQLCloseTrade(sellOrderId, sellPrice, statusChange, buyOrderId)

# configId = 1
# buyOrderId = 3536715492
# buyPrice = 60193.43
# statusChange = '2021-10-18 15:04'

# def SQLInsertTradestatus()
# test insert balance
# coin = 'BTC'
# timeInterval = 4
# SQLInsertBalance(coin, timeInterval)









# SQLOpenTrade(configId, buyOrderId, buyPrice, statusChange)
#----------------------------END TRADE TABLE------------------------------------


#----------------------------BEGIN PORTFOLIO TABLE------------------------------------
# init vortex database tables
sql_init1 = """CREATE TABLE IF NOT EXISTS
PORTFOLIO(row_id INTEGER PRIMARY KEY, time_ind TEXT, coin TEXT, type TEXT, quantity REAL, base TEXT, status TEXT )"""
cursor.execute(sql_init1)



sql_check_preselection = """SELECT coin FROM PORTFOLIO WHERE type = 'preselection' and base = ? """
sql_check_portfolio = """SELECT coin FROM PORTFOLIO WHERE type = 'portfolio' and base = ?"""
sql_insert_preselection = """INSERT INTO PORTFOLIO (time_ind, coin, type, quantity, base) VALUES (?,?,'preselection', 0.0, ?)"""
sql_insert_portfolio = """INSERT INTO PORTFOLIO (time_ind, coin, type, quantity, base) VALUES (?,?,'portfolio', ?,?)"""

sql_portfolio_coin = """SELECT * FROM PORTFOLIO WHERE type = 'portfolio' and coin = ?"""
sql_del_coin_preselection = """DELETE FROM PORTFOLIO WHERE coin = ? AND type = 'preselection' """
sql_del_coin_portfolio = """DELETE FROM PORTFOLIO WHERE coin = ? AND type = 'portfolio' """
sql_check_purchase = """SELECT price FROM PORTFOLIO WHERE coin = ? AND type = 'preselection' """
sql_check_purchase_time = """SELECT time_ind FROM PORTFOLIO WHERE coin = ? AND type = 'portfolio' """
sql_check_update_portfolio = """UPDATE PORTFOLIO SET quantity = ? WHERE coin = ? and base = ?"""
sql_select_portfolio_status = """SELECT status FROM PORTFOLIO WHERE coin = ? """
sql_update_portfolio_status = """UPDATE PORTFOLIO set status = ? WHERE coin = ? """
sql_select_portfolio_low = """SELECT coin FROM PORTFOLIO WHERE status in (0,1) and base = ? """



def SQLSelectPortfolioLow(base):
	cursor.execute(sql_select_portfolio_low,(base,))
	results = cursor.fetchall()
	return hp.ConvertToList(results)



def SQLCheckPortfolio(base):
	cursor.execute(sql_check_portfolio,(base,))
	results = cursor.fetchall()
	return hp.ConvertToList(results)






def SQLUpdatePortfolio(quantity, coin, base):
	cursor.execute(sql_check_update_portfolio, (quantity, coin, base))
	connection.commit()



# timeInd = '2021-10-31 12:28'
coin = 'OGN'
# quantity = 100
# base = 'BTC'


def SQLPortfolioCoin(coin):
	cursor.execute(sql_portfolio_coin, (coin,))
	results = cursor.fetchall()[0]
	return results





def SQLCheckPreselect(base):
	cursor.execute(sql_check_preselection, (base,))
	results = cursor.fetchall()
	return hp.ConvertToList(results)

# print(SQLCheckPreselect('BUSD'))

def SQLAddToPreselection(timeInd, coin, base):
	cursor.execute(sql_insert_preselection, (timeInd, coin, base))
	connection.commit()


def SQLPortfolioPurchaseTime(coin):
	cursor.execute(sql_check_purchase_time, (coin,))
	results = cursor.fetchall()[0][0]
	return hp.StringToDatetime(results)

# print(type(SQLPortfolioPurchaseTime('AXS')))


def SQLAddToPortfolio(timeInd, coin, quantity, base):
	cursor.execute(sql_insert_portfolio, (timeInd, coin, quantity, base))
	connection.commit()



# SQLAddToPortfolio(timeInd, coin, quantity, base)

# SQLAddToPreselection('2021-10-24 15:40', 'DELTA', 200)
	
def SQLDelCoinPreselect(coin):
	cursor.execute(sql_del_coin_preselection, (coin,))
	connection.commit()


def SQLDelCoinPortfolio(coin):
	cursor.execute(sql_del_coin_portfolio, (coin,))
	connection.commit()

def SQLSelectPortfolioStatus(coin):
	cursor.execute(sql_select_portfolio_status, (coin,))
	result = cursor.fetchall()[0][0]
	if result is None:
		return 0
	else:
		return int(result)

# print(SQLSelectPortfolioStatus('SHIB'))	


def SQLUpdatePortfolioStatus(coin, status):
	try:
		currentStatus = SQLSelectPortfolioStatus(coin)
		if currentStatus <= status:
			cursor.execute(sql_update_portfolio_status, (status, coin))
			connection.commit()

	except:
		print('coin %s not in portfolio' %coin)


# SQLUpdatePortfolioStatus('SHIB', 0)

# print(SQLSelectPortfolioStatus('SHIB'))


#----------------------------END PORTFOLIO TABLE------------------------------------



#----------------------------BEGIN PROFITLEVEL------------------------------------
# init vortex profit level
sql_init_profitlevel = """CREATE TABLE IF NOT EXISTS
PROFITLEVEL(row_id INTEGER PRIMARY KEY, profit REAL, profitStopLoss REAL)"""
cursor.execute(sql_init_profitlevel)

sql_insert_profitlevel = """INSERT INTO PROFITLEVEL (profit, profitStopLoss) VALUES (?,?) """
sql_select_profitlevel = """SELECT max(row_id) FROM PROFITLEVEL WHERE profit <  ?"""
sql_select_profitStopLoss = """SELECT profit, profitStopLoss FROM PROFITLEVEL WHERE row_id = ?"""


def SQLInsertProfitLevel(profit, profitStopLoss):
	cursor.execute(sql_insert_profitlevel, (profit, profitStopLoss))
	connection.commit()

def SQLGetProfitLevelId(ROI):
	cursor.execute(sql_select_profitlevel, (ROI,))
	result = cursor.fetchall()[0][0]
	if isinstance(result, int):
		return result
	else:
		result = 0
		return result

# print(SQLGetProfitLevelId(-2.04))


def SQLGetProfitStopLoss(profitLevelId):
	cursor.execute(sql_select_profitStopLoss, (profitLevelId,))
	if profitLevelId == 0:
		return (0,0)
	else:
		result = cursor.fetchall()[0]
		return result


# def SQLGetCoinProfitLevelID(coin):
# 	cursor.execute(sql_select_profitlevelid, (profit, profitStopLoss))


# def SQLUpdateProfitLevelId(coin, profitLevelId):
# 	cursor.execute(sql_update_profitlevelid, (coin, profitLevelId))
# 	connection.commit()



# # profit = 20
# profitLevel = 0
# print(SQLGetProfitStopLoss(profitLevel))

#----------------------------END PROFITLEVEL------------------------------------



#----------------------------BEGIN VORTEXSIGNAL TABLE------------------------------------
# init vortex database tables
sql_init_vortexsignal = """CREATE TABLE IF NOT EXISTS
VORTEXSIGNAL(row_id INTEGER PRIMARY KEY, coin TEXT, signal TEXT, time_ind TEXT, base TEXT )"""
cursor.execute(sql_init_vortexsignal)



sql_insert_vortexsignal = """INSERT INTO VORTEXSIGNAL (coin, signal, time_ind, base) VALUES (?,?,?,?) """
sql_get_vortexdata = """SELECT coin, signal, time_ind FROM VORTEXSIGNAL WHERE base = ? """

def SQLInsertVortexSignal(coin, signal, base):
	timeInd = hp.TimeStamp()
	cursor.execute(sql_insert_vortexsignal, (coin, signal, timeInd, base))
	connection.commit()


# SQLInsertVortexSignal('HOT', 'rose', 'BTC')
# SQLInsertVortexSignal('HOT', 'rose', 'BUSD')
# SQLInsertVortexSignal('GRT', 'rose', 'BUSD')

def GetVortexData(base, timeLag): #returns the vortex coins that are currently in net rose where the signal is not older dan timelag
	cursor.execute(sql_get_vortexdata, (base,))
	data = cursor.fetchall()
	df = pd.DataFrame(data, columns = ['coin', 'signal', 'timeInd'])
	df['timeInd'] = pd.to_datetime(df['timeInd'], format = '%Y-%m-%d %H:%M')
	# grouped = df.groupby(['coin']).last()
	# df_rose = grouped[grouped['signal'] == 'rose'] #coins in rose
	df_rose = df[df['signal'] == 'rose']
	df_recent = df_rose[df_rose['timeInd'] > datetime.now() - timedelta(hours = timeLag) ]
	result = list(set(df_recent['coin'].values.tolist())) #extract coins and place in unique list
	
	# return list(df_recent.index.values)
	return result


# print(GetVortexData('USDT', 8))


#----------------------------END VORTEXSIGNAL TABLE------------------------------------








#################### FUNCTION DECLARATION #############################
tradestatusconfig_id = 1
buyside = 'FILLED'
buyorder_id = 7889523451
buyprice = 56820.01
sellside = 'OPEN'
sellorder_id = 0
sellprice = 0
status = 1 # 1 is buy order is filled, sell is open. 2: buy is filled, sell is open but in profit. 3: buy and sell are filled
status_change = '2021-10-15 16:12'








def SQLGetStatusChange(buyOrderId):
	cursor.execute(sql_get_status_change, (buyOrderId,) )
	statusChange = cursor.fetchall()[0][0]
	return statusChange

# print(SQLGetStatusChange(7889523451))

# define trade status insert function
def SQLInsertTrade(tradestatusconfig_id, buyside, buyorder_id, buyprice, sellside, sellorder_id, sellprice, status, status_change):
	cursor.execute(sql_insert_trade, (tradestatusconfig_id, buyside, buyorder_id, buyprice, sellside, sellorder_id, sellprice, status, status_change) )
	connection.commit()
# SQLInsertTrade(tradestatusconfig_id, buyside, buyorder_id, buyprice, sellside, sellorder_id, sellprice, status, status_change)

# status = 1
# buyOrderId = 7889523451
# update trade with new status
def SQLUpdateTrade(status, statusChange, buyOrderId):
	cursor.execute(sql_adjust_trade_status, (status, statusChange, buyOrderId) )
	connection.commit()

# SQLUpdateTrade(status, buyOrderId)







# ls_tradeConfig = [{'coin': 'BTC', 'base': 'USDC', 'interval': '15M', 'treshold': [40,2], 'stopLossSettings':[30,0.8,0.2]} \
# 			, {'coin': 'BTC', 'base': 'BUSD', 'interval': '1H', 'treshold': [40,2], 'stopLossSettings':[30,1.5,0.2]} \
# 			 , {'coin': 'BTC', 'base': 'USDT', 'interval': '1M', 'treshold': [20,1], 'stopLossSettings':[30,0.4,0.2]}]






# def SQLInsertBalance(coin, timeInterval):
# 	cursor.execute(sql_select_last_time)
# 	try:
# 		result = cursor.fetchall()[0][0]
# 		lastTime_DT = hp.StringToDatetime(result)

# 		if lastTime_DT + timedelta(hours = timeInterval) < datetime.now():
# 			result = ef.CheckBalanceTotal(coin)
# 			freeBalance = result[0]
# 			lockedBalance = result[1]
# 			timestamp = hp.TimeStamp()
# 			cursor.execute(sql_insert_balance, (timestamp, coin, freeBalance, lockedBalance))
# 			connection.commit()
# 	except:
# 		print('balance is empty')


def GetConfig(configId):
	cursor.execute(sql_select_config, (configId,))
	result = cursor.fetchall()
	return result


def GetTransaction(orderId):
	cursor.execute(sql_lookup_transaction, (orderId,))
	result = cursor.fetchall()
	return result
	




