#===============================================================================
#
# The Service Locator
# 
# @version 1.0
# @author Jack <guitarpoet@gmail.com>
# @date Sun May  3 21:34:27 2015
#
#===============================================================================

from cement.core import backend, foundation, controller, handler
from cement.utils.misc import init_defaults
from utils import Singleton
from server import RestServer
import requests
import logging

# The Service Controller
class ServiceController(controller.CementBaseController):
    """
    This is the Application Controller for the RestXMPP Application

    @author Jack
    @version 1.0
    @date Tue May  5 13:14:35 2015
    """

    class Meta:
        label = 'base'
        description = 'This is the control interface for RestXMPP server.'

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        """
        This is the default commmand when no command is set.
        """

        print self._usage_text

    @controller.expose(help='Start the RestXMPP service, if the service is already running, will skip')
    def start(self):
        """
        This command will start the RestXMPP service
        """

        self.app.log.info('Starting RestXMPP Service...')
        rest = ServiceLocator.Instance().rest()
        self.app.log.info('rest:%s...'%(rest))
        if rest:
            rest.start()
            self.app.log.info('RestXMPP Started...')
            # Waiting RestXMPP to stop
            rest.join();
            self.app.log.info('RestXMPP Stopped...')
        else:
            self.app.log.info('RestXMPP Start Failed')

    @controller.expose(help='Stop the RestXMPP Service, if the service is no running already, will skip')
    def stop(self):
        """
        This command will stop the RestXMPP Service
        """

        self.app.log.info('Stopping RestXMPP Service...')
        port = self.app.config.get('xmpp', 'port')
        try:
            r = requests.get('http://localhost:%s/control/stop' % port)
            if r.status_code == 200:
                self.app.log.info('RestXMPP Service Stopped.')
            else:
                self.app.log.info('RestXMPP Service Stop Failed!')
        except(requests.exceptions.ConnectionError):
            self.app.log.info('RestXMPP Service Not Started!')


    @controller.expose(help='Check for the status of RestXMPP Service')
    def status(self):
        self.app.log.info('Testing RestXMPP Service')


# The Application
class App(foundation.CementApp):
    class Meta:
        label = 'xmpp'
        base_controller = ServiceController
        arguments_override_config=True

@Singleton
class ServiceLocator:
    """
    The Service Locator
    """

    _app = None
    _rest = None
    _control = None

    def app(self):
        """
        The Aplication
        """

        if self._app == None:
            # Setting up the defaults
            defaults = init_defaults('xmpp')
            defaults['xmpp']['host'] = 'localhost'
            defaults['xmpp']['port'] = 8080
            defaults['xmpp']['jid'] = None
            defaults['xmpp']['password'] = None
            defaults['xmpp']['server'] = None
            defaults['xmpp']['server_port'] = 5222
            defaults['xmpp']['friend_pattern'] = 'pinet.cc' 
            defaults['xmpp']['friend_default_group'] = 'pinet_friends'
            defaults['xmpp']['room'] = "misc@conference.pinet.cc"
            defaults['xmpp']['nick'] = "test1" 

            # Initialize the application object
            self._app = App('xmpp', config_defaults=defaults)
        return self._app
    
    def config(self):
        """
        The Application Config
        """

        return self.app().config

    def log(self):
        return self.app().log
    
    def rest(self):
        """
        The Rest Service
        """

        if self._rest == None:
            config = self.config()
            self.log().info('config:%s'%config)
            jid = config.get('xmpp', 'jid')
            password = config.get('xmpp', 'password')
            server = config.get('xmpp', 'server')
            server_port = config.get('xmpp', 'server_port')
            friend_pattern = config.get('xmpp', 'friend_pattern')
            group = config.get('xmpp', 'friend_default_group')
            room = config.get('xmpp', 'room')
            nick = config.get('xmpp', 'nick')
            self.log().info('jid:%s password:%s server:%s server_port:%s friend_pattern:%s group:%s room:%s nick:%s'%(jid, password, server, server_port, friend_pattern, group, room, nick))
            if not server:
                self.log().info('Can\'t find jabber server configuration')
                return None
            if not jid:
                self.log().info('Can\'t find jid configuration')
                return None
            if not password:
                self.log().info('Can\'t find password configuration')
                return None

            host = self.app().config.get('xmpp', 'host')
            port_str = self.app().config.get('xmpp', 'port')
            port =  int(port_str)
            self.log().info('host:%s port :%s'%(host, port ))
            self._rest = RestServer(host,port, server, server_port, jid, password, friend_pattern, group, room, nick) 
            self.log().info('self._rest:%s '%(self._rest))
        return self._rest
