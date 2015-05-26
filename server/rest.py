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
import datetime

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
                self.wfile.write('host:             %s\n' % self.rest._host)
                self.wfile.write('h_port:           %s\n' % self.rest._port)
                self.wfile.write('login_status:     %s\n' % self.rest._client.loggedin)
                self.wfile.write('jid:              %s\n' % self.rest._client.jid)
                self.wfile.write('server:           %s\n' % self.rest._client._server)
                self.wfile.write('s_port:           %s\n' % self.rest._client._server_port)
                seconds = (datetime.datetime.now() - self.rest._starttime).seconds
                self.wfile.write('run:              %-3ddays %02d:%02d:%02d\n' % (seconds / 86400, (seconds % 86400) / 3600, (seconds % 3600) / 60, seconds % 60))


                
            elif self.path == '/xmpp/message':
                self.wfile.write(self.path)
            elif self.path == '/control/login':
                if self.rest._client.login():
                    self.wfile.write('Login Successfully!')
            elif self.path == '/control/logout':
                if self.rest._client.disconnect():
                    self.wfile.write('Logout Successfully!')
            elif self.path == '/control/friends':
                self.log = logging.getLogger('cement:app:xmpp')
                self.log.debug('get friends...', extra={'namespace': 'xmpp'})
                roster = self.rest._client.get_roster()
                self.rest._client.send_presence()
                self.log.debug('Roster:%s' % roster, extra={'namespace': 'xmpp'})
                groups = self.rest._client.client_roster.groups()
                self.log.debug('groups:%s'% groups, extra={'namespace': 'xmpp'})
                for group in groups:
                    if group!= '':
                        self.log.debug('group name empty!', extra={'namespace': 'xmpp'})
                    self.wfile.write('\n[group]:%s\n' % group)
                    self.wfile.write('-' * 72)
                    for jid in groups[group]:
                        self.wfile.write('\n[jid]:%s\n'%jid)
                        self.log.debug('[jid]:%s'%jid, extra={'namespace': 'xmpp'})
                        connections = self.rest._client.client_roster.presence(jid)
                        if connections == {} :
                            self.wfile.write('      [status:] offline')
                        else:
                            self.wfile.write('      [status:] online')
                        connections_items = connections.items()
                        self.log.debug('connections:%sconnections_items:%s' %(connections,connections_items), extra={'namespace': 'xmpp'})
                        """
                        for res, pres in connections_items:
                            self.log.debug('res:%spres:%sconnections_items:%sjid:%s' %(res,pres,connections_items,jid), extra={'namespace': 'xmpp'})
                            show = 'available'
                            if pres['show']:
                                show = pres['show']
                                self.log.debug('   - %s (%s)' % (res, show), extra={'namespace': 'xmpp'})
                                self.wfile.write('   - %s (%s)' % (res, show))
                            else:
                                self.log.debug('not found show', extra={'namespace': 'xmpp'})
                            if pres['status'] != '':
                                self.log.debug('[status]%s' % pres['status'], extra={'namespace': 'xmpp'})
                                self.wfile.write('      [status:] online')
                            else:
                                self.log.debug('not found status', extra={'namespace': 'xmpp'})
                                self.wfile.write('      [status:] offline')
                        """
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
    _starttime = None

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
        self._starttime = datetime.datetime.now()

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
