# FIWI, WS 2012
# trend indicator
# core components
# @author Chris Borckholder
from collections import deque

# predefined plot keys
KEY_PRICE = "price"         # current price of share
KEY_COMMAND = "command"     # signaled command
KEY_PROFIT = "profit"       # profit of trader at this time
KEY_LOWER = "lower"         # lower bound of indicator
KEY_UPPER = "upper"         # upper bound of indicator
KEY_HOLD_AT = "hold_at"     # trader holds shares at this price

# possible commands
CMD_BUY = "buy"
CMD_SELL = "sell"
CMD_NONE = "none"

def process(index, signaller, trader, histories):
    plot = []
    for day, price in index:
        if all([h.is_ready() for h in histories]):
            now = MultiPlotPoint(day)
            plot.append(now)
            command = signaller.process(price, now)
            profit = trader.process(command, price, now)
        [h.update(price) for h in histories]
    trader.finish(plot[-1])
    return plot
        
'''
Associates a single x value with multiple key->value pairs
'''
class MultiPlotPoint():
    
    def __init__(self, x):
        self.x = x
        self.y = {}
      
'''
Maintains a variable length history of prices
'''
class History():
  
    def __init__(self, size):
        self._missing = size
        self._values = deque([0] * size, size)
    
    '''
    Sets given value as current and pushes former current into history
    '''
    def update(self, value):
        self._values.append(value)
        if self._missing > 0:
            self._missing -= 1
        return self
    
    '''
    Checks whether history is fully filled
    '''
    def is_ready(self):
        return self._missing <= 0
    
    def mean(self):
        return sum(self._values) / len(self._values)
    
    def lowest(self):
        return min(self._values)
    
    def highest(self):
        return max(self._values)
