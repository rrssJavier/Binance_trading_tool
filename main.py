<<<<<<< HEAD
from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import websocket
import json
import time
from PyQt5.QtCore import *

import data
import api_bridge
import manage_orders
import privateconfig
import variables as var
from gui_ppal import *

operation_side='BUY'

class VentanaPrincipal (QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def closeEvent(self, event):
        websocket_manager.stop_manager_with_all_streams()       
        worker.terminate()
        
'''=======================Acceso a data================================'''

class WorkerThread (QThread):
    def run (self):
        while True:
            oldest_stream_data_stream_buffer = \
                websocket_manager.pop_stream_data_from_stream_buffer()
            if oldest_stream_data_stream_buffer is False:
                time.sleep(0.01)
            else:
                info = data.incoming_data(oldest_stream_data_stream_buffer)
                process_data(info)

def process_data(info):
    if info[0] == "markPriceUpdate":
        ventana.label_price.setText(str(info[1]))

def act_tp_sl():

    '''busca el valor del SL deseado'''
    sl_candel= int("-" + ventana.comboBox_sl.currentText())
    if ventana.radioButton_sl_body.isChecked():
        candel_part = "body" 
    else:
        candel_part = "tail"

    if ventana.comboBox_side.currentText()=="Long":
        if ventana.radioButton_sl_tail.isChecked():
            var.sl_price = var.hist_candles[sl_candel]["low_price"]
        else:
            if var.hist_candles[sl_candel]["close_price"] > \
                var.hist_candles[sl_candel]["open_price"]:
                    var.sl_price = var.hist_candles[sl_candel]["open_price"]
            else:
                var.sl_price = var.hist_candles[sl_candel]["close_price"]
    else:
        if ventana.radioButton_sl_tail.isChecked():
            var.sl_price = var.hist_candles[sl_candel]["high_price"]
        else:
            if var.hist_candles[sl_candel]["open_price"] > \
                var.hist_candles[sl_candel]["close_price"]:
                    var.sl_price = var.hist_candles[sl_candel]["open_price"]
            else:
                var.sl_price = var.hist_candles[sl_candel]["close_price"]
                
    '''busca el valor del TP deseado'''
    act_price=var.mark_prices[var.symbol]
    tp_porcentaje= int(ventana.comboBox_tp.currentText()[:1])
    variacion= abs(act_price-var.sl_price) * tp_porcentaje
    
    if ventana.comboBox_side.currentText()=="Long":
        var.tp_price=act_price+variacion
    else:
        var.tp_price=act_price-variacion
    var.tp_price= round(var.tp_price,var.symbols_info[var.symbol]["pricePrecision"])    
    ventana.label_SL.setText(str(var.sl_price))
    ventana.label_TP.setText(str(var.tp_price))
       
def side_changed(side):
    global operation_side
    if side == "Long":
        operation_side = "BUY"
        ventana.pushButton_operation.setStyleSheet(
            "background-color: rgb(37, 230, 33);")
    else:
        operation_side = "SELL"
        ventana.pushButton_operation.setStyleSheet(
            "background-color: rgb(255, 0, 0);")
    ventana.pushButton_operation.setText(operation_side)

def time_frame_changed(time_frame):
    var.interval = time_frame
    global data_stream_id
    websocket_manager.stop_stream(data_stream_id)
    data_stream_id = websocket_manager.create_stream(
        ["markPrice@1s",f"kline_{var.interval}"],[var.symbol])
    var.hist_candles.clear()
    data.new_candle({}) 
    ventana.statusbar.showMessage(f"{var.tendencia} || {var.balance}")
    
def send_order():
    act_tp_sl()
    response= api_bridge.new_order_now(
        var.symbol, operation_side, var.tp_price, var.sl_price)
    
def symbol_changed(symbol,opening_app=False):
    var.symbol = symbol
    if opening_app == False:
        global data_stream_id
        websocket_manager.stop_stream(data_stream_id)
        data_stream_id = websocket_manager.create_stream(
            ["markPrice@1s",f"kline_{var.interval}"], [var.symbol])
    #var.stepSize= var.symbols_info[symbol]["stepSize"]
    var.pricePrecision = var.symbols_info[symbol]["pricePrecision"]
    var.hist_candles.clear()
    data.new_candle({}) 
    ventana.statusbar.showMessage(f"{var.tendencia} || {var.balance}")
    
    """======================instrucciones iniciales========================"""       
websocket_manager = BinanceWebSocketApiManager(
    exchange= privateconfig.exchange, output_default="dict")
userdata_stream_id = websocket_manager.create_stream(
    ["arr"],["!userData"], stream_label="userData",
    api_key=privateconfig.p_api_key, api_secret=privateconfig.p_secret_key
    )                            
data_stream_id = websocket_manager.create_stream(
    ["markPrice@1s",f"kline_{var.interval}"], ["btcusdt"]
    )

ventana = VentanaPrincipal() 
data.load_symbols_info()
api_bridge.future_account_balance("USDT")
symbol_changed("BTCUSDT",True)  #symbolo predeterminado al abrir la app
ventana.comboBox_symbol.addItems(var.symbols_info.keys())  
ventana.radioButton_sl_body.setChecked(True)
ventana.radioButton_tp_porcen.setChecked(True)

"""=======================conexions sinals-slots===========================""" 
ventana.comboBox_side.activated[str].connect(side_changed)
ventana.comboBox_timeframe.activated[str].connect(time_frame_changed)
ventana.comboBox_symbol.activated[str].connect(symbol_changed)
ventana.pushButton_operation.clicked.connect(send_order)
ventana.pushButton_act.clicked.connect(act_tp_sl)

if privateconfig.url == "https://fapi.binance.com":#por seguridad, luego borrar
    ventana.pushButton_operation.setEnabled(False)
    ventana.setStyleSheet("background-color: rgb(250, 160, 114);")

"""======================esto siempre al final=========================="""
if __name__ == "__main__": 
    app = QtWidgets.QApplication([]) 
    ventana.show() 
    worker = WorkerThread()
    worker.start()
    app.exec_()
=======
from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import websocket
import json
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import data
import api_bridge
import privateconfig
import variables as var
from gui_ppal import *


operation_side='BUY'

class VentanaPrincipal (QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def closeEvent(self, event):
        websocket_manager.stop_manager_with_all_streams()       
        worker.terminate()
        
'''=======================Acceso a data================================'''

class WorkerThread (QThread):
    def run (self):
        while True:
            oldest_stream_data_stream_buffer = \
                websocket_manager.pop_stream_data_from_stream_buffer()
            if oldest_stream_data_stream_buffer is False:
                time.sleep(0.01)
            else:
                info = data.incoming_data(oldest_stream_data_stream_buffer)
                process_data(info)

def process_data(info):
    
    if info[0] == "markPriceUpdate":
        ventana.label_price.setText(str(info[1]))

def act_tp_sl():

    '''busca el valor del SL deseado'''
    sl_candel= int("-" + ventana.comboBox_sl.currentText())
    
    if ventana.radioButton_sl_personal.isChecked():
        var.sl_price = float(ventana.textEdit_sl_personal.toPlainText())
    
    else:
        
        if ventana.comboBox_side.currentText()=="Long":
            if ventana.radioButton_sl_tail.isChecked():
                var.sl_price = var.hist_candles[sl_candel]["low_price"]
            else:
                if var.hist_candles[sl_candel]["close_price"] > \
                    var.hist_candles[sl_candel]["open_price"]:
                        var.sl_price = var.hist_candles[sl_candel]["open_price"]
                else:
                    var.sl_price = var.hist_candles[sl_candel]["close_price"]
        else:
            if ventana.radioButton_sl_tail.isChecked():
                var.sl_price = var.hist_candles[sl_candel]["high_price"]
            else:
                if var.hist_candles[sl_candel]["open_price"] > \
                    var.hist_candles[sl_candel]["close_price"]:
                        var.sl_price = var.hist_candles[sl_candel]["open_price"]
                else:
                    var.sl_price = var.hist_candles[sl_candel]["close_price"]
                    
    '''busca el valor del TP deseado'''
    act_price=var.mark_prices[var.symbol]
    tp_porcentaje= int(ventana.comboBox_tp.currentText()[:1])
    variacion= abs(act_price-var.sl_price) * tp_porcentaje
    
    if ventana.comboBox_side.currentText()=="Long":
        var.tp_price=act_price+variacion
    else:
        var.tp_price=act_price-variacion
    var.tp_price= round(var.tp_price,var.symbols_info[var.symbol]["tickSize"])    
    ventana.label_SL.setText(str(var.sl_price))
    ventana.label_TP.setText(str(var.tp_price))
    print('wwwwwwwwwwwwwwwww',var.tp_price, var.sl_price,'wwwwwwwwwwwwwwwww')
    
def side_changed(side):
    global operation_side
    if side == "Long":
        operation_side = "BUY"
        ventana.pushButton_operation.setStyleSheet(
            "background-color: rgb(37, 230, 33);")
    else:
        operation_side = "SELL"
        ventana.pushButton_operation.setStyleSheet(
            "background-color: rgb(255, 0, 0);")
    ventana.pushButton_operation.setText(operation_side)

def time_frame_changed(time_frame):
    var.interval = time_frame
    global data_stream_id
    websocket_manager.stop_stream(data_stream_id)
    data_stream_id = websocket_manager.create_stream(
        ["markPrice@1s",f"kline_{var.interval}"],[var.symbol])
    var.hist_candles.clear()
    data.new_candle({}) 
    ventana.statusbar.showMessage(f"{var.tendencia} || {var.balance}")
    
def send_order():
    act_tp_sl()
    response= api_bridge.new_order_now(
        var.symbol, operation_side, var.tp_price, var.sl_price)
    
def symbol_changed(symbol,opening_app=False):
    var.symbol = symbol
    if opening_app == False:
        global data_stream_id
        websocket_manager.stop_stream(data_stream_id)
        data_stream_id = websocket_manager.create_stream(
            ["markPrice@1s",f"kline_{var.interval}"], [var.symbol])
    #var.stepSize= var.symbols_info[symbol]["stepSize"]
    var.pricePrecision = var.symbols_info[symbol]["pricePrecision"]
    var.hist_candles.clear()
    data.new_candle({}) 
    ventana.statusbar.showMessage(f"{var.tendencia} || {var.balance}")
    
    """======================instrucciones iniciales========================"""       
websocket_manager = BinanceWebSocketApiManager(
    exchange= privateconfig.exchange, output_default="dict")
userdata_stream_id = websocket_manager.create_stream(
    ["arr"],["!userData"], stream_label="userData",
    api_key=privateconfig.p_api_key, api_secret=privateconfig.p_secret_key
    )                            
data_stream_id = websocket_manager.create_stream(
    ["markPrice@1s",f"kline_{var.interval}"], ["btcusdt"]
    )
app = QApplication([])
ventana = VentanaPrincipal() 
data.load_symbols_info()
api_bridge.future_account_balance("USDT")
symbol_changed("BTCUSDT",True)  #symbolo predeterminado al abrir la app
ventana.comboBox_symbol.addItems(var.symbols_info.keys())  
ventana.radioButton_sl_tail.setChecked(True)
ventana.radioButton_tp_porcen.setChecked(True)

"""=======================conexions sinals-slots===========================""" 
ventana.comboBox_side.activated[str].connect(side_changed)
ventana.comboBox_timeframe.activated[str].connect(time_frame_changed)
ventana.comboBox_symbol.activated[str].connect(symbol_changed)
ventana.pushButton_operation.clicked.connect(send_order)
ventana.pushButton_act.clicked.connect(act_tp_sl)

if privateconfig.url == "https://fapi.binance.com":#por seguridad, luego borrar
    #ventana.pushButton_operation.setEnabled(False)
    ventana.setStyleSheet("background-color: rgb(250, 160, 114);")

"""======================esto siempre al final=========================="""
if __name__ == '__main__':   
    ventana.show() 
    worker = WorkerThread()
    worker.start()
    app.exec_()
>>>>>>> 3b87cef4205a94fddcf5465567f3131b0236bd34
