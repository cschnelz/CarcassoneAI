from re import A
from turtle import tiltangle
import unittest
from Game import Game
from Tile import rotate
from Action import *
from Import import importTiles

## for old tests
from Board import *
from Feature import *

def reset(forced=None):
    game = Game(order=list(range(0,72))) if forced is None else Game(order=forced)
    tileList = importTiles('TileSetSepRoads.json')
    return game, tileList


## Tests for each front-facing func of the api
class testGetState(unittest.TestCase):
    pass

class testGetActions(unittest.TestCase):
    pass

class testApplyAction(unittest.TestCase):
    pass

class testGameOver(unittest.TestCase):
    pass

class testHelpers(unittest.TestCase):
    def testSymmetricTileActions(self):
        game, tileList = reset(forced=[13,62,7,10,29,30])

        self.assertEqual(len(game.state.currentActions),6)
    
    def testNoMeepleActions(self):
        game, tileList = reset(forced=[13,62,8,10,29,30])
        game.state.players[0].meepleCount = 0
        game.state.players[1].meepleCount = 0
        game.applyAction(Action(0,-1,game.state.currentTile[0],False,None))

        self.assertEqual(len(game.state.currentActions),5)

    def testSymmetricTileActions2(self):
        game,tileList = reset(forced=[13,62,27,10,29,30])

        game.applyAction(Action(0,-1,game.state.currentTile[0],False,None))

        self.assertEqual(len(game.state.currentActions),24)
        

class testEquality(unittest.TestCase):
    def testEquality(self):
        game, tileList = reset()
        tile = tileList[16][0]

        a1 = Action(1,0,tile,True,tile.features[0])

        tile2 = tileList[16][0]
        a2 = Action(1,0,tile2,True,tile2.features[0])

        tile3 = tileList[16][1]
        a3 = Action(1,0,tile3,True,tile3.features[0])

        self.assertEqual(a1,a2)
        self.assertNotEqual(a2,a3)

class testEvaluate(unittest.TestCase):
    def testEvaluate1(self):
        game,tileList = reset()
        tile = tileList[19][1]
        game.applyAction(Action(1,0,tile,True,tile.features[0]))
        
        tile = tileList[17][0]
        game.applyAction(Action(1,-1,tile,True,tile.features[0]))
        game.applyAction(Action(2,-1,tileList[56][1],False,None))
        tile = tileList[0][3]
        game.applyAction(Action(0,-1,tile,True,tile.features[1]))
        tile = tileList[1][3]
        game.applyAction(Action(-1,-1,tile,True,tile.features[0]))
        game.applyAction(Action(-1,-2,tileList[11][2],False,None))
        game.applyAction(Action(3,-1,tileList[10][3],False,None))
            
        self.assertEqual(game.evaluate(),(8,8))

class testFinalScore(unittest.TestCase):
    def testFieldScoring(self):
        game,tileList = reset()
        tile = tileList[15][2]
        game.applyAction(Action(0,-1,tile,True,tile.grasses[0]))
        game.applyAction(Action(1,-1,tileList[3][3], False, None))
        tile = tileList[21][0]
        game.applyAction(Action(-1, 0, tile,True,tile.grasses[0]))
        game.applyAction(Action(-2, 0, tileList[27][0],False,None))

        score0_1 = game.state.scoreGrass(game.state.board.board.get((0,-1)),game.state.board.meepled.get((0,-1)))
        self.assertEqual(score0_1,3)
        score_10 = game.state.scoreGrass(game.state.board.board.get((-1,0)),game.state.board.meepled.get((-1,0)))
        self.assertEqual(score_10,3)

       
    def testChapelScoring(self):
        game,tileList = reset()

        tile = tileList[19][1]
        game.applyAction(Action(1,0,tile,True,tile.features[0]))
        game.applyAction(Action(1,-1,tileList[17][0],False,None))
        game.applyAction(Action(0,1,tileList[19][2],False,None))

        self.assertEqual(game.state.finalScore(), (4,0))
    

    def testFinalScore(self):
        game,tileList = reset()
        tile = tileList[19][1]
        game.applyAction(Action(1,0,tile,True,tile.features[0]))
        tile = tileList[17][0]
        game.applyAction(Action(1,-1,tile,True,tile.features[0]))
        game.applyAction(Action(2,-1,tileList[56][1],False,None))
        tile = tileList[0][3]
        game.applyAction(Action(0,-1,tile,True,tile.features[1]))
        tile = tileList[1][3]
        game.applyAction(Action(-1,-1,tile,True,tile.features[0]))
        game.applyAction(Action(-1,-2,tileList[11][2],False,None))
       
        

        self.assertEqual(game.state.finalScore(),(8,4))


