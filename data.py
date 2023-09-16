# -*- coding: utf-8 -*-
"""
Created on Thu May  6 09:41:23 2021

@author: Metsis-white
"""
import websocket, json, datetime
import Herramientas, api_bridge
import variables as var
import os
    
def historical_data(symbol,interval,how_long):
    hist_candles_list = api_bridge.kline_candlestick_data(symbol, interval, how_long)
    temp_list=[]
    for i in range(how_long):
        temp_list.append({
            'symbol':symbol,
            'interval':interval,
            'kline_start_time':hist_candles_list[i][0],
            'Quote_asset_volume':float(hist_candles_list[i][7]),
            'open_price':float(hist_candles_list[i][1]),
            'close_price':float(hist_candles_list[i][4]),
            'high_price':float(hist_candles_list[i][2]),
            'low_price':float(hist_candles_list[i][3])})
    return temp_list
        
def incoming_data(message):
    #print(message,'-----------')
       
    if 'data' in message:
        message = message['data']
    
    if not 'e' in message:
        return ['None','None']  
    
    event_type = message['e']
    
    if event_type == 'listenKeyExpired':
        return ['None','None'] 
    
    if event_type == 'ACCOUNT_UPDATE':
        return ['None','None'] 

    if event_type =='ORDER_TRADE_UPDATE':
        print("------------FILLED--------------------", message, '---------------------')
        save_stream_on_txt('ORDER_TRADE_UPDATE.txt',message)#provisional
        
        if message['o']['x']=="NEW":
            if message['o']['c'][-3]!='-':
                save_order(message)
            
        elif message['o']['X']=="FILLED":
            
            if message['o']['c'][-3]!='-':
                info= read_order(message['o']['c'])
                print("------------reading--------------------", info, '---------------------')

                api_bridge.setup_tp_sl(info['symbol'], info['side'], 
                                       info['quantity'], info['client_id'], 
                                       info['tp'], info['sl'])
            
        return ['ORDER_TRADE_UPDATE','None']
    
    #pendiente al agregar mas streams, todos tienen que tener 'symbol en message['s']
    #print('oooooooooooooooooooooooooo',message,'oooooooooooooooooooooooooo'
    _symbol =  message['s']
    if  _symbol != var.symbol :
        return ['None','None']  
    
    #Actualizacion de precio 
    elif event_type == 'markPriceUpdate':
        price = message['p']
        price = round(float(price),var.pricePrecision)
        var.mark_prices[_symbol] = price
        return ['markPriceUpdate',price]
    
    #New candel    
    elif event_type == 'kline':
        if var.interval != message['k']['i']:
             return ['None','None']
        if message['k']['x'] == True:
            return process_kline(message)
        return ['None','None'] #ya que la vela no ha cerrado se manda None para que sea ignorado
    else:
        #print('+++++++++++++++++++',message,'++++++++++++++++++++++++')
        save_stream_on_txt('fails_streams.txt',message)
        return ['None','None'] # no se reconoce el strem asi que se ignora  
    
def read_order(file):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, f'trades/{file}.txt')
    lee = open(filename,'r')
    json_lee= lee.read()
    info = json.loads(json_lee)
    lee.close()
    return info
    
def save_order(message):
    dict_to_save= {'symbol':message['o']['s'],'time':message['T'],
                   'client_id':message['o']['c'],'side':message['o']['S'],
                   'quantity':message['o']['q'],'sl':var.sl_price,
                   'tp':var.tp_price} 
    cliente_id = message['o']['c']
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, f'trades\{cliente_id}.txt')
    save_stream_on_txt(filename,dict_to_save,False)

def process_kline(message):
    kline_dict = {
        'symbol':  message['s'],   
        'kline_start_time': message['k']['t'],
        'interval': message['k']['i'],
        'Quote_asset_volume':float(message['k']['q']),
        'open_price': float(message['k']['o']),
        'close_price': float(message['k']['c']),
        'high_price': float(message['k']['h']),
        'low_price': float(message['k']['l'])} 
    new_candle(kline_dict)
    salida = ['kline','none']
    return salida
    
def new_candle(kline_dict):
    if len(var.hist_candles) == (var.len_hist_candle):
        var.hist_candles.append(kline_dict)
        var.hist_candles.pop(0)  
    else:
        var.hist_candles = historical_data(var.symbol,var.interval,
                                           var.len_hist_candle)
        for i in range(len(var.hist_candles)):
            print('>>>>>>>', var.hist_candles[i]['high_price'],'<<<<<<<<<')
        print('_____________________________________________')   
def load_symbols_info():
    lee = open('my_symbols_info.txt','r')
    json_lee= lee.read()
    var.symbols_info = json.loads(json_lee)
    lee.close()
    
def save_stream_on_txt(file,stream,log=True):
    
    x = datetime.datetime.now()
    stream = json.dumps(stream)
    _file = open(file,'a')
    if log == True:
        _file.write(x.strftime("%b %d %Y %H:%M:%S")+ '\n' + stream + '\n\n')
    else:
        _file.write(stream)
        
    _file.close()
    
def make_my_symbol_info():
    all_info = api_bridge.exchange_info()
    list_info_symbols= all_info["symbols"]
    dict_symbols={}
    for x in list_info_symbols:
        # tickSize minima unidad que puede subir o bajar el precio
        tick = x['filters'][0]['tickSize']
        tick_size = x['filters'][0]['tickSize']
        tick_size= tick_size.find("1") - 1
        # minima unidad que se puede comprar
        min_qty=  x['filters'][1]['minQty']
        if min_qty.find(".") == -1:
            min_qty= 0
        else:
            min_qty=len(min_qty)-2
        # pricePrecision cantidad de decimales que tiene el precio
        temp_dict= {'pricePrecision':x['pricePrecision'],'tickSize':tick_size,
                    'minQty':min_qty,'tick':tick}
        dict_symbols[x['symbol']]=temp_dict
    
    keys = dict_symbols.keys()
    sorted_keys = sorted(keys)
    sorted_dict_symbols = {}
    for key in sorted_keys:
      if key[-4:] == 'USDT':
          sorted_dict_symbols[key] = dict_symbols[key]
  
    stream = json.dumps(sorted_dict_symbols)
    _file = open('my_symbols_info.txt','w')
    _file.write(stream)
    _file.close()