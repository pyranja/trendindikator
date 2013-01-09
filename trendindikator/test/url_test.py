# rest client url building test
# @author Chris Borckholder
import unittest, logging
import core.rest as rest

HOST = "www.example.com"
FULL_HOST = "www.example.com:80"

class TestRestUrlBuilding(unittest.TestCase):
  
    def setUp(self):
        self.subject = rest.create(HOST)
    
    def test_initial(self):
        self.assertEqual("/", self.subject.path())
        self.assertEqual(FULL_HOST + "/", self.subject.url())
    
    def test_single_move(self):
        self.subject.move("one")
        self.assertEqual("/one", self.subject.path())
    
    def test_consecutive_move(self):
        self.subject.move("one")
        self.subject.move("two")
        self.assertEqual("/one/two", self.subject.path())
    
    def test_triple_move_in_one(self):
        self.subject.move("one","two","three")
        self.assertEqual("/one/two/three", self.subject.path())
    
    def test_back_in_initial_state_does_nothing(self):
        self.subject.back()
        self.assertEqual("/", self.subject.path())
        self.assertEqual(FULL_HOST + "/", self.subject.url())
    
    def test_back_removes_single_fragment(self):
        self.subject.move("test")
        self.subject.back()
        self.assertEqual("/", self.subject.path())
    
    def test_back_only_removes_last_fragment(self):
        self.subject.move("test","remove")
        self.subject.back()
        self.assertEqual("/test", self.subject.path())
    
    def test_add_a_single_query_param(self):
        self.subject.query("key", "value")
        self.assertEqual( { "key" : "value" }, self.subject.params)
        self.assertEqual("/?key=value", self.subject.path())
    
    def test_query_param_is_after_last_path_fragment(self):
        self.subject.query("key", "value")
        self.subject.move("test")
        self.assertEqual("/test?key=value", self.subject.path())
    
    def test_reset_clears_path_and_query(self):
        self.subject.query("key", "value")
        self.subject.move("test","test")
        self.subject.reset()
        self.assertEqual("/", self.subject.path())
        self.assertEqual(FULL_HOST + "/", self.subject.url())
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()