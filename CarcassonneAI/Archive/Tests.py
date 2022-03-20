from tabnanny import check
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from Tile import rotate
from Feature import *
from Board import Board
from Manager import *
from Import import importTiles
from typing import List


import unittest

tileFile = 'TileSetSepRoads.json'
tileList: List[Tile] = importTiles(tileFile)

testPlayers = [Player(0, HumanAgent()), Player(1, HumanAgent())]

class testTileConnections(unittest.TestCase):
    ## Test north to non-south connection
    def testBasic(self):
        self.assertFalse(tileList[1].canConnectTo(tileList[3], 1))
    
    ## tests west to east road connection
    def testBasic2(self):
        self.assertTrue(tileList[34].canConnectTo(tileList[36], 2))

# one large completed city and one smaller uncompleted
def createBoard1():
    importTiles(tileFile)
    board = Board(tileList[0])

    board.addTile(0,-1,rotate(tileList[15], 2))
    board.addTile(1,-1,rotate(tileList[3], 3))
    board.addTile(-1, 0, rotate(tileList[21], 0))
    board.addTile(-2, 0, rotate(tileList[27], 0))
    return board

# single tile with a corner city
def createBoard2():
    importTiles(tileFile)
    board = Board(tileList[0])
    return board

# big looping city
def createBoard3():
    importTiles(tileFile)
    board = Board(rotate(tileList[0], 1))
    board.addTile(0, -1, rotate(tileList[30], 2))
    board.addTile(1, -1, rotate(tileList[27], 0))
    board.addTile(1, 0, rotate(tileList[56], 1))
    board.addTile(2, -1, rotate(tileList[15], 3))
    board.addTile(2, 0, tileList[50])
    return board

# city that branches in two directions and both are unfinished
def createBoard4():
    importTiles(tileFile)
    board = Board(rotate(tileList[0], 1))
    board.addTile(0, -1, rotate(tileList[30], 2))
    board.addTile(1, -1, rotate(tileList[27], 0))
    board.addTile(1, 0, rotate(tileList[56], 1))
    return board

# one terminated road crossing 0,0 and one non terminated road crossing -1 1
def createBoard5():
    importTiles(tileFile)
    board = Board(rotate(tileList[25], 0))
    board.addTile(0, -1, rotate(tileList[34], 2))
    board.addTile(0, -2, rotate(tileList[43], 0))
    board.addTile(0, 1, rotate(tileList[16], 2))
    board.addTile(-1, 1, rotate(tileList[46], 3))
    return board

def createBoard6():
    importTiles(tileFile)
    board = Board(rotate(tileList[1], 0))
    board.addTile(1, 0, rotate(tileList[3], 3))
    return board

class testFinishedFeatures(unittest.TestCase):
        
    def testMultipleCompleteCity(self):
        board = createBoard1()
        self.assertTrue(buildFeature(0, 0, 0, board, FeatType.CITY).completed)

    def testMultipleIncompleteCity(self):
        board = createBoard1()
        self.assertFalse(buildFeature(-1, 0, 3, board, FeatType.CITY).completed)

    def testSingleTileTwoEdges(self):
        board = createBoard2()
        self.assertFalse(buildFeature(0, 0, 0, board, FeatType.CITY).completed)

    def testLoopingCity1(self):
        board = createBoard3()
        self.assertTrue(buildFeature(0, 0, 0, board, FeatType.CITY).completed)

    def testBranchingUnfinished(self):
        board = createBoard4()
        self.assertFalse(buildFeature(0, 0, 0, board, FeatType.CITY).completed)

    def testFinishedRoad(self):
        board = createBoard5()
        self.assertTrue(buildFeature(0, 0, 0, board, FeatType.ROAD).completed)
    
    def testUnfinishedRoad(self):
        board = createBoard5()
        self.assertFalse(buildFeature(0, 1, 3, board, FeatType.ROAD).completed)

    def testSizeTwoCity(self):
        board = createBoard6()
        self.assertTrue(buildFeature(0,0, 1, board, FeatType.CITY).completed)

class testFeatureImports(unittest.TestCase):

    def testChapel1(self):
        importTiles(tileFile)
        tile = tileList[35]
        self.assertTrue(tile.chapel)
        tile2 = Tile(7777, [Road([1], False)], [],'zz', 0)
        self.assertFalse(tile2.chapel)


class testMeepleOccupied(unittest.TestCase):

    def testCity(self):
        importTiles(tileFile)
        board = Board(tileList[15])
        tile = rotate(tileList[50], 1)
        tile.occupied = tile.features[0]
        tile.features[0].occupiedBy = Player(0, HumanAgent())
        board.addTile(-1, 0, tile)
        board.addTile(-1, -1, tileList[1])
        self.assertTrue(buildFeature(-1,-1,2,board,FeatType.CITY).meepled)
        self.assertFalse(buildFeature(-1,-1,1,board,FeatType.CITY).meepled)

    def testRoads(self):
        importTiles(tileFile)
        tile = tileList[70]
        board = Board(tile)

        board.addTile(0, 1, tileList[40])
        self.assertFalse(buildFeature(0,1,0, board,FeatType.ROAD).meepled)

        tile = tileList[46]
        tile.occuped = tile.features[0]
        tile.features[0].occupiedBy = Player(1, HumanAgent())
        board.addTile(0, 2, tile)
        self.assertTrue(buildFeature(0,2,2,board,FeatType.ROAD).meepled)

