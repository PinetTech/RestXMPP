from callback import Callback
import commands
import logging

class Cmd(Callback):
    def __init__(self):
        self.log = logging.getLogger("cement:app:xmpp")

    def run(self, args = None):
        self.log.debug('args:%s'%args.items(), extra={'namespace' : 'xmpp'})
        
        cmd = args.get('cmd', 'not found')

        self.log.debug('cmd:%s  '%cmd, extra={'namespace' : 'xmpp'})
        if cmd != 'not found':
            (status, output) = commands.getstatusoutput(cmd)
            self.log.debug('[status]:%s  [output]:%s'%(status,output), extra={'namespace' : 'xmpp'})
            if status != 0:
                result = 'cmd execute error!'
            else :
                result = output
        return result 

    def ssh_bind(self, args = None):
        """
        ssh -R <local port>:<remote host>:<remote port> <SSH hostname>
        ssh -R sourcePort:forwardToHost:onPort connectToHost
        """
        self.log.debug('args:%s'%args.items(), extra={'namespace' : 'xmpp'})
       
        source_port = args.get('source_port', '22')
        on_port = args.get('on_port', '9090')
        connect_to_host = args.get('connect_to_host', 'ibox@www.pinet.cc')
        cmd = 'ssh -R %s:localhost:%s %s'%(source_port,on_port,connect_to_host) 
        self.log.debug('cmd:%s  '%cmd, extra={'namespace' : 'xmpp'})
        (status, output) = commands.getstatusoutput(cmd)
        self.log.debug('[status]:%s  [output]:%s'%(status,output), extra={'namespace' : 'xmpp'})
        if status != 0:
            result = 'cmd execute error!'
        else :
                result = output
        return result 

