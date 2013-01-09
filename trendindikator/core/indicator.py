'''
Created on Jan 9, 2013

Indicator strategies

@author: Pyranja
'''
import pipe

'''
Buys if stock price exceeds history's max value and sells if price drops below
history's min value
'''
class BreakRange():
    
    def __init__(self, history):
        self.history = history
        
    def process(self, price, plot):
        plot.y[pipe.KEY_LOWER] = self.history.lowest()
        plot.y[pipe.KEY_UPPER] = self.history.highest()
        if price > self.history.highest():
            command = pipe.CMD_BUY
        elif price < self.history.lowest():
            command = pipe.CMD_SELL
        else:
            command = pipe.CMD_NONE
        return command

'''
Buys exactly once on the first invocation, then always signals NONE
'''
class BuyAndHold():
        
    def __init__(self):
        self.price = None    
        
    def process(self, price, plot):
        command = pipe.CMD_NONE
        if not self.price:
            self.price = price
            command = pipe.CMD_BUY
        return command
    
    