'''
Created on Jan 30, 2013

financial math impls

@author: Pyranja
'''
import core.pipe
import math

class Statistics(object):
    
    def __init__(self, name, initial_funds):
        self.name = name
        self.initial_funds = initial_funds
        self.tx_count = 1
        self.total_yield = 0
        self.min_yield = None
        self.max_yield = None
        self.periods = 0
        self.volatility = 0
        self.last_yield = None
        
    def feed(self, points, context_name):
        daily_yields = []
        for point in points:
            point.context = context_name
            self.tx_count += 1 if point.y[core.pipe.KEY_ACTION] == core.pipe.ACTION_CLEAR else 0
            current_yield = point.y[core.pipe.KEY_YIELD]
            self._track_min_max(current_yield)
            daily_yields = self._track_yields(current_yield, daily_yields)
            self.total_yield = current_yield
        self.total_yield -= self.initial_funds
        if self.periods < 1:
            self.periods = 1
        self._calc_volatility(daily_yields)
        if self.min_yield is None:
            self.min_yield = 0
        if self.max_yield is None:
            self.max_yield = 0
            
    def _calc_volatility(self, daily_yields):
        arith_yield_average = (1 / self.periods) * math.fsum(daily_yields)
        squared_yield_spreads = [(days_yield - arith_yield_average) ** 2 for days_yield in daily_yields]
        self.volatility = (1 / self.periods) * math.fsum(squared_yield_spreads)
        self.volatility = math.sqrt(self.volatility) / 100
            
    def _track_yields(self, current_yield, daily_yields):
        if self.last_yield is not None:
            if self.last_yield > 0 or self.last_yield < 0:
                self.periods += 1
                yield_change = (current_yield - self.last_yield) / self.last_yield * 100
                daily_yields.append(yield_change)
        self.last_yield = current_yield
        return daily_yields
    
    def _track_min_max(self, current_yield):
        if self.min_yield is None:
            self.min_yield = current_yield
        elif current_yield is not None:
            self.min_yield = min(current_yield, self.min_yield)
        if self.max_yield is None:
            self.max_yield = current_yield
        elif current_yield is not None:
            self.max_yield = max(current_yield, self.max_yield)
            
    @property
    def relative_yield(self):
        return self.total_yield / self.initial_funds + 1
        
    @property
    def average_yield(self):
        relative_yield = self.relative_yield
        sign = 1
        if relative_yield < 0:
            sign = -1
            relative_yield = math.fabs(relative_yield)
        return sign * (relative_yield ** (1.0 / self.periods) - 1)
    