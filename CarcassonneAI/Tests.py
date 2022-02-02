from Tile import Tile
from Feature import *

import unittest

tileList = [ 
    Tile(0, [Road([1,3], False)]), 
    Tile(1, [City([0], True)]),
    Tile(2, [Road([1, 2], True)]),
    Tile(3, [City([1], False)])
]

class testTileConnections(unittest.TestCase):
    ## Test north to non-south connection
    def testBasic(self):
        self.assertFalse(tileList[1].canConnectTo(tileList[3], 0))
    
    ## tests west to east road connection
    def testBasic2(self):
        self.assertTrue(tileList[0].canConnectTo(tileList[2], 3))


if __name__ == '__main__':
    unittest.main()