'''
Created on Jan 9, 2013

@author: Pyranja
'''
import os
from core.index import CsvRepository
from datetime import date

if __name__ == "__main__":
    index = CsvRepository(os.getcwd())
    print "built index"
    key = index.fetch("AAPL", date(2012,1,1), date(2012,10,1))
    print "got index"
    for day in index.get(key):
        print str(day[0]) + " : " + str(day[1])