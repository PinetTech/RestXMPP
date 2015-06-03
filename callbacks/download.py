from callback import Callback
import commands
import logging

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

        cmd = 'cd %s ; wget %s%s'%(path,url,filename)
        self.log.info('cmd%s  '%cmd, extra={'namespace' : 'xmpp'})
        (status, output) = commands.getstatusoutput(cmd)
        self.log.info('status:%s  \n< output:%s>\n'%(status,output), extra={'namespace' : 'xmpp'})
        if status != 0:
            result = 'wget error!'
        else :
            cmd = 'cd %s ; md5sum %s |cut -d \' \' -f1'%(path,filename)
            (status, output) = commands.getstatusoutput(cmd)
            self.log.info('status:%s  \n< output:%s>\n'%(status,output), extra={'namespace' : 'xmpp'})

            if output == md5:
                process = getattr(self,ok_hdl)
                process()
                result = 'OK' 
            else :
                process = getattr(self,err_hdl)
                process()
                result = 'md5 check error'
        return result 

    def err_hdl_1(self, args = None):
        self.log.info('process errors...', extra={'namespace' : 'xmpp'})

    def ok_hdl_1(self, args = None):
        self.log.info('process success...', extra={'namespace' : 'xmpp'})

