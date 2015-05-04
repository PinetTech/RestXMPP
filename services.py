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
from xmpp import RestServer, ControlServer

# The Base Controller
class ServiceController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = 'This is the control interface for RestXMPP server.'

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        print self._usage_text

    @controller.expose(help='Start the RestXMPP service, if the service is already running, will skip')
    def start(self):
        self.app.log.info('Starting Control Server...')
        ServiceLocator.Instance().control().start()

    @controller.expose(help='Stop the RestXMPP Service, if the service is no running already, will skip')
    def stop(self):
        self.app.log.info('Stopping RestXMPP Service')

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
            defaults['xmpp']['control_host'] = '127.0.0.1'
            defaults['xmpp']['control_port'] = 1080

            # Initialize the application object
            self._app = App('xmpp', config_defaults=defaults)
        return self._app
    
    def config(self):
        """
        The Application Config
        """

        return self.app().config
    
    def control(self):
        """
        The Control Service
        """
        if self._control == None:
            self._control = ControlServer(self.app().config.get('xmpp', 'control_host'),
                    self.app().config.get('xmpp', 'control_port'))
        return self._control

    def rest(self):
        """
        The Rest Service
        """

        if self._rest == None:
            self._rest = RestServer(self.app().config.get('xmpp', 'host'),
                    self.app().config.get('xmpp', 'port'))
        return self._rest
