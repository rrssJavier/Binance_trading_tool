# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 17:35:17 2021

@author: Metsis
"""

import hmac
import time
import hashlib
import requests
import json
from urllib.parse import urlencode
import privateconfig, Herramientas
import variables as var

KEY = privateconfig.p_api_key
SECRET = privateconfig.p_secret_key
BASE_URL =  privateconfig.url


''' ======  begin of functions, you don't need to touch ====== '''
def hashing(query_string):
    return hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), 
                    hashlib.sha256).hexdigest()

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
    query_string = urlencode(payload)
    # replace single quote to double quote
    query_string = query_string.replace('%27', '%22')
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    url = BASE_URL + url_path + '?' + query_string + '&signature=' \
        + hashing(query_string)
    #print("{} {}".format(http_method, url))
    params = {'url': url, 'params': {}}
    response = dispatch_request(http_method)(**params)
    return response.json()

# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + '?' + query_string
    #print("{}".format(url))
    response = dispatch_request('GET')(url=url)
    return response.json()
''' ===========================  end of functions ======================================= '''

'''================================API FUNCTIONS============================'''

        
def current_all_open_orders():
    openoreders = send_signed_request('GET', '/fapi/v1/openOrders')
    return openoreders

def position_information(symbol):
    positions = send_signed_request('GET', '/fapi/v2/positionRisk',
                                               symbol)
    return positions

def cancel_order(symbol,OrderId):
    params = {
    "symbol": symbol,
    "ClientOrderId": OrderId}
    response = send_signed_request('DELETE', '/fapi/v1/order', params)
    return response

def future_account_balance(coin):
    print('------------', coin)
    response = send_signed_request('GET', '/fapi/v2/balance')
    print('=======',response,'==========')
    for i in range(len(response)):
        if response[i]['asset']== coin:
            var.balance = round(float(response[i]['balance']), 2)
            return var.balance 
        
def symbol_price_ticker(symbol):
    price = send_public_request('/fapi/v1/ticker/price' , {"symbol": symbol }) # return a diccionary
    price = float(price["price"])                                                     #take only the value "price
    return price

def kline_candlestick_data(symbol, interval, limit):
    params = {
    "symbol": symbol,
    "interval": interval,
    'limit':limit+1} 
    candels = send_public_request('/fapi/v1/klines', params)
    candels.pop()
    return candels

def exchange_info():
    response = send_public_request('/fapi/v1/exchangeInfo')
    return response

def new_listen_key():
    response = send_signed_request('POST', '/fapi/v1/listenKey')
    return response
    
'''========================================================================='''

def new_order_now(symbol, side, tp_price, sl_price):
    client_id = time.time()
    min_qty= int(var.symbols_info[symbol]['minQty'])-1
    mybalance = future_account_balance('USDT') 
    amount = (mybalance * var.balance_trade) / sl_price
    amount = round(amount,min_qty)
    
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": amount,
        "newClientOrderId":client_id}
    response = send_signed_request('POST', '/fapi/v1/order', params)
    print('++++++++++',params,'--------', response)
    return response

def setup_tp_sl(symbol, side, quantity, client_id, take_profit, stop_lose ):

    VarSLTP=float(var.symbols_info[var.symbol]["tick"])*10
    if side == 'SELL':
        side_close_p = 'BUY'
        priceSL = round(float(stop_lose)+VarSLTP, var.symbols_info[var.symbol]["tickSize"])
        priceTP = round(float(take_profit)-VarSLTP, var.symbols_info[var.symbol]["tickSize"])
    else:
        side_close_p = 'SELL'
        priceSL = round(float(stop_lose)-VarSLTP, var.symbols_info[var.symbol]["tickSize"])
        priceTP = round(float(take_profit)+VarSLTP, var.symbols_info[var.symbol]["tickSize"])

    '''==========================SL================================'''
    params_sl = {
    "symbol": symbol,
    "side": side_close_p, 
    "type": "STOP",
    "timeInForce": "GTC",
    "quantity": quantity,
    "price": priceSL,
    "stopPrice": stop_lose,
    "reduceOnly": "True",
    "priceProtect": "True",
    "workingType": 'MARK_PRICE',
    "newClientOrderId":f'{client_id}-SL'}
    response={}
    response['sl_order']  = send_signed_request('POST', '/fapi/v1/order', params_sl)
    print('==========================SL', params_sl, '================================', response)
    '''==========================TP================================''' 
    params_tp = {
    "symbol": symbol,
    "side": side_close_p,
    "type": "TAKE_PROFIT",
    "timeInForce": "GTC",
    "quantity": quantity,
    "price": priceTP,
    "stopPrice": take_profit,
    "reduceOnly": "True",
    "priceProtect": "True",
    "workingType": 'MARK_PRICE',
    "newClientOrderId":f'{client_id}-TP'}

    response['tp_order']= send_signed_request('POST', '/fapi/v1/order', params_tp)
    print('==========================tp', params_tp, '================================', response)

    #return response
       

