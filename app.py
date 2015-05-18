#! env python

#===============================================================================
#
# The XMPP Server Controller Instance
# 
# @version 1.0
# @author Jack <guitarpoet@gmail.com>
# @date Sun May  3 18:47:07 2015
#
#===============================================================================

# Imports
from services import ServiceLocator
import logging
import cement.ext.ext_logging

sleekxmpp_logger = logging.getLogger('sleekxmpp')
sleekxmpp_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
debug_format = "%(asctime)s (%(levelname)s) sleek : %(message)s"
console_handler.setFormatter(logging.Formatter(debug_format))
sleekxmpp_logger.addHandler(console_handler)

# Construct the APP
app = ServiceLocator.Instance().app();

# Start the APP
try:
    app.setup()
    app.run()
finally:
    # Clean Up
    app.close()
