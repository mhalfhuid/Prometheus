import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

""" This is a very simple script working on Binance API

- work with USER_DATA endpoint with no third party dependency
- work with testnet

Provide the API key and secret, and it's ready to go

Because USER_DATA endpoints require signature:
- call `send_signed_request` for USER_DATA endpoints
- call `send_public_request` for public endpoints

```python

python spot.py

```

"""
# TradingBot API KEYS
# KEY = 'iodryFi60y9K4S4m8P6xqJ3t91sJhlHQRPWm5MyOa4jgPxDPEaiHyzvaDamXBz4s'
# SECRET = 'vpmM768tbDCuokAAbt5dnvTXjGxf7SUtpB1pJ8SugK4bcgupmh7J2d7JHxNp5g6P'
KEY = 'XnVAJk0r8CM28V1OjbNQlzPOK9ZUkl4jzvyceeiU2MLJeW79gQRtSu39BV0Fl68C'
SECRET = 'vBRReeY495Zs0SLukeiuvDAOM7fU2GlOUfTXDTjGvpjQ76IztS3Dy8xoYHSpL19T'
BASE_URL = 'https://api.binance.com' # production base url
# BASE_URL = 'https://testnet.binance.vision' # testnet base url

''' ======  begin of functions, you don't need to touch ====== '''
def hashing(query_string):
    return hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json;charset=utf-8',
        'X-MBX-APIKEY': KEY
    })
    return {
        'GET': session.get,
        'DELETE': session.delete,
        'PUT': session.put,
        'POST': session.post,
    }.get(http_method, 'GET')

# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    url = BASE_URL + url_path + '?' + query_string + '&signature=' + hashing(query_string)
    print("{} {}".format(http_method, url))
    params = {'url': url, 'params': {}}
    response = dispatch_request(http_method)(**params)
    return response.json()

# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + '?' + query_string
    print("{}".format(url))
    response = dispatch_request('GET')(url=url)
    return response.json()

''' ======  end of functions ====== '''

### public data endpoint, call send_public_request #####
# get klines
# response = send_public_request('/api/v3/klines' , {"symbol": "BTCUSDT", "interval": "1d"})
# print(response)


### USER_DATA endpoints, call send_signed_request #####
# get account informtion
# if you can see the account details, then the API key/secret is correct
# response = send_signed_request('GET', '/api/v3/account')
# print(response['makerCommission'])
# print(response['balances']['asset'] = 'BNB')
# ls = [x for x in ls if x[0] != c] 

# def CheckBalance(c):
#     balanceData = [x for x in response['balances'] if x['asset'] == c.upper()]
#     return balanceData

# print (CheckBalance('usdt'))


# [{'asset': 'BTC', 'free': '0.01746090', 'locked': '0.00562300'}, {'asset': 'LTC', 'free': '0.36107000',
#
# # place an order
# if you see order response, then the parameters setting is correct
params = {
    "symbol": "BNBUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": 1,
    "price": "201"
}





# response = send_signed_request('POST', '/api/v3/order', params)
# print(response)


# def SimpleBuy(c, a):
#     coin = c
#     amount = a
#     timestamp = hp.TimeStamp()
#     print('%s: buying %s USD of %s coin' %(timestamp, round(amount,4), coin.upper()))


# def SimpleSell(c, a):
#     coin = c
#     amount = a
#     timestamp = hp.TimeStamp()
#     print('%s: selling %s USD of %s coin' %(timestamp, round(amount,4), coin.upper()))







# User Universal Transfer
# params = {
#     "type": "MAIN_MARGIN",
#     "asset": "USDT",
#     "amount": "0.1"
# }
# response = send_signed_request('POST', ' /sapi/v1/asset/transfer', params)
# print(response)


# New Future Account Transfer (FUTURES)
# params = {
#     "asset": "USDT",
#     "amount": 0.01,
#     "type": 2
# }
# response = send_signed_request('POST', '/sapi/v1/futures/transfer', params)
# print(response)