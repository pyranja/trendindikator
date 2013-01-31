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
SIG_SIMPLE_MOVING_AVERAGE = "simple moving average"
SIG_DUAL_MOVING_AVERAGE = "dual moving average"

def pack(name, trader, *args):
    pipe_spec = pipe.PipeSpec()
    signaler, histories = create_signaler(*args)
    pipe_spec.sigtrader.append( (name, signaler, trader) )
    pipe_spec.histories += histories
    return pipe_spec

# static factory method
def create_signaler(sig_type, signal_threshold, envelope_factor, *args):
    '''
    Create a signaler and its histories according to given arguments. Return the
    created signaler and a list of histories used by it (possibly empty).
    '''
    if signal_threshold < 0:
        raise ValueError("Indicator sensitivity must be positive, but was %f" % signal_threshold)
    histories = []
    product = None
    modifier = create_envelope(envelope_factor)    # increases / decreases limits
    # switch requested type
    if sig_type == SIG_BUY_HOLD:
        '''
        expecting no argument
        '''
        if len(args) != 0:
            raise ValueError("Expected no additional argument for %s but received %s" % (sig_type, args))
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
        histories = [history]
    elif sig_type == SIG_SIMPLE_MOVING_AVERAGE:
        '''
        expecting one argument:
           length of average
        '''
        if len(args) != 1:
            raise ValueError("Expected two additional arguments for %s but received %s" % (sig_type, args))
        history = pipe.History(int(args[0]))
        product = SimpleMovingAverage(history, modifier)
        histories = [history]
    elif sig_type == SIG_DUAL_MOVING_AVERAGE:
        '''
        expecting two arguments:
           length of fast history 
           length of slow history
        '''
        if len(args) != 2:
            raise ValueError("Expected two additional arguments for %s but received %s" % (sig_type, args))
        fast = pipe.History(int(args[0]))
        slow = pipe.History(int(args[1]))
        if fast >= slow:
            raise ValueError("Fast average length (%f) must be smaller than slow average length (%f) in %s" % (fast, slow, sig_type))
        product = DualMovingAverage(fast, slow, modifier)
        histories = [fast, slow]
    else:   # default
        raise ValueError("Given type %s is not available" % sig_type)
    # end switch
    # wrap with damper if sensitivity > 0
    if signal_threshold > 0:
        product = Damper(product, signal_threshold)
    return product, histories

def create_envelope(factor):
    if factor > 1.0 or factor < 0.0:
        raise ValueError("Threshold factor must be in 0..1 but was %f" % factor)
    def product(value):
        return factor * value
    return product

class Damper():
    '''
    Wrap a signaler and forward its generated signal only if it was repeated at
    least sensitivity times in a row.
    '''
    
    def __init__(self, delegate, sensitivity):
        if sensitivity < 0:
            raise ValueError("Indicator sensitivity must be positive, but was %f" % sensitivity)
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
        lower = lower - self.mod(lower)
        upper = self.range.highest()
        upper = upper + self.mod(upper)
        plot.y[pipe.KEY_LOWER] = lower
        plot.y[pipe.KEY_UPPER] = upper
        if price > upper:
            command = pipe.CMD_BUY
        elif price < lower:
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
        plot.y[pipe.KEY_LOWER] = None
        plot.y[pipe.KEY_UPPER] = None
        if self.is_first:
            self.is_first = False
            command = pipe.CMD_BUY
        return command
    
class SimpleMovingAverage():
    '''
    Signal BUY if instrument above average and vice versa
    '''
    
    def __init__(self, history, modifier):
        self.history = history
        self.modifier = modifier
        
    def process(self, price, plot):
        command = pipe.CMD_NONE
        average = self.history.mean()
        offset = self.modifier(average)
        plot.y[pipe.KEY_LOWER] = average - offset
        plot.y[pipe.KEY_UPPER] = average + offset
        if price > average + offset:
            command = pipe.CMD_BUY
        elif price < average - offset:
            command = pipe.CMD_SELL
        return command
    
class DualMovingAverage():
    '''
    Signal BUY if shorter average is above longer and vice versa
    '''
    # maintains type of last crossover:
    #    -1 -> top-down cross
    #    0  -> no cross
    #    1  -> bottom-up cross 
    def __init__(self, fast, slow, modifier):
        self.fast = fast
        self.slow = slow
        self.mod = modifier
        self.last_cross = 0     # type of last crossover
    
    def process(self, price, plot):
        command = pipe.CMD_NONE
        slow_avg = self.slow.mean()
        fast_avg = self.fast.mean()
        offset = self.mod(price)
        plot.y[pipe.KEY_LOWER] = slow_avg
        plot.y[pipe.KEY_UPPER] = fast_avg
        if fast_avg > slow_avg + offset:
            command = pipe.CMD_BUY
        elif fast_avg < slow_avg - offset:
            command = pipe.CMD_SELL
        return command
            
        