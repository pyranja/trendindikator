'''
Created on Jan 9, 2013

Trading strategies

@author: Pyranja
'''
import pipe

def create_trader(starting_funds, dynamic_budget = False, short_sell = False, reverse = False):
    budget = DynamicBudget(starting_funds) if dynamic_budget else StaticBudget(starting_funds)
    product = ShortLong(budget) if short_sell else OnlyLong(budget)
    if reverse:
        product = SignalReverser(product)
    return product
    
class StaticBudget():
    '''Maintains a fixed budget'''
    def __init__(self, starting):
        self.starting = starting
        self.current = starting
    
    def deposit(self, amount):
        self.current += amount
    
    def quantity_for(self, price):
        return self.starting // price
    
    def current_yield(self, profit = 0):
        return self.current + profit - self.starting

class DynamicBudget():
    '''Maintains a changing budget'''
    def __init__(self, starting):
        self.starting = starting
        self.current = starting
        
    def deposit(self, amount):
        self.current += amount
        
    def quantity_for(self, price):
        return self.current // price
    
    def current_yield(self, profit = 0):
        return self.current + profit - self.starting

class Short():
    '''Expects price to fall.'''
    def __init__(self, quantity, price):
        self.price = price
        self.quantity = quantity
        
    def should_clear_on(self, command):
        return True if command == pipe.CMD_BUY else False
        
    def clear(self, price):
        return self.quantity * (self.price - price)

class Long():
    '''Expects price to rise.'''
    def __init__(self, quantity, price):
        self.price = price
        self.quantity = quantity
    
    def should_clear_on(self, command):
        return True if command == pipe.CMD_SELL else False    
        
    def clear(self, price):
        return self.quantity * (price - self.price)

class SignalReverser(object):
    '''
    Wraps a trader and changes all received signals to the opposite
    '''
    def __init__(self, delegate):
        self.delegate = delegate
        
    def process(self, command, price, plot):
        if command == pipe.CMD_BUY:
            command = pipe.CMD_SELL
        elif command == pipe.CMD_SELL:
            command = pipe.CMD_BUY
        # NONE stays
        return self.delegate.process(command, price, plot)

    def finish(self, *args):
        return self.delegate.finish(*args)

class AbstractTrader(object):
    '''Template for a trader'''
    def __init__(self, budget):
        self.budget = budget
        self.position = None
        self.last_price = None
    
    def process(self, command, price, plot):
        '''
        React to given command by either clearing a held position or creating a 
        new position or doing nothing. Return the profit generated this cycle. 
        '''
        profit = 0
        action = pipe.ACTION_NO
        self.last_price = price # memoize for finish
        self.plot(plot, command, price)
        if self.position is not None: 
            if self.position.should_clear_on(command):
                profit = self.position.clear(price)
                self.budget.deposit(profit)
                self.position = None
                action = pipe.ACTION_CLEAR
        else:
            self.position, action = self.position_for(command, price)
        plot.y[pipe.KEY_ACTION] = action
        return profit
    
    def plot(self, plot, command, price):
        plot.y[pipe.KEY_COMMAND] = command
        virtual_profit = self.position.clear(price) if self.position is not None else 0
        plot.y[pipe.KEY_PROFIT] = virtual_profit
        plot.y[pipe.KEY_YIELD] = self.budget.current_yield(virtual_profit)
        if self.position is not None:
            plot.y[pipe.KEY_HOLD_AT] = self.position.price
        else:
            plot.y[pipe.KEY_HOLD_AT] = None
    
    def position_for(self, command, price):
        '''Create a new position for given command and price.'''
        raise NotImplementedError("Missing template method")
    
    def finish(self, plot):
        '''Clear any outstanding position.'''
        profit = 0
        if self.position is not None:
            profit = self.position.clear(self.last_price)
        plot.y[pipe.KEY_PROFIT] = profit
        plot.y[pipe.KEY_YIELD] = self.budget.current_yield(profit)
        plot.y[pipe.KEY_ACTION] = pipe.ACTION_CLEAR
        return profit

class ShortLong(AbstractTrader):
    '''Uses SHORT and LONG positions.'''
    def __init__(self, *args):
        super(ShortLong, self).__init__(*args)
    
    # override
    def position_for(self, command, price):
        quantity = self.budget.quantity_for(price)
        if command == pipe.CMD_BUY:
            return Long(quantity, price), pipe.ACTION_LONG
        elif command == pipe.CMD_SELL:
            return Short(quantity, price), pipe.ACTION_SHORT
        else:
            return None, pipe.ACTION_NO

class OnlyLong(AbstractTrader):
    '''Only uses LONG positions.'''
    def __init__(self, *args):
        super(OnlyLong, self).__init__(*args)
        
    # override
    def position_for(self, command, price):
        quantity = self.budget.quantity_for(price)
        if command == pipe.CMD_BUY:
            return Long(quantity, price), pipe.ACTION_LONG
        else:
            return None, pipe.ACTION_NO
        
class OnlyShort(AbstractTrader):
    def __init__(self, *args):
        super(OnlyShort, self).__init__(*args)
        
    # override
    def position_for(self, command, price):
        quantity = self.budget.quantity_for(price)
        if command == pipe.CMD_SELL:
            return Short(quantity, price), pipe.ACTION_SHORT
        else:
            return None, pipe.ACTION_NO
    