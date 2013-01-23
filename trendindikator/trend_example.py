'''
Created on 15.11.2012

example run of trend processing
expects table.csv in same directory

@author: Pyranja
'''
import csv, os, core.indicator, core.trader
import core.pipe as pipe

from core.index import CsvRepository
from datetime import date

if __name__ == "__main__":
    repo = CsvRepository(os.getcwd())
    key = repo.fetch("AAPL", date(1990,1,1), date(2012,10,1))
    
    signaller, histories = core.indicator.create_signaler(core.indicator.SIG_BREAK_RANGE, 0, 0, 5)
    #signaller, histories = core.indicator.create_signaler(core.indicator.SIG_BUY_HOLD, 0, 0)
    trader = core.trader.create_trader(1000)
    
    index = repo.get(key)
    
    plot = pipe.process(index, [(signaller, trader)], histories)
    
    print "\n".join([str(p.x) + ":" + str(p.y) for p in plot]) 
    print "sum of profit :"+ str(sum([p.y[pipe.KEY_PROFIT] for p in plot]))
    
