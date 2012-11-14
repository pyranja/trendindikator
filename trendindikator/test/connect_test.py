# rest client connection test
# @author Chris Borckholder
import unittest, logging
import core.rest as rest

from httplib import InvalidURL

VALID_HOST = "www.google.com"
INVALID_HOST = "www.invalid-url.net"

class TestRestConnecting(unittest.TestCase):

    def setUp(self):
        self.subject = None
    
    def tearDown(self):
        if self.subject:
            self.subject.disconnect()
  
    def test_is_disconnected_before_connecting(self):
        self.subject = rest.create(INVALID_HOST)
        self.assertFalse(self.subject.isConnected())
    
    def test_can_connect_to_valid(self):
        self.subject = rest.create(VALID_HOST)
        self.subject.connect()
        self.assertTrue(self.subject.isConnected())
    
    def test_invalid_host_fails_on_connecting(self):
        self.subject = rest.create(INVALID_HOST)
        with self.assertRaises(InvalidURL):
            self.subject.connect()
      
    def test_context_autoconnects(self):
        with rest.create(VALID_HOST) as client:
            self.assertTrue(client.isConnected())
      
    def test_head_fetches_no_body(self):
        with rest.create(VALID_HOST) as c:
            response = c.head()
            self.assertTrue(response.status < 400)
            self.assertEqual(0, len(response.read()))
  
    def test_get_fetches_a_body(self):
        with rest.create(VALID_HOST) as c:
            response = c.get()
            self.assertTrue(response.status < 400)
            self.assertTrue(len(response.read()) > 0)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()