'''
Created on Jan 8, 2013

@author: Pyranja
'''
import csv, os
from datetime import datetime
from core import rest

# connection parameter for yahoo API
YAHOO_HOST = "ichart.yahoo.com"
YAHOO_APP = "table.csv"

def yahoo_fetcher(stock, start, end):
    with rest.create(YAHOO_HOST) as c:
        c.move(YAHOO_APP)
        c.query("s",stock).query("ignore",".csv")
        c.params.update(map_date(["a","b","c"],start))
        c.params.update(map_date(["d","e","f"],end))
        c.query("g","d")
        resp = c.get()
        if not resp.status == 200:
            raise IOError("Failed to fetch index data. Error code : %i" % resp.status)
        return resp.read()

# helper to fill date url parameters
# months are zero based !
def map_date(keys, date):
    mapped = {}
    date_parts = [ date.month - 1, date.day, date.year ]
    [mapped.update({pair[0] : pair[1]}) for pair in zip(keys, date_parts)]
    return mapped

# yahoo index date format
DATE_FORMAT = "%Y-%m-%d"

'''
Iterates an index file
'''
def index_generator(filename):
    with open(filename,"r") as source:
        reader = csv.DictReader(source)
        for row in reversed(list(reader)):
            date = datetime.strptime(row["Date"], DATE_FORMAT)
            price = float(row["Adj Close"])
            yield date, price

class CsvRepository(object):
    '''
    Manages index data using .csv files. 
    Offers CRUD operations on indexes and is able to fetch index data from the
    YAHOO finance webservice.  
    '''

    def __init__(self, base, fetcher = yahoo_fetcher):
        '''
        Creates a repository in given directory
        @param base: directory where .csv should be stored
        @param fetcher: optional fetcher implementation for stock data 
        '''
        self.__base = base
        if not os.path.exists(base):
            raise IOError("invalid index base directory ["+ base +"]")
        self.__fetcher = fetcher
        self.__indices = {}
        self.__next_key = 0
        
    def fetch(self, stock, start, end):
        '''
        Attempts to fetch index data for the given stock name and date range
        @param stock: symbol of desired stock
        @param start: starting date
        @param end: ending date 
        @return: key of created index on success
        @raise exception: on webservice call failure or io failure 
        '''
        key = str(self.__next_key)
        self.__next_key += 1
        filename = self.__base + "/index-" + key + ".csv"
        with open(filename, "wb") as sink:
            sink.write(self.__fetcher(stock, start, end))
        self.__indices[key] = filename
        return key
    
    def get(self, key):
        '''
        @return: a generator yielding the data of the index with given key
        '''
        filename = self.__indices[key]
        return index_generator(filename)
    
    def delete(self, key):
        '''
        Deletes the index with given key
        '''
        filename = self.__indices.pop(key, None)
        if filename:
            try:
                os.remove(filename)
            except:
                pass # same effect
    
    def clear(self):
        '''
        Deletes all existing indices
        '''
        for filename in self.__indices.itervalues():
            try:
                os.remove(filename)
            except:
                pass # same effect
        self.__indices.clear()
            