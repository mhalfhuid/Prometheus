# setup config tables in monitor.db
import os, sys
import sqlite3
import helpfunctions as hp
import pandas as pd
from datetime import datetime, timedelta
import dbconnection as con




# define connection and database
connection = con.connection
cursor = connection.cursor()

#----------------------------BEGIN ORDERS TABLE------------------------------------
# creating config table
sql_config = """CREATE TABLE IF NOT EXISTS
ORDERS(id INTEGER PRIMARY KEY, symbol TEXT, orderId INT, transactTime TEXT, price REAL, quantity REAL, status TEXT, side TEXT)"""
cursor.execute(sql_config)

sql_insert_order = """INSERT INTO ORDERS (symbol, orderId, transactTime, price, quantity, status, side) VALUES (?,?,?,?,?,?,?)"""
def SQLInsertOrder(symbol, orderId, transactTime, price, quantity, status, side):
	# time_ind = hp.TimeStamp()
	cursor.execute(sql_insert_order, (symbol, orderId, transactTime, price, quantity, status, side))
	connection.commit()

# SQLInsertOrder('ETHUSDC', 688725808, '2022-05-21 01:00', 2050, 26.0, 'NEW', 'BUY')

# truncating order table
sql_truncate = """DELETE FROM ORDERS"""
def SQLTruncateOrderTable():
	cursor.execute(sql_truncate)
	connection.commit()




# select all orders
sql_select_order = """SELECT * FROM ORDERS"""
def SQLSelectOrder():
	cursor.execute(sql_select_order)
	ls = cursor.fetchall()
	return ls

# check specific order
sql_select_orderid = """SELECT * FROM ORDERS WHERE orderId = ?"""
def SQLSelectOrderId(orderId):
	orderId = int(orderId)
	cursor.execute(sql_select_orderid, (orderId,))
	ls = cursor.fetchall()
	return ls


sql_select_vw_order = """SELECT * FROM VW_ORDERS"""
def SQLSelectVWOrder():
	cursor.execute(sql_select_vw_order)
	ls = cursor.fetchall()
	return ls

# update order status
sql_update_order_status =  """UPDATE ORDERS SET status = ? WHERE orderId = ? """
def SQLUpdateOrderStatus(status, orderId):
	cursor.execute(sql_update_order_status, (status, orderId))
	connection.commit()


# SQLUpdateOrderStatus('FILLED', 688725910.0000000)

# delete order
sql_delete_order = """DELETE FROM ORDERS WHERE orderId = ?"""
def SQLDeleteOrder(orderId):
	cursor.execute(sql_delete_order, (orderId,))
	connection.commit()
	

#----------------------------BEGIN BALANCE TABLE------------------------------------
# creating config table
sql_create_balance = """CREATE TABLE IF NOT EXISTS
BALANCE(id INTEGER PRIMARY KEY, strategy TEXT, symbol TEXT, balanceTime TEXT, usd_balance REAL)"""
cursor.execute(sql_create_balance)
connection.commit()



sql_insert_balance = """INSERT INTO BALANCE (strategy, symbol,balanceTime, usd_balance) VALUES (?,?,?,?)"""
def SQLInsertBalance(strategy, symbol, balanceTime, usd_balance):
	cursor.execute(sql_insert_balance, (strategy, symbol, balanceTime, usd_balance))
	connection.commit()


sql_last_balance = """SELECT MAX(DATETIME(balanceTime)) FROM BALANCE"""
def SQLLastBalance():
	cursor.execute(sql_last_balance)
	result = cursor.fetchall()
	if result[0][0] != None:
		return result[0][0]
	else: 
		return None

# print(SQLLastBalance())
#----------------------------BEGIN TRADE TABLE------------------------------------

# defining trade status table
# sql_init_trade = """CREATE TABLE IF NOT EXISTS
# TRADES(id INTEGER PRIMARY KEY, symbol TEXT, orderId INT, transactTime TEXT, price REAL, quantity REAL, status TEXT, side TEXT)"""
# cursor.execute(sql_init_trade)

# # trade queries
# # sql_select_trade = """SELECT * FROM TRADE"""
# sql_insert_trade = """INSERT INTO TRADES (symbol, orderId, transactTime, price, quantity,status, side) VALUES (?,?,?,?,?)"""
# def SQLInsertTrade(symbol, orderId, transactTime, price, quantity,status, side):
# 	cursor.execute(sql_insert_order, (symbol, orderId, transactTime, price, quantity,status, side))
# 	connection.commit()
# sql_adjust_trade_status = """UPDATE TRADE SET status = ?, status_change = ? WHERE buyorder_id = ? """
# sql_get_trade_status = """SELECT status FROM TRADE WHERE buyorder_id = ? """
# sql_get_status_change = """SELECT status_change FROM TRADE WHERE buyorder_id = ? """
# sql_close_trade = """UPDATE TRADE SET sellside = 'FILLED', sellorder_id = ?, status_change = ?, sellprice = ?, status = 3 WHERE trade_id IN (SELECT max(trade_id) FROM TRADE WHERE tradestatusconfig_id = ? )  """
# sql_open_trade = """INSERT INTO TRADE (tradestatusconfig_id, buyside, buyorder_id, buyprice, sellside, sellorder_id, sellprice, status, status_change, quantity) VALUES (?,?,?,?, ?, ?, ?, ?, ?, ?)"""
# sql_trade_interval = """SELECT interval FROM CONFIG WHERE config_id in  (SELECT tradestatusconfig_id FROM TRADE WHERE buyorder_id = ?)"""
# sql_last_trade = """SELECT * FROM TRADE WHERE trade_id IN (SELECT max(trade_id) FROM TRADE WHERE tradestatusconfig_id = ? ) """
# sql_update_last_trade_status = """UPDATE TRADE SET sellorder_id = ?, status = ? WHERE trade_id IN (SELECT max(trade_id) FROM TRADE WHERE tradestatusconfig_id = ? )  """
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


# define close trade
def SQLCloseTrade(sellOrderId, transactTime, price, tradeStatusConfig):
	cursor.execute(sql_close_trade,(sellOrderId, transactTime, price, tradeStatusConfig ) )
	connection.commit()


#----------------------------END TRADE TABLE------------------------------------



	
