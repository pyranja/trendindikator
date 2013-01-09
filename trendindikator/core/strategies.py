'''
Created on 15.11.2012

indicator- and trading-strategy factory methods

@author: Pyranja
'''
import comps

'''
Indicator that interprets a price that is higher than the history's maximum as a BUY
and a price that is lower than the history's minimum as a SELL. The given history
should not be modified afterwards.
@param history: initialized history that will be consulted, must support lowest() and highest()
@return: indicator that returns command and history's MAX and MIN as limits 
'''
def createBreakRangeIndicator(history):
    def indicator(price):
        limits = {}
        limits["low"] = history.lowest()
        limits["high"] = history.highest()
        if price > history.highest():
            command = comps.BUY
        elif price < history.lowest():
            command = comps.SELL
        else:
            command = comps.NONE
        history.update(price) # externalize this?
        return command, limits
    return indicator

'''
Indicator that will trigger a BUY only on the first price, else NONE
@return: indicator that returns command and single purchase price as limit 
'''
def createBuyAndHoldIndicator():
    def indicator(price):
        command = comps.NONE
        if not indicator.price:
            indicator.price = price
            command = comps.BUY
        limits = { "price" : indicator.price }
        return command, limits
    return indicator

'''
Trader with a fixed budget, that buys immediately on a BUY and holds until first SELL.
@param budget: Fixed budget available for each BUY
'''   
def createSingleIndexBuySellTrader(budget):
    def trader(command, price):
        profit = None
        if command == comps.BUY and not trader.purchase_quantity:
            assert not trader.purchase_price
            trader.purchase_quantity = budget // price
            trader.purchase_price = price * trader.purchase_quantity
        if command == comps.SELL or command == comps.FINISH and trader.purchase_quantity:
            assert trader.purchase_price
            profit = (trader.purchase_quantity * price) - trader.purchase_price
            trader.purchase_price = None
            trader.purchase_quantity = None
        return profit
    trader.purchase_quantity = None
    trader.purchase_price = None
    return trader