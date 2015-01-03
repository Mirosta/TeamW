import sys
import os
import logging
# Set debug logging
logging.getLogger().setLevel(logging.DEBUG)
#Add lib to path
newPath = os.path.join(os.path.dirname(__file__), '..', 'lib')
logging.info('Adding to pypath ' + newPath)
sys.path.append(newPath)
