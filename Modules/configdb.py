# setup config tables in PROTRADER.db
import os, sys
import sqlite3
import helpfunctions as hp
import pandas as pd
from datetime import datetime, timedelta
import dbconnection as con




# define connection and database
connection = con.connection
cursor = connection.cursor()

#----------------------------BEGIN SHORTTRADE TABLE------------------------------------
# creating shorttrade table
sql_create_short_trade_table = """CREATE TABLE IF NOT EXISTS
SHORTTRADE (id INTEGER PRIMARY KEY, symbol TEXT, interval TEXT, sellOrderId INT, sellTransactTime DATE, sellPrice REAL, buyOrderId INT, buyTransactTime DATE, buyPrice REAL, status TEXT, quantity REAL, ocoBuyOrderId INT, stopLimitBuyPerc REAL, stopLimitBuyPrice REAL, stopLimitStatus TEXT)"""



def SQLCreateShortTradeTable():
	cursor.execute(sql_create_short_trade_table)
	connection.commit()

# SQLCreateShortTradeTable()

#----------------------------BEGIN LONGTRADE TABLE------------------------------------
# creating longtrade table
sql_create_long_trade_table = """CREATE TABLE IF NOT EXISTS
LONGTRADE (id INTEGER PRIMARY KEY, symbol TEXT, interval TEXT, buyOrderId INT, buyTransactTime DATE, buyPrice REAL, sellOrderId INT, sellTransactTime DATE, sellPrice REAL, status TEXT, quantity REAL, ocoSellOrderId INT,stopLimitSellPerc REAL, stopLimitSellPrice REAL, stopLimitStatus TEXT)"""



def SQLCreateLongTradeTable():
	cursor.execute(sql_create_long_trade_table)
	connection.commit()

# SQLCreateLongTradeTable()


# insert into trades table
sql_insert_short_trade = """INSERT INTO
SHORTTRADE (symbol, interval, sellOrderId, sellTransactTime, sellPrice, buyOrderId, buyTransactTime, buyPrice, status, quantity,ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
def SQLInsertShortTrade(symbol, interval, sellOrderId, sellTransactTime, sellPrice, buyOrderId, buyTransactTime, buyPrice, status, quantity, ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus):
	cursor.execute(sql_insert_short_trade, (symbol, interval, sellOrderId, sellTransactTime, sellPrice, buyOrderId, buyTransactTime, buyPrice, status, quantity,ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus))
	connection.commit()


symbol = 'XMRBUSD'
interval = '15M'
sellOrderId = 9999
sellTransactTime = hp.TimeStamp()
sellPrice = 26000
buyOrderId = 333
buyTransactTime = hp.TimeStamp()
buyPrice = 0
status = 'FILLED'
quantity = 0.1
stopLimitBuyPrice = 0
stopLimitBuyPerc = 1.5
stopLimitStatus = 'OPEN'
ocoBuyOrderId = 0



# SQLInsertShortTrade(symbol, interval, sellOrderId, sellTransactTime, sellPrice, buyOrderId, buyTransactTime, buyPrice, status, quantity, ocoBuyOrderId, stopLimitBuyPerc, stopLimitBuyPrice, stopLimitStatus)

###################################################
sql_insert_long_trade = """INSERT INTO
LONGTRADE (symbol, interval, buyOrderId, buyTransactTime, buyPrice, sellOrderId, sellTransactTime, sellPrice, status, quantity, ocoSellOrderId, stopLimitSellPerc, stopLimitSellPrice, stopLimitStatus) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
def SQLInsertLongTrade(symbol, interval, buyOrderId, buyTransactTime, buyPrice, sellOrderId, sellTransactTime, sellPrice, status, quantity, ocoSellOrderId, stopLimitSellPerc, stopLimitSellPrice, stopLimitStatus):
	cursor.execute(sql_insert_long_trade, (symbol, interval, buyOrderId, buyTransactTime, buyPrice, sellOrderId, sellTransactTime, sellPrice, status, quantity,ocoSellOrderId, stopLimitSellPerc, stopLimitSellPrice, stopLimitStatus))
	connection.commit()


symbol = 'BTCUSDT'
interval = '15M'
sellOrderId = 9999
buyOrderId = 333
buyTransactTime = hp.TimeStamp()
buyPrice = 2000
sellTransactTime = ''
sellPrice = 4000
status = 'FILLED'
quantity = 0.1
stopLimitSellPrice = 0
stopLimitSellPerc = 2.5
stopLimitStatus = 'OPEN'
ocoSellOrderId = 0



