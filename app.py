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

# Construct the APP
app = ServiceLocator.Instance().app();

# Start the APP
try:
    app.setup()
    app.run()
finally:
    # Clean Up
    app.close()
