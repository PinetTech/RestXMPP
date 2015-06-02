#===============================================================================
#
# The XMPP callback_hdl
# 
# @version 1.0
# @author Kallun <kallun.zhu@pinet.co>
# @date Tue June  2 09:13:03 2015
#
#===============================================================================

# Imports
import sys
import importlib
import logging

log = logging.getLogger("cement:app:xmpp")


def callback_handle(args):
    t = args.get('type', 'not found')
    m = args.get('module', 'not found')
    f = args.get('function', 'not found')
    arg = args.get('args', 'not found')

    log.debug("Callback para type:%s, module:%s, function:%s, arg:%s" %(t, m, f, arg), extra={'namespace' : 'xmpp'})
    
    try:
        module = __import__("callbacks." + m)
        module = getattr(module, m)
        callback_class = getattr(module, m.capitalize())
        c = callback_class()
        try:
            function = getattr(c, str(f))
            function(arg)
            
        except AttributeError:
            log.error("No functon named %s found!" %f, extra={'namespace' : 'xmpp'})
            
    except ImportError:
        log.error("No callback named %s found!" %m, extra={'namespace' : 'xmpp'})



