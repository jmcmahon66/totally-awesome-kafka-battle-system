import time
import logging
from helper import myfunction
# import sys

logging.basicConfig(level=logging.DEBUG) #, stream=sys.stdout)
logger = logging.getLogger(__name__)

i = 0

if __name__ == '__main__':
    while i < 5:
        i += 1
        print(i)
        string = myfunction()
        logger.debug(f"{string} {i}")
        time.sleep(5)