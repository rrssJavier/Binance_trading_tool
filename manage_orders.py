# -*- coding: utf-8 -*-
"""
Created on Mon May 10 06:08:36 2021

@author: Metsis
"""
import variables as var
from random import randint
import time

import api_bridge
import Herramientas

def new_order_now(symbol, side, tp_price, sl_price):
    client_id = time.time()
    the_price = var.mark_prices[symbol]
    min_qty= int(var.symbols_info[symbol]['minQty'])-1
    tick_size= int(var.symbols_info[symbol]['tickSize'])
    mybalance = api_bridge.future_account_balance('USDT') 
    print(symbol, side, tp_price, sl_price)
    amount = (mybalance * var.balance_trade) / sl_price
    amount = round(amount,min_qty)
    
    if side == "BUY":
        price = the_price +(the_price*0.004)
        stop_price= the_price +(the_price*0.002)
    elif side == "SELL":
        price = the_price -(the_price*0.004)
        stop_price= the_price -(the_price*0.002)
    price = round(price,tick_size)
    stop_price = round(stop_price, tick_size)
    params = {
        "symbol": symbol,
        "side": side,
        "type": "STOP",
        "timeInForce": "GTC",
        "quantity": amount,
        "price": price,
        'stopPrice': stop_price,
        "newClientOrderId":client_id}
    print(params)
    response = api_bridge.send_signed_request('POST', '/fapi/v1/order', params)
    return response

def setup_tp_sl(symbol, side, quantity, client_id, take_profit, stop_lose ):
    '''==========================SL================================'''
    side_close_p = 'BUY' if side == 'SELL' else 'SELL'
    params_sl = {
    "symbol": symbol,
    "side": side_close_p,
    "type": "STOP_MARKET",
    "timeInForce": "GTC",
    "quantity": quantity,
    "stopPrice": stop_lose,
    "reduceOnly": "True",
    "priceProtect": "True",
    "workingType": 'MARK_PRICE',
    "newClientOrderId":f'{client_id}SL'}
    response={}
    response['sl_order']  = api_bridge.send_signed_request('POST', '/fapi/v1/order', params_sl)
    
    '''==========================TP================================''' 
    params_tp = {
    "symbol": symbol,
    "side": side_close_p,
    "type": "TAKE_PROFIT_MARKET",
    "timeInForce": "GTC",
    "quantity": quantity,
    "stopPrice": take_profit,
    "reduceOnly": "True",
    "priceProtect": "True",
    "workingType": 'MARK_PRICE',
    "newClientOrderId":f'{client_id}TP'}

    response['tp_order']  = api_bridge.send_signed_request('POST', '/fapi/v1/order', params_tp)
    return response