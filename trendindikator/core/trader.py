'''
Created on Jan 9, 2013

Trading strategies

@author: Pyranja
'''
import pipe

'''
Trader with a fixed budget, that buys immediately on a BUY and holds until first SELL.
'''
class SingleIndexBuySell():

    def __init__(self, budget):
        self.budget = budget
        self.purchase_quantity = None
        self.purchase_price = None
        self.last_price = None
        
    def _sell(self, price):
        profit = self.purchase_quantity * (price - self.purchase_price)
        self.purchase_price = None
        self.purchase_quantity = None
        return profit
    
    def _buy(self, price):
        self.purchase_quantity = self.budget // price
        self.purchase_price = price
        
    def process(self, command, price, plot):
        profit = 0
        self.last_price = price # memoize for finish
        if command == pipe.CMD_BUY and not self.purchase_quantity:
            assert not self.purchase_price
            self._buy(price)
        if command == pipe.CMD_SELL and self.purchase_quantity:
            assert self.purchase_price
            profit = self._sell(price)
        if self.purchase_quantity:
            plot.y[pipe.KEY_HOLD_AT] = self.purchase_price
        else:
            plot.y[pipe.KEY_HOLD_AT] = None
        plot.y[pipe.KEY_COMMAND] = command
        plot.y[pipe.KEY_PROFIT] = profit
        plot.y[pipe.KEY_PRICE] = price
        return profit
    
    def finish(self, plot):
        profit = 0
        if self.purchase_quantity:
            profit = self._sell(self.last_price)
        plot.y[pipe.KEY_PROFIT] += profit
        plot.y[pipe.KEY_COMMAND] = pipe.CMD_SELL
        return profit
    