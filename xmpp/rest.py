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
import threading
import BaseHTTPServer

class ApiRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    rest = None

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", 'text')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", 'text')
        self.end_headers()

        if self.path == '/control/close':
            self.wfile.write('Shutting Down...')
            ApiRequestHandler.rest.stop()
        elif self.path == '/control/status':
            self.wfile.write('Not implemented!')
        else:
            self.wfile.write('Path [%s] is not supported yet!' % self.path)

class RestServer(threading.Thread):
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
        threading.Thread.__init__(self)
        self._host = host
        self._port = port
        ApiRequestHandler.rest = self
        self._server = BaseHTTPServer.HTTPServer((self._host, self._port), ApiRequestHandler)

    def stop(self):
        """
        Stop the Rest Server
        """
        self._started = False

    def run(self):
        """
        Start the Http Server
        """
        if not self._started:
            self._started = True
            while(self._started):
                self._server.handle_request()
