#===============================================================================
#
# The Control Server
# 
# This is the control server that runs for the controlling method
# 
# @version 1.0
# @author Jack <guitarpoet@gmail.com>
# @date Sun May  3 22:56:11 2015
#
#===============================================================================

# Imports
import threading
import SimpleHTTPServer
import SocketServer

class ControlRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print self

class ControlServer(threading.Thread):
    """
    The Controller Server
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
        self._server = SocketServer.TCPServer((self._host, self._port), ControlRequestHandler)

    def stop(self):
        """
        Stop the Rest Server
        """
        self.started = False

    def run(self):
        """
        Start the Http Server
        """
        if not self._started:
            self._server.serve_forever()
            self._started = True
