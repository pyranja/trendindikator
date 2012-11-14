# core components test
import unittest, logging
import core.comps

SIZE = 3

class HistoryTest(unittest.TestCase):

    def setUp(self):
        self.subject = core.comps.History(SIZE)
    
    def test_initial(self):
        self.assertEqual([0] * 3, list(self.subject._values))
        self.assertEqual(0, self.subject.mean())
        self.assertEqual(0, self.subject.min())
        self.assertEqual(0, self.subject.max())
    
    def test_updating(self):
        self.subject.update(1)
        self.assertEqual([0,0,1], list(self.subject._values))
        self.subject.update(2)
        self.assertEqual([0,1,2], list(self.subject._values))
        self.subject.update(3).update(4)
        self.assertEqual([2,3,4], list(self.subject._values))
    
    def test_min(self):
        self.subject.update(1)
        self.assertEqual(0, self.subject.min())
        self.subject.update(2).update(3)
        self.assertEqual(1, self.subject.min())
    
    def test_max(self):
        self.assertEqual(0, self.subject.max())
        self.subject.update(1)
        self.assertEqual(1, self.subject.max())
        self.subject.update(2).update(3)
        self.assertEqual(3, self.subject.max())
    
    def test_mean(self):
        self.assertEqual(0, self.subject.mean())
        self.subject.update(1).update(1).update(1)
        self.assertEqual(1, self.subject.mean())
        self.subject.update(4)
        self.assertEqual(2, self.subject.mean())
        self.subject.update(4)
        self.assertEqual(3, self.subject.mean())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()