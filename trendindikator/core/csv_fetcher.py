# yahoo finance .csv fetcher
# @author Chris Borckholder
import logging, rest, csv

YAHOO_HOST = "ichart.yahoo.com"
YAHOO_APP = "table.csv"
STOCK = "AAPL"
FROM = "01012012"
TILL = "01102012"

def map_date(keys, date_parts):
    mapped = {}
    [mapped.update({pair[0] : pair[1]}) for pair in zip(keys, date_parts)]
    return mapped

if __name__ == "__main__":
    with rest.create(YAHOO_HOST) as c, open("table.csv","wb") as sink:
        c.move(YAHOO_APP)
        c.query("s",STOCK).query("ignore",".csv")
        c.params.update(map_date(["a","b","c"],[1,1,2012]))
        c.params.update(map_date(["d","e","f"],[10,1,2012]))
        c.query("g","d")
        resp = c.get()
        print("Status :", resp.status)
        sink.write(resp.read())
    with open("table.csv","r") as source:
        reader = csv.reader(source)
        print [row for row in reader]