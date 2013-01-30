'''
Created on 15.11.2012

example run of trend processing
expects table.csv in same directory

@author: Pyranja
'''
import os, core.indicator, core.trader

from core.index import CsvRepository
from datetime import date
from core import pipe

if __name__ == "__main__":
    repo = CsvRepository(os.getcwd())
    key = repo.fetch("AAPL", date(1990,1,1), date(2012,10,1))
    
    aPipe = pipe.PipeSpec()
    actor = pipe.Actor("test1")
    actor.trader = core.trader.create_trader(10000)
    actor.signaler = core.indicator.create_signaler(core.indicator.SIG_BREAK_RANGE, 0, 0, 5)
    aPipe.add(actor)
    actor = pipe.Actor("test2")
    actor.trader = core.trader.create_trader(10000)
    actor.signaler = core.indicator.create_signaler(core.indicator.SIG_BUY_HOLD, 0, 0)
    aPipe.add(actor)    
        
    index = repo.get(key)
    
    plot = aPipe.invoke(index)
    
    print "\n".join([str(point.x) + "|" + str(point.price) + ":" + str(point.get_all_contexts()) for point in plot])
    