# SQLInsertLongTrade(symbol, interval, buyOrderId, buyTransactTime, buyPrice, sellOrderId, sellTransactTime, sellPrice, status, quantity, ocoSellOrderId, stopLimitSellPerc, stopLimitSellPrice, stopLimitStatus)

###################################################
# lookup last control flow
sql_lookup_last_short_transaction = """SELECT status
FROM SHORTTRADE
WHERE sellTransactTime in 
    (
        SELECT MAX(sellTransactTime)
        FROM SHORTTRADE
    )"""

def SQLLookupLastShortTransaction():
	cursor.execute(sql_lookup_last_short_transaction)
	status = cursor.fetchall()
	if len(status) > 0: 
		return status[0][0]
	print('error, no transactions found')


###################################################
# lookup last control flow
sql_lookup_last_long_transaction = """SELECT status
FROM LONGTRADE
WHERE buyTransactTime in 
    (
        SELECT MAX(buyTransactTime)
        FROM LONGTRADE
    )"""

def SQLLookupLastLongTransaction():
	cursor.execute(sql_lookup_last_long_transaction)
	status = cursor.fetchall()
	if len(status) > 0: 
		return status[0][0]
	print('error, no transactions found')


##################################################


# lookup last buyPrice 
sql_lookup_buyPrice = """SELECT buyPrice
FROM SHORTTRADE
WHERE buyTransactTime in 
    (
        SELECT MAX(buyTransactTime)
        FROM SHORTTRADE
    )"""

def SQLLookupBuyPrice():
	cursor.execute(sql_lookup_buyPrice)
	result = cursor.fetchall()
	if len(result) > 0: 
		return result[0][0]
	print('error no buy price')

# print(SQLLookupBuyPrice())

##################################################


# set control flow of last order
# sql_set_control_flow = """UPDATE TRADES 
# SET controlFlow = ?
# WHERE id in (
#                 SELECT id
#                 FROM TRADES 
#                 WHERE transactTime in (
#                                         SELECT max(transactTime) FROM TRADES
#                                       )
#             )"""

# def SQLSetControlFlow(flow):
# 	cursor.execute(sql_set_control_flow, (flow,))
# 	connection.commit()

##################################################


# get prices of last short trade
# sql_get_prices = """SELECT sellPrice, buyPrice 
# FROM SHORTTRADE WHERE sellTransactTime IN (
# SELECT MAX(sellTransactTime)
# FROM SHORTTRADE
# ) """

# def SQLGetPrices():
# 	cursor.execute(sql_get_prices)
# 	result = cursor.fetchall()
# 	if len(result) == 1:
# 		return result[0]
# 	else:
# 		print('error no prices found')


# print(SQLGetPrices())



##################################################


# get prices of last short trade
# sql_get_short_prices = """SELECT sellPrice, buyPrice 
# FROM SHORTTRADE WHERE sellTransactTime IN (
# SELECT MAX(sellTransactTime)
# FROM SHORTTRADE
# ) """

# def SQLGetShortPrices():
# 	cursor.execute(sql_get_short_prices)
# 	result = cursor.fetchall()
# 	if len(result) == 1:
# 		return result[0]
# 	else:
# 		print('error no prices found')

# print(SQLGetShortPrices())



##################################################


# get prices of last long trade
# sql_get_long_prices = """SELECT sellPrice, buyPrice 
# FROM LONGTRADE WHERE buyTransactTime IN (
# SELECT MAX(buyTransactTime)
# FROM LONGTRADE
# ) """

# def SQLGetLongPrices():
# 	cursor.execute(sql_get_long_prices)
# 	result = cursor.fetchall()
# 	if len(result) == 1:
# 		return result[0]
# 	else:
# 		print('error no prices found')

# print(SQLGetLongPrices())

##################################################

buyOrderId = 333
buyTransactTime = hp.TimeStamp()
buyPrice = 2000
status = 'FILLED'
quantity = 0.1

# buy back after sell
sql_update_buy_back = """UPDATE shorttrade SET buyOrderId = ?, buyTransactTime = ?, buyPrice = ?, status = ? 
where sellTransactTime IN (SELECT MAX(sellTransactTime) FROM SHORTTRADE) """

def SQLUpdateBuyBack(buyOrderId, buyTransactTime, buyPrice, status):
	cursor.execute(sql_update_buy_back, (buyOrderId, buyTransactTime, buyPrice, status))
	connection.commit()


# SQLUpdateBuyBack(buyOrderId, buyTransactTime, buyPrice, status)


##################################################

