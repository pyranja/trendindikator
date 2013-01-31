'''
Created on Jan 30, 2013

Mocks presenter interactions

@author: Pyranja
'''

class GraphView(object):
    
    def __init__(self):
        def print_a_thing(a_thing):
            print a_thing
        self.canvas = print_a_thing
    
    def notify(self, message):
        print message
        
    def report(self, text):
        print text

class IndicatorView(object):
    
    def __init__(self):
        pass
    
    @property
    def name(self):
        pass
        
    @name.setter
    def name(self, value):
        pass
    
    @property
    def signaler_type(self):
        pass
        
    @signaler_type.setter
    def signaler_type(self, value):
        pass
    
    @property
    def signal_threshold(self):
        pass
        
    @signal_threshold.setter
    def signal_threshold(self, value):
        pass
    
    @property
    def envelope_factor(self):
        pass
        
    @envelope_factor.setter
    def envelope_factor(self, value):
        pass
    
    @property
    def history_param1(self):
        pass
        
    @history_param1.setter
    def history_param1(self, value):
        pass
        
    @history_param1.deleter
    def history_param1(self):
        pass
    
    @property
    def history_param2(self):
        pass
        
    @history_param2.setter
    def history_param2(self, value):
        pass
        
    @history_param2.deleter
    def history_param2(self):
        pass

class MockView(object):
    '''
    main view - settings + graphics
    '''
    def __init__(self):
        self.freezed = False
        self.indicator1 = IndicatorView()
        self.indicator2 = IndicatorView()
        
    def freeze(self):
        if not self.freezed:
            print "FREEZING"
            self.freezed = True
        else:
            raise ValueError("Already freezed")
        
    def thaw(self):
        if self.freezed:
            print "THAWING"
            self.freezed = False
        else:
            raise ValueError("Not freezed")
        
    def notify(self, message):
        print message

    # --> index properties        
    @property
    def stock_symbol(self):
        pass
    
    @stock_symbol.setter
    def stock_symbol(self, value):
        pass

    @property
    def stock_start(self):
        pass
        
    @stock_start.setter
    def stock_start(self, value):
        pass
    
    @property
    def stock_end(self):
        pass
        
    @stock_end.setter
    def stock_end(self, value):
        pass
    
    # --> trader properties
    @property
    def ctrl_trader_mode(self):
        pass
        
    @trader_mode.setter
    def trader_mode(self, value):
        pass
    
    @property
    def ctrl_initial_funds(self):
        pass
        
    @initial_funds.setter
    def initial_funds(self, value):
        pass
    
    @property
    def dynamic(self):
        pass
        
    @dynamic.setter
    def dynamic(self, value):
        pass
    
    @property
    def reverse(self):
        pass
        
    @reverse.setter
    def reverse(self, value):
        pass
