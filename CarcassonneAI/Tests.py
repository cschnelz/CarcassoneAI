from Tile import rotate
from Feature import *
from Board import Board
from Manager import *
from Import import importTiles

import unittest

tileList = importTiles('TileSetSepRoads.json')

class testTileConnections(unittest.TestCase):
    ## Test north to non-south connection
    def testBasic(self):
        self.assertFalse(tileList[1].canConnectTo(tileList[3], 1))
    
    ## tests west to east road connection
    def testBasic2(self):
        self.assertTrue(tileList[34].canConnectTo(tileList[36], 2))

# one large completed city and one smaller uncompleted
def createBoard1():
    importTiles('TileSetSepRoads.json')
    board = Board(tileList[0])

    board.addTile(0,-1,rotate(tileList[15], 2))
    board.addTile(1,-1,rotate(tileList[3], 3))
    board.addTile(-1, 0, rotate(tileList[21], 0))
    board.addTile(-2, 0, rotate(tileList[27], 0))
    return board

# single tile with a corner city
def createBoard2():
    importTiles('TileSetSepRoads.json')
    board = Board(tileList[0])
    return board

# big looping city
def createBoard3():
    importTiles('TileSetSepRoads.json')
    board = Board(rotate(tileList[0], 1))
    board.addTile(0, -1, rotate(tileList[30], 2))
    board.addTile(1, -1, rotate(tileList[27], 0))
    board.addTile(1, 0, rotate(tileList[56], 1))
    board.addTile(2, -1, rotate(tileList[15], 3))
    board.addTile(2, 0, tileList[50])
    return board

# city that branches in two directions and both are unfinished
def createBoard4():
    importTiles('TileSetSepRoads.json')
    board = Board(rotate(tileList[0], 1))
    board.addTile(0, -1, rotate(tileList[30], 2))
    board.addTile(1, -1, rotate(tileList[27], 0))
    board.addTile(1, 0, rotate(tileList[56], 1))
    return board

# one terminated road crossing 0,0 and one non terminated road crossing -1 1
def createBoard5():
    importTiles('TileSetSepRoads.json')
    board = Board(rotate(tileList[25], 0))
    board.addTile(0, -1, rotate(tileList[34], 2))
    board.addTile(0, -2, rotate(tileList[43], 0))
    board.addTile(0, 1, rotate(tileList[16], 2))
    board.addTile(-1, 1, rotate(tileList[46], 3))
    return board

class testFinishedFeatures(unittest.TestCase):
        
    def testMultipleCompleteCity(self):
        board = createBoard1()
        self.assertTrue(finishedFeature(0, 0, board.tileAt(0,0), 0, board))

    def testMultipleIncompleteCity(self):
        board = createBoard1()
        self.assertFalse(finishedFeature(-1, 0, board.tileAt(-1,0), 3, board))

    def testSingleTileTwoEdges(self):
        board = createBoard2()
        self.assertFalse(finishedFeature(0, 0, board.tileAt(0,0), 0, board))

    def testLoopingCity1(self):
        board = createBoard3()
        self.assertTrue(finishedFeature(0, 0, board.tileAt(0,0), 0, board))

    def testBranchingUnfinished(self):
        board = createBoard4()
        self.assertFalse(finishedFeature(0, 0, board.tileAt(0,0), 0, board))

    def testFinishedRoad(self):
        board = createBoard5()
        self.assertTrue(finishedFeature(0, 0, board.tileAt(0,0), 0, board))
    
    def testUnfinishedRoad(self):
        board = createBoard5()
        self.assertFalse(finishedFeature(0, 1, board.tileAt(0,1), 3, board))

class testFeatureImports(unittest.TestCase):

    def testChapel1(self):
        importTiles('TileSetSepRoads.json')
        tile = tileList[35]
        self.assertTrue(tile.chapel)
        tile2 = Tile(7777, [Road([1], False)], 'zz', 0)
        self.assertFalse(tile2.chapel)

    def testGrass(self):
        tile1 = Tile(888, [City([0], False), Road([1,2], False)], 'zz', 0)
        feats = tile1.features
        grasses = tile1.grass
        self.assertTrue(tile1.edges[3] is None)
        self.assertTrue(grasses[0].edges == [2])


if __name__ == '__main__':
    unittest.main()