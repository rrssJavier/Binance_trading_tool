# -*- coding: utf-8 -*-
"""
Created on Mon May 10 03:49:53 2021

@author: Metsis
"""
#Variables confiuradas

sl_max=0.01
tp_max=0.03
len_hist_candle= 10
#NvelasPromedio=12

#variables calculadas
hist_candles = []
tendencia=''
balance=0
minQty=0      #decimales que tiene la orden minima ej: 3 decimales 0,001 BTC
pricePrecision=0 # decimales del market price ej: BTC a 55700,34 pricePrecision = 2

#variables de operaciones
sl_price=0
tp_price=0
balance_trade = 0.98 #porcentaje del capital en cada trade
interval='3m'
symbol=''
symbols_info={}
mark_prices = {}
