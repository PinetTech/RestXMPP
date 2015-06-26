#===============================================================================
#
# The XMPP Client
# 
# @version 1.0
# @author Jack <guitarpoet@gmail.com>
# @date Tue May  5 15:57:03 2015
#
#===============================================================================

# Imports
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from callback_hdl import callback_handle
import ssl
import logging
import json

class Client(ClientXMPP):

    class Meta:
        label = 'client'

    """
    The XMPP Client
    """
    
    def __init__(self, jid, password, server, server_port, friend_pattern, group, room, nick):
        """
        The constructor of the XMPP Client
        """

        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message, threaded=True)
        self.add_event_handler('presence_subscribe',
                               self.subscribe)
        self._password = password
        self._server = server
        self._server_port = server_port
        self._friend_pattern= friend_pattern 
        self._friend_default_group = group 
        self._connection = None
        self._auth = None
        self.loggedin = False
        self.joinmuc = False
        self._log = logging.getLogger("cement:app:xmpp")
        self.ssl_version = ssl.PROTOCOL_SSLv3
        self._log.info('XMPP client initialized...', extra={'namespace' : 'xmpp'})
        if self._server_port != 5222:
            self._log.info('server_port:%s is not default value!'%(self._server_port), extra={'namespace' : 'xmpp'})
        
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # XMPP Ping
        #Adapt the value of self.room when you test the conference
        self.room = room 
        self.nick = nick 

    def session_start(self, event):
        self.send_presence()
        try:
            self.get_roster()
            self._log.info('Now sending the message...', extra={'namespace' : 'xmpp'})
        except IqError as err:
            self._log.error('There was an error getting the roster')
            self._log.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            self._log.error('Server is taking too long to respond')
            self.disconnect()

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.
        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            self.analysis_msg(msg)

        elif msg['type'] == 'groupchat':
            self._log.info('Receive groupchat message:%s' %msg, extra={'namespace' : 'xmpp'})
            if msg['mucnick'] != self.nick:
                self.analysis_msg(msg)

        return 

    def analysis_msg(self,msg):
        msg_decode = msg['body'].decode('utf-8')
        self._log.debug('Receive msg_decode:%s' %msg_decode, extra={'namespace' : 'xmpp'})
        msg_ret = {}
        try:
            eval(msg_decode)
        except Exception,e :
            self._log.debug('is not json!!', extra={'namespace' : 'xmpp'})
            msg_ret['result'] = "msg is not json format!"
            self.reply_msg(msg,msg_ret) 
            return 
        try:
            data = json.loads(msg_decode)
        except TypeError, err:
            self._log.debug('error:%s' %err, extra={'namespace' : 'xmpp'})
            msg_ret['result'] = "msg load error!"
            self.reply_msg(msg,msg_ret) 
            return msg_ret
        for (k,v) in data.items(): 
            self._log.debug('val is :%s'%k, extra={'namespace' : 'xmpp'})
            if k == 'result':
                msg_ret['result'] = "is_reply"
                return 
        result = callback_handle(data)

        data[u'result'] = result.decode('utf-8')
        encodedjson = json.dumps(data)
        msg_ret = encodedjson.decode('ascii')
        self.reply_msg(msg,msg_ret) 
        return 

    def reply_msg(self,msg_src,msg_reply):
        msg_src.reply("\n%s" % msg_reply).send()
        return

    def login(self):
        """
        Login to jabber server
        """
        if self.connect((self._server,self._server_port),reattempt = False):
            self._log.info('Connected !...', extra={'namespace' : 'xmpp'})
            self.process()
            self.loggedin = True
            return True
        else:
            self.loggedin = False 
            self._log.info('Connect failed!...', extra={'namespace' : 'xmpp'})
            return False 

    def subscribe(self, pres):
        """
        handle the friend's addaaaaaaing and subscription request
        1.filtering friends according to the [friend_pattern],in cement config file
        2.[friend_default_group],in cement config file
        """
        domain = self._friend_pattern
        if domain == None:
            self._log.info('domain: is not configured', extra={'namespace' : 'xmpp'})
        else:
            self._log.info('domain:%s' %domain, extra={'namespace' : 'xmpp'})
        
        group = self._friend_default_group
        if group == None:
            self._log.info('group: is not configured', extra={'namespace' : 'xmpp'})
        else:
            self._log.info('group:%s' %group, extra={'namespace' : 'xmpp'})

        jid_from = pres['from']
        if  jid_from.domain == domain:
            self.auto_authorize = True
            self.auto_subscribe = True
            self.send_presence(pto=pres['from'],
                           ptype='subscribed')
            self._log.info('jid:%s subscribed '%jid_from,extra={'namespace' : 'xmpp'})
            self.update_roster(pres['from'], name=jid_from.username, groups=[group])
        else :
            self.auto_authorize = False 
            self.auto_subscribe = False
            self.send_presence(pto=pres['from'],
                           ptype='unsubscribed')
            self._log.info('jid:%s unsubscribed '%jid_from,extra={'namespace' : 'xmpp'})

    def join_muc(self):
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)
        self._log.info('JoinMUC, room:%s' %self.room, extra={'namespace' : 'xmpp'})
        



