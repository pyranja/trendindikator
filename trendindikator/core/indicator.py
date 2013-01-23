'''
Created on Jan 9, 2013

FIWI WS 2012
Signaler strategies

@author: Pyranja
'''
import pipe

# indicator types
SIG_BUY_HOLD = "buy hold"
SIG_BREAK_RANGE = "break range"
SIG_MOVING_AVERAGE = "moving average"

# static factory method
def create_signaler(sig_type, sensitivity, threshold, *args):
    '''
    Create a signaler and its histories according to given arguments. Return the
    created signaler and a list of histories used by it (possibly empty).'''
    histories = []
    product = None
    modifier = create_thresholder(threshold)    # increases / decreases limits
    # switch requested type
    if sig_type == SIG_BUY_HOLD:
        product = BuyAndHold()
    elif sig_type == SIG_BREAK_RANGE:
        '''
        expecting single argument: 
            length of range
        '''
        if len(args) != 1:
            raise ValueError("Expected single additional argument for %s but received %s" % (sig_type, args))
        history = pipe.History(int(args[0]))
        product = BreakRange(history, modifier)
        histories.append(history)
    elif sig_type == SIG_MOVING_AVERAGE:
        '''
        expecting two arguments:
           length of fast history 
           length of slow history
        '''
        if len(args) != 2:
            raise ValueError("Expected two additional arguments for %s but received %s" % (sig_type, args))
        fast = pipe.History(int(args[0]))
        slow = pipe.History(int(args[1]))
        product = MovingAverage(fast, slow, modifier)
        histories += [fast, slow]
    else:   # default
        raise ValueError("Given type %s does not available" % sig_type)
    # end switch
    # wrap with damper if sensitivity > 0
    if sensitivity > 0:
        product = Damper(product, sensitivity)
    return product, histories

def create_thresholder(threshold):
    if threshold > 1.0 or threshold < 0.0:
        raise ValueError("Threshold factor must be in 0..1 but was %f" % threshold)
    def product(value):
        return threshold * value
    return product

class Damper():
    '''
    Wrap a signaler and forward its generated signal only if it was repeated at
    least sensitivity times in a row.
    '''
    
    def __init__(self, delegate, sensitivity):
        self.delegate = delegate
        self.sensitivity = sensitivity
        self.last_command = None
        self.repetitions = 0
        
    def process(self, price, plot):
        forward = pipe.CMD_NONE
        command = self.delegate.process(price, plot)
        if command == self.last_command:
            if self.repetitions >= self.sensitivity:
                forward = command
            self.repetitions += 1
        else:
            self.last_command = command
            self.repetitions = 0
        return forward

class BreakRange():
    '''
    Signal BUY if stock price exceeds range's max value and SELL if price 
    drops below range's min value
    '''
    
    def __init__(self, history, modifier):
        self.range = history
        self.mod = modifier
        
    def process(self, price, plot):
        lower = self.range.lowest()
        upper = self.range.highest()
        plot.y[pipe.KEY_LOWER] = lower
        plot.y[pipe.KEY_UPPER] = upper
        if price > (upper + self.mod(upper)):
            command = pipe.CMD_BUY
        elif price < (lower - self.mod(lower)):
            command = pipe.CMD_SELL
        else:
            command = pipe.CMD_NONE
        return command

class BuyAndHold():
    '''
    Signal BUY exactly once on the first invocation, then always signal NONE.
    '''
        
    def __init__(self):
        self.is_first = True    
        
    def process(self, price, plot):
        command = pipe.CMD_NONE
        if self.is_first:
            self.is_first = False
            command = pipe.CMD_BUY
        return command
    
class MovingAverage():
    '''
    Signal BUY if shorter average is above longer and vice versa
    '''
    
    def __init__(self, fast, slow, modifier):
        self.fast = fast
        self.slow = slow
        self.mod = modifier
    
    def process(self, price, plot):
        pass
        