import sys

from Manager import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        forcedOrder = [int(x) for x in sys.argv[1:len(sys.argv)]]
        initialize(forcedOrder)
    initialize([])