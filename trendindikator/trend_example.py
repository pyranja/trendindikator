'''
Created on 15.11.2012

example run of trend processing
expects table.csv in same directory

@author: Pyranja
'''
import csv
import core.comps as comps
import core.strategies as strats

if __name__ == "__main__":
    sink = comps.DataSink()
    trader = comps.Trader(strats.createSingleIndexBuySellTrader(10), sink)
    trend = comps.Signaller(strats.createBreakRangeIndicator(3, [1,2,3]), trader, sink)
    with open("table.csv","r") as source:
        reader = csv.DictReader(source)
        for idx, row in enumerate(reader):
            trend.process(None, idx, float(row["Adj Close"]))
    #print "Profit over all: ", sum([profit[1] for profit in sink.data[comps.KEY_PROFIT]])
    print sink.data
    
