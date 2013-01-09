'''
Created on 15.11.2012

@author: Pyranja
'''
import unittest 
import core.comps as comps
import core.strategies as strats

class Test(unittest.TestCase):

    def setUp(self):
        self.sink = comps.DataSink()
        trader = comps.Trader(strats.createSingleIndexBuySellTrader(10), self.sink)
        self.core = comps.Signaller(strats.createBreakRangeIndicator(3, [1,2,3]), trader, self.sink)

    def tearDown(self):
        pass

    def test_should_do_nothing(self):
        self.core.process(None, 1, 2)
        self.assertEqual([comps.NONE], self.sink.data[comps.KEY_COMMAND])
        self.assertEqual([(1,1)], self.sink.data["low"])
        self.assertEqual([(1,3)], self.sink.data["high"])
        
    def test_should_buy(self):
        self.core.process(None, 1, 4)
        self.assertEqual([comps.BUY], self.sink.data[comps.KEY_COMMAND])
        self.assertEqual([(1,1)], self.sink.data["low"])
        self.assertEqual([(1,3)], self.sink.data["high"])
        
    def test_should_buy_then_sell(self):
        self.core.process(None, 1, 4)
        self.assertEqual([comps.BUY], self.sink.data[comps.KEY_COMMAND])
        self.assertEqual([(1,1)], self.sink.data["low"])
        self.assertEqual([(1,3)], self.sink.data["high"])
        self.core.process(None, 2, 1)
        self.assertEqual([comps.BUY, comps.SELL], self.sink.data[comps.KEY_COMMAND])
        self.assertEqual([(1,1),(2,2)], self.sink.data["low"])
        self.assertEqual([(1,3),(2,4)], self.sink.data["high"])
        self.assertEqual([(2,-6)], self.sink.data[comps.KEY_PROFIT])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()