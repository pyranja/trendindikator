'''
Created on Jan 8, 2013

@author: Pyranja
'''
import unittest, os
from core.index import CsvRepository
from datetime import datetime

def mock_fetcher(p1, p2, p3):
    return "Date,Adj Close\n2013-01-02,2.5\n2012-11-01,1.0\n"

class Test(unittest.TestCase):


    def setUp(self):
        test_dir = os.getcwd() + "\\index_test"
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        self.subject = CsvRepository(test_dir, mock_fetcher)


    def tearDown(self):
        self.subject.clear()


    def test_get_fails_on_invalid_key(self):
        with self.assertRaises(KeyError):
            self.subject.get("INVALID")
        
    def test_delete_no_fail_on_invalid_key(self):
        self.subject.delete("INVALID")
        
    def test_getting_existing(self):
        key = self.subject.fetch(None, None, None)
        self.assertIsNotNone(self.subject.get(key))
        
    def test_get_gives_generator(self):
        key = self.subject.fetch(None, None, None)
        data = self.subject.get(key)
        self.assertEquals((datetime(2012,11,01),1.0), data.next())
        self.assertEquals((datetime(2013,01,02),2.5), data.next())
        
    def test_get_fails_after_delete(self):
        key = self.subject.fetch(None, None, None)
        data = self.subject.get(key)
        self.assertEqual(2, len(list(data)))
        self.subject.delete(key)
        with self.assertRaises(KeyError):
            self.subject.get(key)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()