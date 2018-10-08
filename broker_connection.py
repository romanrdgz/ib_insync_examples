# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 15:06:53 2018

@author: roman.rodriguez
"""
from ib_insync import IB, util
util.useQt()


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    

class BrokerConnection(metaclass=Singleton):
    def __init__(self):
        self.ib = IB()

    def connect(self, host, port, client_id, callback=None):
        self.ib.connect(host, port, clientId=client_id)
        if callback:
            self.ib.connectedEvent += callback
        
    def disconnect(self):
        self.ib.disconnect()
        
    def isConnected(self):
        return self.ib.isConnected()
        
    def positions(self):
        return [pos for pos in self.ib.positions() if pos.contract.secType == 'OPT']
    
    def reqMatchingSymbols(self, text_to_search):
        '''
        Function IBApi::EClient::reqMatchingSymbols is available to search for
        stock contracts. The input can be either the first few letters of the
        ticker symbol, or for longer strings, a character sequence matching a
        word in the security name.
        https://interactivebrokers.github.io/tws-api/matching_symbols.html
        '''
        return self.ib.reqMatchingSymbols(text_to_search)
    
    def getOptionChainContracts(self, contract):
        chain = self.ib.reqSecDefOptParams(contract.symbol, contract.exchange, contract.secType, contract.conId)
        qChain = self.ib.qualifyContracts(chain)
        #return util.df(qChain)
        return qChain