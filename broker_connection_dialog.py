# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 14:07:08 2018

@author: roman.rodriguez
"""
from PySide2.QtGui import QIntValidator
from PySide2.QtWidgets import (QDialog, QDialogButtonBox, QGroupBox, QLabel,
            QLineEdit, QVBoxLayout)
import asyncio
from quamash import QEventLoop, QThreadExecutor
from broker_connection import BrokerConnection
from simple_settings import LazySettings


class BrokerConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super(BrokerConnectionDialog, self).__init__(parent)
        
        self.settings = LazySettings('settings')
        self.broker = BrokerConnection()

        onlyInt = QIntValidator(1, 9999)

        hostLabel = QLabel("Host:")
        self.hostEdit = QLineEdit(self.settings.HOST)

        portLabel = QLabel("Port:")
        self.portEdit = QLineEdit(str(self.settings.PORT))
        self.portEdit.setValidator(onlyInt)

        clientIdLabel = QLabel("Client ID:")
        self.clientIdEdit = QLineEdit('1')
        self.clientIdEdit.setValidator(onlyInt)


        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.groupBox = QGroupBox()
        groupLayout = QVBoxLayout()
        groupLayout.addWidget(hostLabel)
        groupLayout.addWidget(self.hostEdit)
        groupLayout.addWidget(portLabel)
        groupLayout.addWidget(self.portEdit)
        groupLayout.addWidget(clientIdLabel)
        groupLayout.addWidget(self.clientIdEdit)
        groupLayout.addStretch(1)
        self.groupBox.setLayout(groupLayout)
        
        if self.broker.isConnected():
            buttonBox.button(QDialogButtonBox.Ok).setText('Disconnect')
            self.groupBox.setEnabled(False)
        else:
            buttonBox.button(QDialogButtonBox.Ok).setText('Connect')
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.groupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Settings")
        
    def accept(self):
        host = self.hostEdit.text()
        port = int(self.portEdit.text())
        client_id = int(self.clientIdEdit.text())
        self.broker.connect(host, port, client_id)
        self.broker.ib.connectedEvent += self.onConnectionEstablished
        self.hide()
        
    def onConnectionEstablished(self):
        if self.parent():
            self.parent().statusBar().showMessage('Connected to IB TWS/Gateway')
        else:
            print('Connected to IB TWS/Gateway')
        # Retrieve account open option positions from broker
        opt_positions = self.broker.positions()
        print(opt_positions)
            
    def reject(self):
        self.hide()
        
        
if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    brokerDialog = BrokerConnectionDialog()
    brokerDialog.show()
    
    with loop:
        loop.run_forever()
    