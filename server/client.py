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
    
    def __init__(self, jid, password, server, server_port):
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
        self._connection = None
        self._auth = None
        self.loggedin = False
        self.joinmuc = False
        self._log = logging.getLogger("cement:app:xmpp")
        self.ssl_version = ssl.PROTOCOL_SSLv3
        self._log.info('XMPP client initialized...', extra={'namespace' : 'xmpp'})
        
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # XMPP Ping
        #Adapt the value of self.room when you test the conference
        self.room = "misc@conference.pinet.cc"
        self.nick = "test2"

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
            msg_decode = msg['body'].decode('utf-8')
            self._log.debug('Receive msg_decode:%s' %msg_decode, extra={'namespace' : 'xmpp'})
            data = json.loads(msg_decode)
            callback_handle(data)
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

        elif msg['type'] == 'groupchat':
            self._log.info('Receive groupchat message:%s' %msg, extra={'namespace' : 'xmpp'})
            if msg['mucnick'] != self.nick:
                self.send_message(mto=msg['from'].bare,
                                  mbody="I heard that, %s." % msg['mucnick'],
                                  mtype='groupchat')
    

    def login(self):
        """
        Login to jabber server
        """
        self.connect()
        self.process()
        self.loggedin = True
        return True

    def subscribe(self, pres):
        """
        handle the friend's addaaaaaaing and subscription request
        1.filtering friends according to the [friend_pattern],undetermined 
        2.[friend_default_group]:'pinet'
        """
        jid_from = pres['from']
        if  (jid_from.domain == 'pinet.cc' or jid_from.domain == 'localhost') and jid_from.username != 'user_abc':
            self.auto_authorize = True
            self.auto_subscribe = True
            self.send_presence(pto=pres['from'],
                           ptype='subscribed')
            self._log.info('jid:%s subscribed '%jid_from,extra={'namespace' : 'xmpp'})
            self.update_roster(pres['from'], name=jid_from.username, groups=['pinet'])
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



        