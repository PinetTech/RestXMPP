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
import logging
import BaseHTTPServer
import cgi
from client import Client

class ApiRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    rest = None

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", 'text')
        self.end_headers()
    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", 'text')
            self.end_headers()

            if self.path == '/xmpp/message':
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                if ctype == 'multipart/form-data':
                    postvars = cgi.parse_multipart(self.rfile, pdict)
                elif ctype == 'application/x-www-form-urlencoded':
                    length = int(self.headers.getheader('content-length'))
                    postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                else:
                    postvars = {}
                jid = postvars['jid'][0]
                message = postvars['message'][0]
                if self.rest._client.loggedin:
                    self.rest._client.send_message(mto=jid, mbody=message)
                    self.wfile.write('message [%s] to [%s] sent...' % (message, jid))
                else:
                    self.wfile.write('Please login first...')
            else:
                self.wfile.write('Path [%s] is not supported yet!' % self.path)
        except Exception as ex:
            self.send_response(400)
            self.wfile.write(ex.args)
            raise

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", 'text')
            self.end_headers()

            if self.path == '/control/stop':
                self.wfile.write('Shutting Down...')
                ApiRequestHandler.rest.stop()
            elif self.path == '/control/status':
                self.wfile.write('Not implemented!')
            elif self.path == '/xmpp/message':
                self.wfile.write(self.path)
            elif self.path == '/control/login':
                if self.rest._client.login():
                    self.wfile.write('Login Successfully!')
            elif self.path == '/control/logout':
                if self.rest._client.disconnect():
                    self.wfile.write('Logout Successfully!')
            elif self.path == '/control/friends':
                    self.rest._client.browse_roster()
                    groups = self.rest._client._groups
                    self.wfile.write('\nRoster\n')
                    for group in groups:
                        self.wfile.write('\n%s\n' % group)
                        self.wfile.write('-' * 72)
                        for jid in groups[group]:
                            self.wfile.write('\n[jid]:%s\n'%jid)
                            connections_items = self.rest._client._connections_items
                            for res, pres in connections_items:
                                self.wfile.write('\n victor debug\n' )
                                show = 'available'
                                if pres['show']:
                                    show = pres['show']
                                    #print('   - %s (%s)' % (res, show))
                                    self.wfile.write('   - %s (%s)' % (res, show))
                                else:
                                    self.wfile.write(' \nnot found show\n')
                                if pres['status']:
                                    #print('       %s' % pres['status'])
                                    self.wfile.write('       %s' % pres['status'])
                                else:
                                    self.wfile.write(' \nnot found status\n')
                    
            else:
                self.wfile.write('Path [%s] is not supported yet!' % self.path)

        except Exception as ex:
            self.send_response(400)
            self.wfile.write(ex.args)
            raise

class RestServer(threading.Thread):
    """
    The Restful Http Server Thread
    """

    _started = False
    _server = None
    _host = None
    _port = 0;

    def __init__(self, host, port, server, server_port, jid, password):
        """
        The constructor for Rest Server
        """
        threading.Thread.__init__(self)
        self._host = host
        self._port = port
        ApiRequestHandler.rest = self
        self._server = BaseHTTPServer.HTTPServer((self._host, self._port), ApiRequestHandler)
        self.log = logging.getLogger('cement:app:xmpp')
        self._client = Client(jid, password, server, server_port)
        self.log.debug('Rest Server Initialized...', extra={'namespace': 'xmpp'})

    def stop(self):
        """
        Stop the Rest Server
        """
        self.log.debug('Disconnecting XMPP Client...', extra={'namespace': 'xmpp'})
        self._started = False
        self._client.disconnect()

    def run(self):
        """
        Start the Http Server
        """
        if not self._started:
            self._started = True
            while(self._started):
                self._server.handle_request()
