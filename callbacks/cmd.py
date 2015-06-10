from callback import Callback
import commands
import logging
import os

class Cmd(Callback):
    def __init__(self):
        self.log = logging.getLogger("cement:app:xmpp")
        self.log.debug('Cmd class creat object !', extra={'namespace' : 'xmpp'})

    def run(self, args = None):
        self.log.debug('args:%s'%args.items(), extra={'namespace' : 'xmpp'})
        cmd = args.get('cmd', 'not found')
        self.log.debug('cmd:%s  '%cmd, extra={'namespace' : 'xmpp'})
        if cmd != 'not found':
            (status, output) = commands.getstatusoutput(cmd)
            self.log.debug('[status]:%s  [output]:%s'%(status, output), extra={'namespace' : 'xmpp'})
            if status != 0:
                result = 'cmd execute error!'
            else :
                result = output
        return result 

    def ssh_bind(self, args = None):
        """
        ssh -R sourcePort:forwardToHost:onPort connectToHost
        """
        self.log.debug('args:%s'%args.items(), extra={'namespace' : 'xmpp'})
       
        source_port = args.get('source_port', '22')
        on_port = args.get('on_port', '9090')
        connect_to_host = args.get('connect_to_host', 'ibox@www.pinet.cc')
        path = '/usr/local/src/RestXMPP/bin/'
        cmd = 'cd %s ; sh ssh_xmpp %s %s %s '%(path, on_port, source_port, connect_to_host) 
        self.log.debug('cmd:%s  '%cmd, extra={'namespace' : 'xmpp'})
        os.system(cmd)
        result = 'OK SSH Tunnel'
        return result 
