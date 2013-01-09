# Simple python REST client
# @author Chris Borckholder
import logging, sys
from socket import gaierror
from httplib import HTTPConnection, NotConnected, InvalidURL
from urllib import urlencode

log = logging.getLogger(__name__)

# supported HTTP verbs
METHOD_GET = "GET"
METHOD_PUT = "PUT"
METHOD_POST = "POST"
METHOD_DELETE = "DELETE"
METHOD_HEAD = "HEAD"

HTTP_PORT = 80

# factory method for rest clients
def create(host, port=HTTP_PORT):
    return Client(host, port)

# concatenates path fragments and params parameters to create an URL
def makeURL(fragments, params):
    queryString = "?"+ urlencode(params) if params else ""
    pathString =  "/"+ "/".join(fragments)
    url = pathString + queryString
    return url
      
class Client:

    def __init__(self, host, port=HTTP_PORT):
        self.header = {}
        self.params = {}
        self._conn = None
        self._root = host +":"+ str(port)
        self._path = []
  
    # fluent url creation
    # appends all arguments as path fragments
    def move(self, *to):
        self._path.extend(to)
        return self
    
    # removes the last path fragment
    def back(self):
        self._path = self._path[:-1]
        return self
    
    # removes all path fragments and params parameters
    def reset(self):
        self._path = []
        self.params = {}
        return self
    
    # appends a params parameter
    def query(self, key, value):
        self.params[key] = value
        return self
  
    # state getter
    # the currently set path, relative to the host given on creation
    def path(self):
        return makeURL(self._path, self.params)
  
    # the complete url that would be used in a request
    def url(self):
        return self._root + self.path()
  
    # HTTP verb impls
    # All requests will be sent to the current set resource
    def head(self):
        return self.request(METHOD_HEAD)
    
    def get(self):
        return self.request(METHOD_GET)
    
    def post(self, data=""):
        return self.request(METHOD_POST, data)
    
    def put(self, data=""):
        return self.request(METHOD_PUT, data)
    
    def delete(self):
        return self.request(METHOD_DELETE)
  
    # Sends a request to set service, returning a tuple of
    # ResponseMeta ( headers, status ), ResponseBody
    def request(self, method, body = "", header = {} , params = {} ):
        if not self._conn:
            raise NotConnected("Client not connected. Call .connect() before sending requests")
        headers = self.header.copy()
        headers.update(header)
        queries = self.params.copy()
        queries.update(params)
        resource = makeURL(self._path, queries)
        self._conn.request(method, resource, body, headers)
        meta = self._conn.getresponse()
        #data = meta.read()
        return meta
  
    def isConnected(self):
        return True if self._conn else False
  
    # establishes the HTTP connection
    def connect(self):
        if not self._conn:
            self._conn = HTTPConnection(self._root)
        try:
            self._conn.connect()
        except gaierror as cause:
            trace = sys.exc_info()[2]
            raise InvalidURL("Cannot connect to {} due to {}".format(self.url(), cause)), None, trace
        log.debug("Connected to %s", self._root)
        return self
    
    # closes the HTTP connection
    def disconnect(self):
        if self._conn:
            self._conn.close()
            self._conn = None
            log.debug("Disconnected from %s", self._root)
        return self
  
    # python magic
    def __str__(self):
        return "URL: "+ self.url() +"\nHeader: "+ str(self.header)
  
    def __enter__(self):
        self.connect()  
        return self
    
    def __exit__(self, type, value, traceback):
        self.disconnect()
    
    def __del__(self):
        self.disconnect()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log.info("Starting")
    c = create("vph1ds1.gridlab.univie.ac.at")
    log.info("Created %s", c)
    with c:
        c.move("test")
        log.info("Single move %s", c)
        c.move("1","2")
        log.info("Double move %s", c)
        c.header["Content-Type"] = "*/*"
        log.info("Set header %s", c)
        c.params["key"] = "value"
        log.info("Set params param %s", c)
        c.reset()
        log.info("Reset %s", c)
        response = c.get()
        log.info("GET %s \nResponse : %s \nStatus : %s \nBody : %s", c, response, response.status, response.read())
    log.info("Exiting")