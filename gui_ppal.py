# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_ppal.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(295, 309)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_sl = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_sl.setGeometry(QtCore.QRect(10, 140, 131, 141))
        self.groupBox_sl.setObjectName("groupBox_sl")
        self.radioButton_sl_body = QtWidgets.QRadioButton(self.groupBox_sl)
        self.radioButton_sl_body.setGeometry(QtCore.QRect(10, 20, 89, 20))
        self.radioButton_sl_body.setObjectName("radioButton_sl_body")
        self.radioButton_sl_tail = QtWidgets.QRadioButton(self.groupBox_sl)
        self.radioButton_sl_tail.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.radioButton_sl_tail.setObjectName("radioButton_sl_tail")
        self.label_SL = QtWidgets.QLabel(self.groupBox_sl)
        self.label_SL.setGeometry(QtCore.QRect(10, 120, 111, 20))
        self.label_SL.setTextFormat(QtCore.Qt.RichText)
        self.label_SL.setAlignment(QtCore.Qt.AlignCenter)
        self.label_SL.setObjectName("label_SL")
        self.comboBox_sl = QtWidgets.QComboBox(self.groupBox_sl)
        self.comboBox_sl.setGeometry(QtCore.QRect(80, 30, 41, 22))
        self.comboBox_sl.setObjectName("comboBox_sl")
        self.comboBox_sl.addItem("")
        self.comboBox_sl.addItem("")
        self.comboBox_sl.addItem("")
        self.comboBox_sl.addItem("")
        self.comboBox_sl.addItem("")
        self.comboBox_sl.addItem("")
        self.comboBox_sl.addItem("")
        self.comboBox_sl.addItem("")
        self.comboBox_sl.addItem("")
        self.comboBox_sl.addItem("")
        self.radioButton_sl_personal = QtWidgets.QRadioButton(self.groupBox_sl)
        self.radioButton_sl_personal.setGeometry(QtCore.QRect(10, 80, 31, 20))
        self.radioButton_sl_personal.setText("")
        self.radioButton_sl_personal.setObjectName("radioButton_sl_personal")
        self.textEdit_sl_personal = QtWidgets.QTextEdit(self.groupBox_sl)
        self.textEdit_sl_personal.setGeometry(QtCore.QRect(40, 70, 81, 31))
        self.textEdit_sl_personal.setObjectName("textEdit_sl_personal")
        self.groupBox_tp = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_tp.setGeometry(QtCore.QRect(150, 140, 131, 141))
        self.groupBox_tp.setObjectName("groupBox_tp")
        self.label_TP = QtWidgets.QLabel(self.groupBox_tp)
        self.label_TP.setGeometry(QtCore.QRect(10, 120, 111, 16))
        self.label_TP.setScaledContents(False)
        self.label_TP.setAlignment(QtCore.Qt.AlignCenter)
        self.label_TP.setObjectName("label_TP")
        self.comboBox_tp = QtWidgets.QComboBox(self.groupBox_tp)
        self.comboBox_tp.setGeometry(QtCore.QRect(30, 30, 61, 22))
        self.comboBox_tp.setObjectName("comboBox_tp")
        self.comboBox_tp.addItem("")
        self.comboBox_tp.addItem("")
        self.comboBox_tp.addItem("")
        self.radioButton_tp_porcen = QtWidgets.QRadioButton(self.groupBox_tp)
        self.radioButton_tp_porcen.setGeometry(QtCore.QRect(4, 31, 21, 20))
        self.radioButton_tp_porcen.setText("")
        self.radioButton_tp_porcen.setObjectName("radioButton_tp_porcen")
        self.comboBox_symbol = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_symbol.setGeometry(QtCore.QRect(10, 80, 131, 22))
        self.comboBox_symbol.setEditable(True)
        self.comboBox_symbol.setObjectName("comboBox_symbol")
        self.pushButton_operation = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_operation.setGeometry(QtCore.QRect(180, 70, 51, 24))
        self.pushButton_operation.setStyleSheet("background-color: rgb(37, 230, 33);")
        self.pushButton_operation.setObjectName("pushButton_operation")
        self.label_price = QtWidgets.QLabel(self.centralwidget)
        self.label_price.setGeometry(QtCore.QRect(10, 20, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_price.setFont(font)
        self.label_price.setAutoFillBackground(False)
        self.label_price.setFrameShape(QtWidgets.QFrame.Box)
        self.label_price.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_price.setLineWidth(2)
        self.label_price.setObjectName("label_price")
        self.comboBox_side = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_side.setGeometry(QtCore.QRect(10, 110, 61, 22))
        self.comboBox_side.setObjectName("comboBox_side")
        self.comboBox_side.addItem("")
        self.comboBox_side.addItem("")
        self.comboBox_timeframe = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_timeframe.setGeometry(QtCore.QRect(80, 110, 62, 22))
        self.comboBox_timeframe.setObjectName("comboBox_timeframe")
        self.comboBox_timeframe.addItem("")
        self.comboBox_timeframe.addItem("")
        self.comboBox_timeframe.addItem("")
        self.comboBox_timeframe.addItem("")
        self.comboBox_timeframe.addItem("")
        self.comboBox_timeframe.addItem("")
        self.pushButton_act = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_act.setGeometry(QtCore.QRect(180, 30, 51, 24))
        self.pushButton_act.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.pushButton_act.setObjectName("pushButton_act")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Binance-Boot V1"))
        self.groupBox_sl.setTitle(_translate("MainWindow", "SL"))
        self.radioButton_sl_body.setText(_translate("MainWindow", "Body"))
        self.radioButton_sl_tail.setText(_translate("MainWindow", "Tail"))
        self.label_SL.setText(_translate("MainWindow", "Select SL"))
        self.comboBox_sl.setItemText(0, _translate("MainWindow", "1"))
        self.comboBox_sl.setItemText(1, _translate("MainWindow", "2"))
        self.comboBox_sl.setItemText(2, _translate("MainWindow", "3"))
        self.comboBox_sl.setItemText(3, _translate("MainWindow", "4"))
        self.comboBox_sl.setItemText(4, _translate("MainWindow", "5"))
        self.comboBox_sl.setItemText(5, _translate("MainWindow", "6"))
        self.comboBox_sl.setItemText(6, _translate("MainWindow", "7"))
        self.comboBox_sl.setItemText(7, _translate("MainWindow", "8"))
        self.comboBox_sl.setItemText(8, _translate("MainWindow", "9"))
        self.comboBox_sl.setItemText(9, _translate("MainWindow", "10"))
        self.groupBox_tp.setTitle(_translate("MainWindow", "TP"))
        self.label_TP.setText(_translate("MainWindow", "Select TP"))
        self.comboBox_tp.setItemText(0, _translate("MainWindow", "3%"))
        self.comboBox_tp.setItemText(1, _translate("MainWindow", "4%"))
        self.comboBox_tp.setItemText(2, _translate("MainWindow", "5%"))
        self.pushButton_operation.setText(_translate("MainWindow", "BUY"))
        self.label_price.setText(_translate("MainWindow", "0,00"))
        self.comboBox_side.setItemText(0, _translate("MainWindow", "Long"))
        self.comboBox_side.setItemText(1, _translate("MainWindow", "Short"))
        self.comboBox_timeframe.setItemText(0, _translate("MainWindow", "3m"))
        self.comboBox_timeframe.setItemText(1, _translate("MainWindow", "1m"))
        self.comboBox_timeframe.setItemText(2, _translate("MainWindow", "5m"))
        self.comboBox_timeframe.setItemText(3, _translate("MainWindow", "15m"))
        self.comboBox_timeframe.setItemText(4, _translate("MainWindow", "30m"))
        self.comboBox_timeframe.setItemText(5, _translate("MainWindow", "1h"))
        self.pushButton_act.setText(_translate("MainWindow", "ACT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