def resetScore():
    testPlayers[0].score = testPlayers[1].score = 0

def calculateScoreQuiet(completed: List[combinedFeature]):
    for c in completed:
        for feat in c.meepled:
            feat.occupiedBy = None
        if len(c.playersOn) > 0:
            redCount = c.playersOn.count('red')
            blueCount = c.playersOn.count('blue')

            if redCount == blueCount:
                testPlayers[0].score += c.score
                testPlayers[1].score += c.score
            elif redCount > blueCount:
                testPlayers[0].score += c.score
            else:
                testPlayers[1].score += c.score
            testPlayers[0].meepleCount += redCount
            testPlayers[1].meepleCount += blueCount

class testScoring(unittest.TestCase):

    def testCity(self):
        importTiles(tileFile)
        resetScore()
        self.assertTrue(players[0].score == players[1].score)

        board = Board(tileList[56])
        
        tile = tileList[3]
        tile.occupied = tile.features[0]
        tile.features[0].occupiedBy = testPlayers[1]
        board.addTile(0,1,tile)

        tile = tileList[31]
        board.addTile(0, -1, tile)

        completed = checkCompletedFeatures(0, -1, board)
        calculateScoreQuiet(completed)

        self.assertTrue(testPlayers[0].score == 0 and testPlayers[1].score == 6)
    
    def testRoad(self):
        importTiles(tileFile)
        resetScore()
        self.assertTrue(testPlayers[0].score == testPlayers[1].score)

        board = Board(tileList[70])
        tile = tileList[40]
        tile.occupied = tile.features[0]
        tile.features[0].occupiedBy = testPlayers[0]
        board.addTile(0,1,tile)
        board.addTile(0,2,rotate(tileList[16], 2))

        completed = checkCompletedFeatures(0, 2, board)
        calculateScoreQuiet(completed)

        self.assertTrue(testPlayers[0].score == 3 and testPlayers[1].score == 0)

    def testLoopCity(self):
        importTiles(tileFile)
        resetScore()
        self.assertTrue(testPlayers[0].score == testPlayers[1].score and testPlayers[0].score == 0)

        board = Board(rotate(tileList[63], 2))
        tile = rotate(tileList[50],1)
        tile.occupied = tile.features[0]
        tile.occupied.occupiedBy = testPlayers[1]
        board.addTile(0,1,tile)

        board.addTile(1, 0, rotate(tileList[30], 3))
        board.addTile(1, 1, tileList[29])

        completed = checkCompletedFeatures(1, 1, board)
        self.assertTrue(len(completed) == 1)
        
        calculateScoreQuiet(completed)

        self.assertTrue(testPlayers[0].score == 0 and testPlayers[1].score == 10)

    def testSharedPoints(self):
        importTiles(tileFile)
        resetScore()
        self.assertTrue(testPlayers[0].score == testPlayers[1].score and testPlayers[0].score == 0)

        board = Board(rotate(tileList[63], 2))
        tile = rotate(tileList[50],1)
        tile.occupied = tile.features[0]
        tile.occupied.occupiedBy = testPlayers[1]
        board.addTile(0,1,tile)

        tile = rotate(tileList[30], 3)
        tile.occupied = tile.features[0]
        tile.occupied.occupiedBy = testPlayers[0]
        board.addTile(1, 0, tile)
        board.addTile(1, 1, tileList[29])

        completed = checkCompletedFeatures(1, 1, board)
        self.assertTrue(len(completed) == 1)

        calculateScoreQuiet(completed)

        self.assertTrue(testPlayers[0].score == 10 and testPlayers[1].score == 10)

    def testMajorityTakesAll(self):
        importTiles(tileFile)
        resetScore()
        self.assertTrue(testPlayers[0].score == testPlayers[1].score and testPlayers[0].score == 0)

        board = Board(rotate(tileList[63], 2))
        tile = rotate(tileList[50],1)
        tile.occupied = tile.features[0]
        tile.occupied.occupiedBy = testPlayers[1]
        board.addTile(0,1,tile)

        tile = rotate(tileList[30], 3)
        tile.occupied = tile.features[0]
        tile.occupied.occupiedBy = testPlayers[0]
        board.addTile(1, 0, tile)

        tile = tileList[29]
        tile.occupied = tile.features[0]
        tile.occupied.occupiedBy = testPlayers[0]
        board.addTile(1, 1, tile)

        completed = checkCompletedFeatures(1, 1, board)
        self.assertTrue(len(completed) == 1)

        calculateScoreQuiet(completed)

        self.assertTrue(testPlayers[0].score == 10 and testPlayers[1].score == 0)

    def testChapelScoring(self):
        boardC = Board(rotate(tileList[4],1))
        chapelTile = tileList[35]
        chapelTile.occupied = chapelTile.features[0]
        chapelTile.occupied.occupiedBy = testPlayers[1]
        testPlayers[1].meepleCount -= 1

        boardC.addTile(0,-1,chapelTile)
        boardC.addTile(0,-2,rotate(tileList[9],1))
        boardC.addTile(1,-1,tileList[25])
        boardC.addTile(-1,-1,tileList[34])
        boardC.addTile(1,-2,tileList[14])
        boardC.addTile(1,0, rotate(tileList[24],1))
        boardC.addTile(-1,0, rotate(tileList[28],2))
        boardC.addTile(-1,-2, rotate(tileList[41],3))

        self.assertTrue(testPlayers[1].meepleCount == 6)
        completed = checkCompletedFeatures(-1, -2, boardC)
        self.assertTrue(len(completed) == 2)
        calculateScoreQuiet(completed)
        self.assertTrue(testPlayers[0].score == 0 and testPlayers[1].score == 9)
        self.assertTrue(testPlayers[0].meepleCount == 7 and testPlayers[1].meepleCount == 7)



