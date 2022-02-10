import sys

from Manager import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        forcedOrder = sys.argv[1:len(sys.argv)]
        initialize(forcedOrder)
    initialize([])