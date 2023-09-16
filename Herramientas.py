# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 17:56:14 2021

@author: Metsis
"""
import datetime
import variables as var
   
def TimeStamp_to_date_hour(timestamp):
    format = "%d/%m/%y %H:%M:%S"
    fecha =  datetime.datetime.fromtimestamp(timestamp/1000)
    fecha = fecha.strftime(format)
    return fecha

def TimeStamp_to_date(timestamp):
    format = "%d/%m/%y"
    fecha =  datetime.datetime.fromtimestamp(timestamp/1000)
    fecha = fecha.strftime(format)
    return fecha

def TimeStamp_to_hour(timestamp):
    format = "%H:%M:%S"
    hour =  datetime.datetime.fromtimestamp(timestamp/1000)
    hour = hour.strftime(format)
    return hour

def calc_decimals(numero):
    #Calcula el numero de decimales que tiene un par
    numero = str(numero)
    if numero.find(".") == -1:
        return 0
    LenDecimal = len(numero) - numero.find(".") - 1
    return LenDecimal

def calc_quantity(symbol, act_price, balance):
    amount = balance / act_price
    amount = round(amount,int(var.symbols_info[symbol]['minQty'] ))
    return amount