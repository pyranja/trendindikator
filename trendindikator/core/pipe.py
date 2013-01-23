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
KEY_ACTION = "action"       # trader took this action

# possible actions
ACTION_NO = "no action"     # did nothing
ACTION_LONG = "long"        # create long position
ACTION_SHORT = "short"      # create short position
ACTION_CLEAR = "clear"      # clear current position

# possible commands
CMD_BUY = "buy"
CMD_SELL = "sell"
CMD_NONE = "none"

def process(index, sigtrader, histories):
    '''
    Process all day->price pairs provided by the given index. Feed each pair 
    to all given histories. If all histories are ready, feed subsequent pairs 
    also to all given signaler->trader pairs.
    After the index was consumed completely, finish all given traders and return
    the generated list of MultiValuePoints.
    @type index: Iterable that provides day->price pairs
    @type sigtrader : List of (Signaler,Trader) tuples
    @type histories : List of Histories
    
    @todo create a distinct plot for each sigtrader pair 
    '''
    plot = []
    for day, price in index:
        if all([h.is_ready() for h in histories]):
            now = MultiValuePoint(day)
            plot.append(now)
            for signaler, trader in sigtrader:
                command = signaler.process(price, now)
                trader.process(command, price, now)
        [h.update(price) for h in histories]
    [trader.finish(plot[-1]) for _, trader in sigtrader]
    return plot
        
class MultiValuePoint():
    '''Associates a single x value with multiple key->value pairs'''
    
    def __init__(self, x):
        self.x = x
        self.y = {}
      
class PipeSpec(object):
    '''Holds all required components of a processing pipe.'''
    
    def __init__(self):
        self.sigtrader = []
        self.histories = []
        
    def merge(self, other):
        '''Unify the given PipeSpec with this PipeSpec and return this.'''
        self.sigtrader += other.sigtrader
        self.histories += other.histories
        return self      
      
class History():
    '''Maintains a variable length history of prices'''
  
    def __init__(self, size):
        '''Initialize a History of size length with all zeros.'''
        self._missing = size
        self._values = deque([0] * size, size)
    
    def update(self, price):
        '''Advance history by dropping the first price and appending the given price.'''
        self._values.append(price)
        if self._missing > 0:
            self._missing -= 1
        return self
    
    def is_ready(self):
        '''Check whether history has been advanced at least size times.'''
        return self._missing <= 0
    
    def mean(self):
        return sum(self._values) / len(self._values)
    
    def lowest(self):
        return min(self._values)
    
    def highest(self):
        return max(self._values)