class testRotation(unittest.TestCase):
    def testRotateCity(self):
        importTiles(tileFile)
        tile = tileList[29]

        tile2 = rotate(tile, 1)
        self.assertTrue(tile2.edges[0] == FeatType.CITY and tile2.edges[1] == FeatType.CITY)
        self.assertTrue(set(tile2.features[0].edges) == set([0,1]))

    def testRotateRoad(self):
        importTiles(tileFile)
        tile = tileList[29]

        tile2 = rotate(tile, 2)
        self.assertTrue(tile2.edges[0] == FeatType.ROAD and tile2.edges[3] == FeatType.ROAD)
        self.assertTrue(set(tile2.features[1].edges) == set([0,3]))

    def testRotateGrass(self):
        importTiles(tileFile)
        tile = tileList[29]

        self.assertTrue(tile.edges[0] == FeatType.CITY and tile.edges[3] == FeatType.CITY)        
        self.assertTrue(tile.edges[1] == FeatType.ROAD and tile.edges[2] == FeatType.ROAD)
        self.assertTrue(tile.grasses[0].edges == [2,5])

        tile2 = rotate(tile, 1)

        self.assertTrue(tile2.edges[1] == FeatType.CITY)
        self.assertTrue(set(tile2.grasses[0].edges) == set([4,7]))


class testFields(unittest.TestCase):
    def fieldBoard(self):
        importTiles(tileFile)
        tile = tileList[70]
        board = Board(tile)

        board.addTile(0, 1, tileList[40])
        
        tile = tileList[46]
        tile.occupied = tile.grasses[0]
        tile.occupied.occupiedBy = testPlayers[1]
        board.addTile(0, 2, tile)
        return board

    def testFieldBuilding(self):
        board = self.fieldBoard()
        completed = buildFeature(0,0,5,board, FeatType.GRASS)
        leftFields = set([(71,5), (41,0),(41,7),(41,6),(41,5),(47,7),(47,6),(47,5),(47,0)])
        self.assertEqual(set(completed.features), leftFields)

        rightFields = set([(71,4), (41,1),(41,2),(41,3),(41,4),(47,1),(47,2),(47,3),(47,4)])
        completed = buildFeature(0,0,4,board, FeatType.GRASS)
        self.assertEqual(set(completed.features), rightFields)

        board.addTile(0,3,rotate(tileList[19], 2))
        totalFields = leftFields.union(rightFields).union(set([(20,0),(20,1),(20,2),(20,3),(20,4),(20,5),(20,6),(20,7)]))
        completed2 = buildFeature(0,0, 5, board, FeatType.GRASS)
        self.assertEqual(set(completed2.features), totalFields)

    def testCityAdjacency(self):
        t3 = rotate(tileList[0], 1)
        board = Board(t3)
        c3 = t3.features[0]

        t2 = rotate(tileList[30],2)
        board.addTile(0, -1, t2)
        c2 = t2.features[0]

        t1 = rotate(tileList[27], 0)
        board.addTile(1, -1, t1)
        c1 = t1.features[0]

        t4 = rotate(tileList[56], 1)
        board.addTile(1, 0, t4)
        c4 = t4.features[0]
        
        board.addTile(1,-2, rotate(tileList[25], 1))
        board.addTile(0,-2, rotate(tileList[14], 3))
        board.addTile(-1,-1, rotate(tileList[24], 3))
        board.addTile(-1,0, rotate(tileList[28], 2))

        completed = buildFeature(0,0,7,board, FeatType.GRASS)
        self.assertEqual(adjacentCities(completed), {c1,c2,c3})
        

        completed2 = buildFeature(0,0,6,board, FeatType.GRASS)
        self.assertFalse(adjacentCities(completed2))

        completed3 = buildFeature(1,-1,5,board, FeatType.GRASS)
        self.assertEqual(adjacentCities(completed3), {c4,c1})

class testBoardFuncs(unittest.TestCase):

    def testNeighbor8(self):
        board = createBoard3()
        self.assertEqual({31,28,57}, set([node.tile.id for node in board.neighbors8(0,0)]))

if __name__ == '__main__':
    unittest.main()