## Holds all information about the current game state

from typing import List

from Board import Board, combinedFeature, Node, meepleInfo, builtFeature
from Feature import *
from Tile import Tile
from Player import Player
from Import import importTiles
from Action import Action, validActions
from random import random, choice
import copy

class State:
    def __init__(self, players: List[Player], order):
        self.players = players
        self.currentPlayer = 0
        self.order = order
        self.tileHist = []
        
        self.turn = 2
        self.tileList = importTiles('TileSetSepRoads.json')
        
        self.currentTile = self.tileList.pop(int(random()*len(self.tileList))) if len(self.order) == 0 else self.tileList[self.order.pop(0)]
        self.board = Board(self.currentTile)
        self.currentTile = self.dispatchTile() if len(self.order) == 0 else self.dispatchTile(self.order.pop(0))

        self.hash = "" 
        ## a unique hash string, representing actions in order
        ## 'id xCoord yCoord Meepled Feat/Grass Edge'

    # Get a new tile for current tile
    def dispatchTile(self, index=None) -> Tile:
        if index is None:
            dispatchId = int(random() * len(self.tileList))
            tile = self.tileList[dispatchId]
            del self.tileList[dispatchId]
        else:
            dispatchId = index
            tile = self.tileList[dispatchId]

        if len(validActions(self.board,tile,False)) == 0:
            return self.dispatchTile()
        else:
            self.tileHist.append(tile.id)
            return tile

    def getActions(self) -> List[Action]:
        return validActions(self.board, self.currentTile, self.players[self.currentPlayer].meepleCount > 0)
    
    def gameOver(self) -> bool:
        # check for end of game
        return self.turn >= 72

    def scoreDelta(self):
        score = (self.players[0].score,self.players[1].score)
        fscore = self.finalScore()
        return (score[0] + fscore[0]) - (score[1] + fscore[1])

    def applyAction(self, action: Action, quiet=False):
        # update the state based on the action

        if action.meeple:     
            meeple = meepleInfo(self.players[self.currentPlayer],action.feature)
            self.board.meepled[(action.x, action.y)] = meeple
        
            self.players[self.currentPlayer].meepleCount -= 1

        self.playTile(action,quiet)
        self.currentPlayer = (self.currentPlayer + 1) % 2
        self.turn += 1
        self.currentTile = self.dispatchTile() if len(self.order) == 0 else self.dispatchTile(self.order.pop(0))

    def playTile(self, action: Action, quiet=False):
        ## Add the tile to the board
        node = self.board.addTile(action.x, action.y, action.tile)
        ## Update connected features
        self.board.connectFeatures(node, action.feature, self.players[self.currentPlayer].color)

        ## Calculate and update scores
        completed = self.checkCompletedFeatures(action.x, action.y)
        self.calculateScore(completed, quiet)

    ## Called in PlayTile
    def checkCompletedFeatures(self, x, y) -> List[builtFeature]:
        completed = []
        node = self.board.nodeAt(x,y)

        toCheck: set[builtFeature] = set()
        ## add into a set to avoid checking the same feature twice
        for i in range(4):
            bF = self.board.findTracked(node,i,self.board.trackedFeatures)
            if bF is not None:
                toCheck.add(bF)
        for bF in toCheck:
            if bF.completed:
                completed.append(bF)
                for coord in set(bF.coordsMeepled):
                    try:
                        self.board.meepled.pop(coord)
                    except:
                        print(self.tileHist)

        # for i in range(4):
        #     tile = self.board.tileAt(x,y)
        #     combined = self.board.buildFeature(x,y,i,tile.featureAtEdge(i))
        #     if combined.completed and combined.featType is not None:
        #         # prevents duping of looped features
        #         if combined not in completed:
        #             for record in set(combined.meepleRecords):
        #                 self.board.meepled.pop(record)
        #             completed.append(combined)

        ## check each neighbor to see if a chapel has been finished
        for node in self.board.neighbors8(x,y):
            # if the neighbor coords are in our meepled dictioanry
            if (x,y) in self.board.meepled.keys():
                meepled = self.board.meepled.get((x,y))
                # and that meepled record is of the feature on a chapel tile
                if meepled.feature and node.tile.chapel:
                    # check if it has tiles in all 8 neighbor spots
                    if len(self.board.neighbors8(node.x,node.y)) == 8:
                        combined = builtFeature(FeatType.CHAPEL, node.id, (node.x,node.y),0,set())
                        combined.score = 9
                        combined.meepled.append(meepled.color)
                        completed.append(combined)
                        self.board.meepled.pop((x,y))

        return completed

     
    def calculateScore(self, completed: List[builtFeature], quiet):
        for bF in completed:
            if len(bF.meepled) > 0:
                redCount = bF.meepled.count('red')
                blueCount = bF.meepled.count('blue')

                if redCount == blueCount:
                    self.players[0].score += bF.score
                    self.players[1].score += bF.score
                    if not quiet:
                        print(f"Score! Both players earned {bF.score} points!")
                elif redCount > blueCount:
                    self.players[0].score += bF.score
                    if not quiet:
                        print(f"Score! Red player earned {bF.score} points!")
                else:
                    self.players[1].score += bF.score
                    if not quiet:
                        print(f"Score! Blue player earned {bF.score} points!")
                
                if not quiet:
                    print(f"Current score: Red {self.players[0].score} - Blue {self.players[1].score}")
                self.players[0].meepleCount += redCount
                self.players[1].meepleCount += blueCount
                if not quiet:
                    print(f"Meeple Counts: Red {self.players[0].meepleCount} - Blue {self.players[1].meepleCount}")


    def finalScore(self):
        finalScore = [0,0]
        for loc,node in self.board.board.items():
            tile = node.tile

            # if we have a record of that location being meepled
            if loc in self.board.meepled.keys():
                meepled = self.board.meepled.get(loc)

                if meepled.feature and tile.chapel:
                    finalScore[meepled.id] += self.scoreChapel(node)
                elif not meepled.feature:
                    finalScore[meepled.id] += self.scoreGrass(node, meepled)
                else:
                    finalScore[meepled.id] += self.scoreFeature(node, meepled)


            # if tile.occupied is not None and tile.occupied.occupiedBy is not None:
            #     if tile.occupied.featType == FeatType.CHAPEL:
            #         finalScore[tile.occupied.occupiedBy.id] += self.scoreChapel(node)
            #     elif tile.occupied.featType == FeatType.GRASS:
            #         finalScore[tile.occupied.occupiedBy.id] += self.scoreGrass(node)
            #     else:
            #         finalScore[tile.occupied.occupiedBy.id] += self.scoreFeature(node) 
        
        return tuple(finalScore)

    def scoreFeature(self, node: Node, meepled: meepleInfo):
        bF = self.board.findTracked(node,meepled.edge,self.board.trackedFeatures)
        #combined = self.board.buildFeature(node.x,node.y,meepled.edge,meepled.featureObject.featType)
        if bF is not None and bF.meepled:
            return bF.score if bF.featType == FeatType.ROAD else int(bF.score / 2)
        return 0

    def scoreGrass(self, node: Node, meepled: meepleInfo):
        bF = self.board.findTracked(node,meepled.edge,self.board.trackedFields)
        #field = self.board.buildFeature(node.x,node.y,meepled.edge,FeatType.GRASS)
        if bF is not None and bF.meepled:
            score = self.scoreAdjacentCities(bF)
            return score
        return 0

    def scoreAdjacentCities(self, completed: builtFeature):
        citiesChecked = []
        score = 0


        
        for node,edge in completed.adjacentCities.items():
            
            ## get the edge numbers of the city adjacent to the current portion of the field - for dual city tiles
            adjacent = list(set(node.tile.adjacentCity(node.tile.grassAtEdge(edge))))
            
            for cityEdge in adjacent:
                builtCity = self.board.findTracked(node,cityEdge,self.board.trackedFeatures)
                if builtCity is not None and builtCity not in citiesChecked:
                    citiesChecked.append(builtCity)
                    if builtCity.completed:
                        score += 3
            
            # for cityEdge in adjacent:
            #     city = node.tile.featureAtEdge(cityEdge)
            #     ## if we havent explored it yet
            #     if city not in citiesChecked:
            #         # explore it
            #         combinedCity = self.board.buildFeature(node.x, node.y,cityEdge,FeatType.CITY)
            #         # add the cities we've seen to our checked list so we don't double score
            #         for tf in combinedCity.tileFeat:
            #             citiesChecked.append(tf[1])
            #         # add score if the city is completed (carcassone field rules)
            #         if combinedCity.completed:
            #             score += 3

        return score

    def scoreChapel(self, node: Node):
        return len(self.board.neighbors8(node.x, node.y)) + 1