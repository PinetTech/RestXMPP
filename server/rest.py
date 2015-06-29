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
                self.wfile.write('Shutting Down...\n')
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
                if self.rest._client.loggedin == False:
                    if self.rest._client.login():
                        self.wfile.write('Login Successfully!\n')
                    else:
                        self.wfile.write('Login failed, please check!\n')
                else:
                    self.wfile.write('Login already!\n')
            elif self.path == '/control/logout':
                if self.rest._client.loggedin == True:
                    self.rest._client.disconnect(wait=True)
                    self.wfile.write('Logout Successfully!\n')
                    self.rest._client.loggedin = False
                    self.rest._client.joinmuc = False
                else:
                    self.wfile.write('Logout already!\n')
            elif self.path == '/control/friends':
                if self.rest._client.loggedin == False:
                    self.wfile.write('Login first!\n')
                else:
                    self.control_friends('all')
            elif self.path == '/control/friends:online':
                if self.rest._client.loggedin == False:
                    self.wfile.write('Login first!\n')
                else:
                    self.control_friends('online')
            elif self.path == '/control/friends:offline':
                if self.rest._client.loggedin == False:
                    self.wfile.write('Login first!\n')
                else:
                    self.control_friends('offline')
				
            elif self.path == '/control/join':
                if self.rest._client.loggedin == False:
                    self.wfile.write('Login first!\n')
                else:
                    if self.rest._client.joinmuc == False:
                        self.rest._client.join_muc()
                        self.wfile.write('Join muc Successfully!\n')
                        self.rest._client.joinmuc = True
                    else:
                        self.wfile.write('Joined already!\n')
                        

            else:
                self.wfile.write('Path [%s] is not supported yet!\n' % self.path)

        except Exception as ex:
            self.send_response(400)
            self.wfile.write(ex.args)
            raise
       
    def control_friends(self,status):
        self.log = logging.getLogger('cement:app:xmpp')
        self.log.debug('get friends...', extra={'namespace': 'xmpp'})
        client = self.rest._client
        groups = client.client_roster.groups()
        self.log.debug('groups:%s'% groups, extra={'namespace': 'xmpp'})
        for group in groups:
            group_empty_flag = True
            if group == '':
                self.log.debug('group name empty!', extra={'namespace': 'xmpp'})
            self.wfile.write('\n\n[group]:%s\n' % group)
            self.wfile.write('-' * 72)
            for jid in groups[group]:
                if jid == client.jid:
                    continue
                subscription = client.client_roster[jid]['subscription']
                if subscription == 'none':
                    client.del_roster_item(jid)
                    continue
                connections = client.client_roster.presence(jid)
                self.log.debug('[jid]:%s'%jid, extra={'namespace': 'xmpp'})
                
                if connections == {} :
                    if status == 'offline' or status == 'all':
                        group_empty_flag = False
                        self.wfile.write('\n\n[jid]:              %s'%jid)
                        self.wfile.write('\n[status]:           offline')
                        self.wfile.write('\n[subscription]:     %s\n'%subscription)
                else:
                    if status == 'online' or status == 'all':
                        group_empty_flag = False
                        self.wfile.write('\n\n[jid]:              %s'%jid)
                        self.wfile.write('\n[status]:           online')
                        self.wfile.write('\n[subscription]:     %s\n'%subscription)
                    connections_items = connections.items()
                    self.log.debug('connections_items:%s' %connections_items, extra={'namespace': 'xmpp'})
            if group_empty_flag :
                self.wfile.write('\n no results in this group!\n')


class RestServer(threading.Thread):
    """
    The Restful Http Server Thread
    """

    _started = False
    _server = None
    _host = None
    _port = 0;
    _starttime = None

    def __init__(self, host, port, server, server_port, jid, password, friend_pattern, group, room, nick, auto_login):
        """
        The constructor for Rest Server
        """
        threading.Thread.__init__(self)
        self._host = host
        self._port = port
        ApiRequestHandler.rest = self
        self.log = logging.getLogger('cement:app:xmpp')
        self.log.debug('Rest Server Initialized before creat http server...', extra={'namespace': 'xmpp'})
        self.log.debug('host:%s... port :%s'%(self._host,self._port), extra={'namespace': 'xmpp'})
        self._server = BaseHTTPServer.HTTPServer((self._host, self._port), ApiRequestHandler)
        self.log = logging.getLogger('cement:app:xmpp')
        self.log.debug('server:%s... port :%s'%(self._server,self._port), extra={'namespace': 'xmpp'})
        self._client = Client(jid, password, server, server_port, friend_pattern, group, room, nick, auto_login)
        self.log.debug('client:%s... '%(self._client), extra={'namespace': 'xmpp'})
        self.log.debug('Rest Server Initialized...', extra={'namespace': 'xmpp'})
        self._starttime = datetime.datetime.now()
        self.log.debug('starttime:%s... '%(self._starttime), extra={'namespace': 'xmpp'})

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
