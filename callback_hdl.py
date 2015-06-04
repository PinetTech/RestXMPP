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



def callback_handle(args):
    log = logging.getLogger("cement:app:xmpp")
    t = args.get('type', 'not found')
    m = args.get('module', 'not found')
    f = args.get('function', 'not found')
    arg = args.get('args', 'not found')

    log.debug("Callback para type:%s, module:%s, function:%s, arg:%s" %(t, m, f, arg), extra={'namespace' : 'xmpp'})
    
    try:
        module = __import__("callbacks." + m)
    except ImportError:
        log.error("No callback named %s found!" %m, extra={'namespace' : 'xmpp'})
        result = 'No callback named %s found!' %m
        return result 
    try:
        module = getattr(module, m)
    except AttributeError:
        log.error("get attr: %s error!" %m, extra={'namespace' : 'xmpp'})
        result = 'get attr: %s error!' %m
        return result 
    except :
        log.error("unknow error! module:%s" %m, extra={'namespace' : 'xmpp'})
        result = ' unknow error module1'
        return result 
    try:
        callback_class = getattr(module, m.capitalize())
        c = callback_class()
        try:
            function = getattr(c, str(f))
            result = function(arg)
            
        except AttributeError:
            log.error("No functon named %s found!" %f, extra={'namespace' : 'xmpp'})
            result = 'No functon named %s found!' %f
        except :
            result = ' unknow error module3'
            
    except AttributeError:
        log.error("get attr: %s error!" %m, extra={'namespace' : 'xmpp'})
        result = 'get attr: %s error!' %m
    except :
        log.error("unknow error! module:%s" %m, extra={'namespace' : 'xmpp'})
        result = ' unknow error module2'
    return result