## Refactors of the old tests into the new format
class testFinishedFeatures(unittest.TestCase):
    def testSmallCities(self):
        game,tileList = reset()
        game.applyAction(Action(-1,0,tileList[21][0],False,None))
        game.applyAction(Action(-2,0,tileList[3][1],False,None))
        game.applyAction(Action(0,-1,tileList[61][1],False,None))

        self.assertTrue(game.board().findTracked(game.board().nodeAt(-2,0),1,game.board().trackedFeatures).completed)
        self.assertTrue(game.board().findTracked(game.board().nodeAt(-1,0),1,game.board().trackedFeatures).completed)
        self.assertFalse(game.board().findTracked(game.board().nodeAt(0,-1),0,game.board().trackedFeatures).completed)

    def testMultiCity(self):
        game, tileList = reset()
        game.applyAction(Action(0,-1,tileList[15][2],False,None))
        game.applyAction(Action(1,-1,tileList[3][3], False, None))
        game.applyAction(Action(-1, 0,tileList[21][0],False,None))
        game.applyAction(Action(-2, 0,tileList[27][0],False,None))

        self.assertTrue(game.board().findTracked(game.board().nodeAt(0,0),0,game.board().trackedFeatures).completed)
        self.assertFalse(game.board().findTracked(game.board().nodeAt(-1, 0), 3, game.board().trackedFeatures).completed)

    def testUnfinishedCornerCity(self):
        game, tileList = reset()
        self.assertFalse(game.board().findTracked(game.board().nodeAt(0,0),0,game.board().trackedFeatures).completed)

    def testLoopedCity(self):
        game, tileList = reset()
        game.applyAction(Action(0, -1,tileList[30][3],False,None))
        game.applyAction(Action(-1, -1,tileList[27][0],False,None))
        game.applyAction(Action(-1, 0,tileList[56][1],False,None))
        game.applyAction(Action(-2, -1,tileList[15][2],False,None))
        game.applyAction(Action(-2, 0,tileList[50][1],False,None))
        
        self.assertTrue(game.board().findTracked(game.board().nodeAt(0, 0), 0, game.board().trackedFeatures).completed)

    def testBranchingUnfinished(self):
        game, tileList = reset()
        game.applyAction(Action(0, -1,tileList[30][3],False,None))
        game.applyAction(Action(-1, -1,tileList[27][0],False,None))
        game.applyAction(Action(-1, 0,tileList[56][1],False,None))
        
        self.assertFalse(game.board().findTracked(game.board().nodeAt(0, 0), 0, game.board().trackedFeatures).completed)

    def testRoads(self):
        game, tileList = reset()
        game.applyAction(Action(1, 0,tileList[34][1],False,None))
        game.applyAction(Action(2, 0,tileList[43][1],False,None))
        game.applyAction(Action(0, 1,tileList[16][2],False,None))
        
        self.assertTrue(game.board().findTracked(game.board().nodeAt(0,0),1,game.board().trackedFeatures).completed)
        self.assertFalse(game.board().findTracked(game.board().nodeAt(0,1),1,game.board().trackedFeatures).completed)

    def testLoopRoad(self):
        game,tileList = reset()
        game.applyAction(Action(1, 0,tileList[16][0],False,None))
        game.applyAction(Action(0,1,tileList[14][2],False,None))
        game.applyAction(Action(1,1,tileList[24][1],False,None))

        self.assertTrue(game.board().findTracked(game.board().nodeAt(0,0),1,game.board().trackedFeatures).completed)


class testOccupiedFeature(unittest.TestCase):
    
    def testCityMeepled(self):
        game,tileList = reset()
        tile = tileList[61][1]
        game.applyAction(Action(0,-1,tile,True,tile.features[0]))

        self.assertTrue(game.state.board.featureMeepled(0,0,0,FeatType.CITY))
        self.assertFalse(game.state.board.featureMeepled(0,-1,0,FeatType.CITY))

    def testRoadMeepled(self):
        game,tileList = reset()
        tile = tileList[16][0]
        game.applyAction(Action(1,0,tile,True,tile.features[2]))
        tile = tileList[28][0]
        game.applyAction(Action(2,0,tile,True,tile.features[0]))
        
    
        self.assertTrue(game.state.board.featureMeepled(0,0,1,FeatType.ROAD))
        self.assertTrue(game.state.board.featureMeepled(1,0,1,FeatType.ROAD))
        self.assertFalse(game.state.board.featureMeepled(1,0,2,FeatType.ROAD))




class testScoring(unittest.TestCase):
    
    def testFinishAndScore(self):
        game,tileList = reset([0,61,3,10])
        self.assertEqual(game.getScore(),(0,0))

        tile = game.state.currentTile[1]
        game.applyAction(Action(0,-1,tile,True,tile.features[0]))
    
        self.assertTrue(game.state.board.featureMeepled(0,0,0,FeatType.CITY))
        game.applyAction(Action(-1,0,game.state.currentTile[1],False,None))
        
        self.assertEqual(game.getScore(),(8,0))
       


class testFields(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
