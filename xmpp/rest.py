#===============================================================================
#
# The Rest API Server
# 
# @version 1.0
# @author Jack <guitarpoet@gmail.com>
# @date Sun May  3 19:59:48 2015
#
#===============================================================================

# Imports
import SimpleHTTPServer
import SocketServer

class ApiRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            print 'Hello'
        else:
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

class RestServer(object):
    """
    The Restful Http Server Thread
    """

    _started = False
    _server = None
    _host = None
    _port = 0;

    def __init__(self, host, port):
        """
        The constructor for Rest Server
        """
        config = ServiceLocator.Instance().config()
        self._host = host
        self._port = port
        self._server = SocketServer.TCPServer((self._host, self._port), ApiRequestHandler)

    def stop(self):
        """
        Stop the Rest Server
        """
        self.started = False
        self._server.shutdown_request()


    def start(self):
        """
        Start the Http Server
        """
        if not self._started:
            self._started = True
            self._server.serve_forever()
