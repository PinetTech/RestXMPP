from callback import Callback
import commands
import logging
import subprocess

class Download(Callback):
    def __init__(self):
        self.log = logging.getLogger("cement:app:xmpp")

    def download(self, args = None):
        self.log.info('downloading initialized...', extra={'namespace' : 'xmpp'})
        self.log.debug('args:%s'%args.items(), extra={'namespace' : 'xmpp'})
        
        url = args.get('url', 'not found')
        filename = args.get('filename', 'not found')
        path = args.get('path', '/home/download')
        md5 = args.get('md5', 'not found')
        ok_hdl = args.get('ok_hdl', 'not found')
        err_hdl = args.get('err_hdl', 'not found')

        cmd = 'cd %s ; wget -t 5 -T 20 -c %s%s'%(path,url,filename)
        self.log.debug('cmd:%s  '%cmd, extra={'namespace' : 'xmpp'})
        self.log.info('downloading ...', extra={'namespace' : 'xmpp'})
        (status, output) = commands.getstatusoutput(cmd)
        self.log.debug('[status]:%s  [output]:%s'%(status,output), extra={'namespace' : 'xmpp'})
        if status != 0:
            result = 'wget error!'
        else :
            cmd = 'cd %s ; md5sum %s |cut -d \' \' -f1'%(path,filename)
            (status, output) = commands.getstatusoutput(cmd)
            self.log.debug('[status]:%s  [output]:%s'%(status,output), extra={'namespace' : 'xmpp'})

            if output == md5:
                process = getattr(self,ok_hdl)
                process(path, filename)
                result = 'OK' 
            else :
                process = getattr(self,err_hdl)
                process(path, filename)
                result = 'md5 check error'
        return result 

    def ok_hdl_1(self, file_path, file_name):
        self.log.info('process ok condition...', extra={'namespace' : 'xmpp'})
        path = '/usr/local/src/RestXMPP/bin/'
        cmd = 'cd %s ; sh download_ok_hdlr %s %s '%(path, file_path, file_name) 
        self.log.debug('cmd:%s  '%cmd, extra={'namespace' : 'xmpp'})
        ret = subprocess.call(cmd,shell = True)
        self.log.info('ret:%s...'%ret, extra={'namespace' : 'xmpp'})
        return ret 

    def err_hdl_1(self, file_path, file_name):
        self.log.info('process error condition...', extra={'namespace' : 'xmpp'})
        path = '/usr/local/src/RestXMPP/bin/'
        cmd = 'cd %s ; sh download_err_hdlr %s %s '%(path, file_path, file_name) 
        self.log.debug('cmd:%s  '%cmd, extra={'namespace' : 'xmpp'})
        ret = subprocess.call(cmd,shell = True)
        self.log.info('ret:%s...'%ret, extra={'namespace' : 'xmpp'})
        return ret 