sellOrderId = 333
sellTransactTime = hp.TimeStamp()
sellPrice = 2025
status = 'FILLED'
quantity = 0.1

# buy back after sell
sql_update_sell_back = """UPDATE LONGTRADE SET sellOrderId = ?, sellTransactTime = ?, sellPrice = ?, status = ? 
where buyTransactTime IN (SELECT MAX(buyTransactTime) FROM LONGTRADE) """

def SQLUpdateSellBack(sellOrderId, sellTransactTime, sellPrice, status):
	cursor.execute(sql_update_sell_back, (sellOrderId, sellTransactTime, sellPrice, status))
	connection.commit()

# SQLUpdateSellBack(sellOrderId, sellTransactTime, sellPrice, status)

##################################################


# buy back after sell
sql_last_short_transaction = """SELECT buyPrice, sellPrice, quantity, status, stopLimitStatus, buyOrderId, ocoBuyOrderId
FROM SHORTTRADE 
WHERE sellTransactTime IN (
SELECT MAX(sellTransactTime)
FROM SHORTTRADE WHERE symbol = ?
) """

def SQLLastShortTransaction(symbol):
	cursor.execute(sql_last_short_transaction,(symbol,))
	result = cursor.fetchall()
	if len(result) == 1:
		return result[0]
	else:
		# print('no last order found for this symbol')
		return False



# print(SQLLastShortTransaction('XMRBUSD'))
##################################################


sql_last_long_transaction = """SELECT buyPrice, sellPrice, quantity, status, stopLimitStatus, sellOrderId, ocoSellOrderId 
FROM LONGTRADE WHERE buyTransactTime IN (
SELECT MAX(buyTransactTime)
FROM LONGTRADE WHERE symbol = ?
) """

def SQLLastLongTransaction(symbol):
	cursor.execute(sql_last_long_transaction, (symbol,))
	result = cursor.fetchall()
	if len(result) == 1:
		return result[0]
	else:
		# print('no last order found for this symbol')
		return False

# print(SQLLastLongTransaction('BTCUSDT'))



#----------------------------BEGIN BALANCE TABLE------------------------------------
# creating balance table
sql_create_balance_table = """CREATE TABLE IF NOT EXISTS
BALANCE (id INTEGER PRIMARY KEY, symbol TEXT, measure_time DATE, coin_quantity REAL, base_quantity REAL, dollar_value INT)"""


def SQLCreateBalanceTable():
	cursor.execute(sql_create_balance_table)
	connection.commit()

# SQLCreateBalanceTable()


# insert into trades table
sql_insert_balance_table = """INSERT INTO
BALANCE (symbol, measure_time, coin_quantity, base_quantity, dollar_value) VALUES (?,?,?,?,?)"""
def SQLInsertBalance(symbol, measure_time, coin_quantity, base_quantity, dollar_value):
	cursor.execute(sql_insert_balance_table, (symbol, measure_time, coin_quantity, base_quantity, dollar_value))
	connection.commit()


symbol = 'BTCUSDT'
measure_time = hp.StringToDatetime(hp.TimeStamp())
coin_quantity = 23
base_quantity = 21
dollar_value = 224
# SQLInsertBalance(symbol, measure_time, coin_quantity, base_quantity, dollar_value)


sql_last_balance = """SELECT * FROM BALANCE WHERE measure_time IN (SELECT MAX(measure_time) 
FROM BALANCE)"""
def SQLLastBalance():
	cursor.execute(sql_last_balance)
	result = cursor.fetchall()
	if len(result)>0:
		return result[0]
	else:
		return 'empty balance'





# close buy OCO
sql_close_buy_oco = """UPDATE SHORTTRADE SET stopLimitStatus = ?, status = 'FILLED'
WHERE sellTransactTime IN (SELECT sellTransactTime FROM SHORTTRADE WHERE symbol = ?)"""
def SQLCloseBuyOCO(symbol, status):
	cursor.execute(sql_close_buy_oco, (status, symbol))
	connection.commit()

# SQLCloseBuyOCO('XMRBUSD')

sql_close_sell_oco = """UPDATE LONGTRADE SET stopLimitStatus = ?, status = 'FILLED' 
WHERE buyTransactTime IN (SELECT buyTransactTime FROM LONGTRADE WHERE symbol = ?)"""
def SQLCloseSellOCO(symbol, status):
	cursor.execute(sql_close_sell_oco, (status, symbol))
	connection.commit()


# symbol = 'XMRBUSD'
# ocoSellOrderId = 130701594
# SQLCloseSellOCO(symbol, status)



