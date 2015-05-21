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
import ssl
import logging
import threading

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
        #self.add_event_handler("session_start", self.session_start)
	#victor changed to:
        self.add_event_handler("session_start", self.session_start,threaded=True)
        self.add_event_handler("message", self.message)
        self.add_event_handler("changed_status", self.wait_for_presences)

        self._password = password
        self._server = server
        self._server_port = server_port
        self._connection = None
        self._auth = None
        self.loggedin = False
        self._log = logging.getLogger("cement:app:xmpp")
        self.ssl_version = ssl.PROTOCOL_SSLv3
        self._log.info('XMPP client initialized...', extra={'namespace' : 'xmpp'})
        """
        victor add 
        """
        self._groups = {}
        self._connections = {}
        self._connections_items = {}
        self.name = None
        #self._auth = None

        self.received = set()
        self.presences_received = threading.Event()

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
            msg.reply("Thanks for sending\n%(body)s" % msg).send()
    

    def login(self):
        """
        Login to jabber server
        """
        self.connect()
        self.process()
        self.loggedin = True
        return True

    def browse_roster(self):
        """
        victor add for browse roster
        """
        print('Waiting for presence updates...\n')
        self.presences_received.wait(5)
        print('Roster for %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        self._groups = groups
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                
                if self.client_roster[jid]['name']:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    print(' %s [%s]' % (jid, sub))

                connections = self.client_roster.presence(jid)
                self._connections = connections
                self._connections_items = connections.items()
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - victor debug:%s (%s)' % (res, show))
                    if pres['status']:
                        print('   victor debug    %s' % pres['status'])

        #self.disconnect()

        
    def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

