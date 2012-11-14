# FIWI, WS 2012
# trend indicator
# core components
# @author Chris Borckholder
from collections import deque

# predefined sink keys
KEY_INDEX = "index"
KEY_COMMAND = "command"
KEY_PROFIT = "profit"

# possible commands
BUY = "command_buy"
SELL = "command_sell"
NONE = "command_none"
FINISH = "command_finish"

class Signaller():
    # Signalling component
    # Collaborators
    #   graph sink for limit data
    #   trader as next in chain
    # Dependencies
    #   indicator_strategy function that evals price to produce command
    def __init__(self, indicator_strategy, trader, graph):
        self._trader = trader
        self._graph = graph
        self._indicator = indicator_strategy

    def process(self, command, day, price):
        command, limits = self._indicator(price)
        # update graph sink
        graph_msg = { KEY_COMMAND : command }
        for key, value in limits.iteritems:
            graph_msg[key] = (day, value)
            self._graph.send(graph_msg)
        # forward to trader
        self._trader.process(command, day, price)
    
class Trader():
    # Trading component
    # Collaborators
    #   statistics sink for profit data
    # Dependencies
    #   trading_strategy computes profit for given commands
    def __init__(self, trading_strategy, statistics):
        self._statistics = statistics
        self._trading = trading_strategy
    
    def process(self, command, day, price):
        profit = self._trading(command, price)
        # update statistics sink
        if profit:
            self._statistics.send(KEY_PROFIT=(day, price))

class DataSink():
    # gathers data from sent messages, e.g.
    #   prices
    #   used limits
    #   signalled commands
    #   or profit
    # for each day
    def __init__(self):
        self._data = { }
    
    def send(self, **message):
        for key, value in message:
            if not key in self._data:
                self._data[key] = []
            self._data[key].append(value)
  
    def data(self):
        return self._data
      
class History():
  
    def __init__(self, size):
        self._values = deque([0] * size, size)
    
    def update(self, *values):
        for val in values:
            self._values.append(val)
        return self
    
    def mean(self):
        return sum(self._values) / len(self._values)
    
    def min(self):
        return min(self._values)
    
    def max(self):
        return max(self._values)
