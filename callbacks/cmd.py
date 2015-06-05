from callback import Callback
import commands
import logging
import os

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
        ssh -R sourcePort:forwardToHost:onPort connectToHost
        """
        self.log.debug('args:%s'%args.items(), extra={'namespace' : 'xmpp'})
       
        source_port = args.get('source_port', '22')
        on_port = args.get('on_port', '9090')
        connect_to_host = args.get('connect_to_host', 'ibox@www.pinet.cc')
        cmd = 'ssh -R %s:localhost:%s %s -Nf'%(on_port,source_port,connect_to_host) 
        #cmd = 'ssh -R -Nf 9091:localhost:22 spirit@192.168.20.138'
        self.log.debug('cmd:%s  '%cmd, extra={'namespace' : 'xmpp'})

        try:
            pid = os.fork()
            if pid == 0: 
                self.log.debug('this is child process', extra={'namespace' : 'xmpp'})
                (status, output) = commands.getstatusoutput(cmd)
                self.log.debug('[status]:%s  [output]:%s'%(status,output), extra={'namespace' : 'xmpp'})
                if status != 0:
                    result = 'cmd execute error!'
                else :
                    result = 'OK'+output

            else: 
                result = 'OK parent'
                self.log.debug('this is parent process', extra={'namespace' : 'xmpp'})
        except:
            result = 'fork error!'
        return result 

