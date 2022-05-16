## Holds all information about the current game state

from os import execv
from typing import List

from Board import Board, combinedFeature, Node, meepleInfo, builtFeature
from Feature import *
from Tile import Tile
from Player import Player
from Import import importTiles
from Action import Action, validActions, validActionsLocation
from random import random, choice, shuffle
import copy
import string

class State:
    def __init__(self, players: List[Player], order):
        self.players = players
        self.currentPlayer = 0
        self.tileHist = []
        self.currentActions: List[Action] = []
        
        self.turn = 2
        self.tileList = importTiles('TileSetSepRoads.json')
        
        if len(order) == 0:
            self.order = list(range(0,72))
            shuffle(self.order)
        else:
            self.order = order
            remaining_tiles = list(set(range(0,72)) - set(order))
            shuffle(remaining_tiles)
            self.order.extend(remaining_tiles)

        self.board = Board(self.tileList[self.order.pop(0)][0])
        self.dispatchTile()

        self.hash = "" 
        ## a unique hash string, representing actions in order
        ## 'id xCoord yCoord Meepled Feat/Grass Edge'

    # Get a new tile for current tile
    def dispatchTile(self):
        if len(self.order) == 0:
            self.currentTile = None
            return

        tile_orienations = None
        try:
            index = self.order.pop(0)
            tile_orienations = self.tileList[index]
        except:
            print('oop')

        self.currentActions = validActions(self.board, tile_orienations, self.players[self.currentPlayer].meepleCount > 0)
        if len(self.currentActions) == 0:
            self.order.append(index)
            self.dispatchTile()
        else:
            self.tileHist.append(tile_orienations[0].id)
            self.currentTile = tile_orienations

    def dispatchSpecific(self, index):
        tile_orientations = self.tileList[index]
        self.currentActions = validActions(self.board,tile_orientations,self.players[self.currentPlayer].meepleCount > 0)
        if len(self.currentActions) == 0:
            return False
        self.currentTile = tile_orientations
        self.tileHist.append(tile_orientations[0].id)
        return True

    def getActions(self) -> List[Action]:
        return self.currentActions
    
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
            self.players[self.currentPlayer].meeplesPlaced += 1

        self.playTile(action,quiet)
        self.currentPlayer = (self.currentPlayer + 1) % 2
        self.turn += 1
        self.currentTile = None

    def playTile(self, action: Action, quiet=False):
        ## Add the tile to the board
        node = self.board.addTile(action.x, action.y, action.tile)
        ## Update connected features
        self.board.connectFeatures(node, action.feature, self.players[self.currentPlayer].color)

        ## Calculate and update scores
        completed = self.checkCompletedFeatures(action.x, action.y)
        self.calculateScore(completed, quiet)

    ## dispatches the next tile but picks a random valid location first
    ##   and then only calculates actions for that location
    ## for random policy rollout only
    def dispatchTileOptimized(self):
        index = self.order.pop(0)
        tile_orientations = self.tileList[index]
        shuffle(tile_orientations)
        for i in range(len(tile_orientations)):
            tile_orientation = tile_orientations[i]
            locs = [loc for loc in self.board.openLocations if self.board.isValid(loc[0],loc[1],tile_orientation)]
            
            if len(locs) > 0:
                loc = choice(locs)
                self.currentActions = validActionsLocation(self.board,loc,tile_orientation,self.players[self.currentPlayer].meepleCount > 0)
                self.currentTile = tile_orientations
            
            elif i == len(tile_orientations) - 1:
                self.order.append(index)
                self.dispatchTileOptimized()
           

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
                        #print(self.tileHist)
                        pass

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

     
    def uniqueRemainingTiles(self) -> List[int]:
        found = set()
        remaining = []
        for index in self.order:
            if self.tileList[index][0].imgCode not in found:
                found.add(self.tileList[index][0].imgCode)
                remaining.append(index)
        return remaining

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
        
        meepledLocs = list(self.board.meepled.keys())
        for loc,node in self.board.board.items():
            tile = node.tile

            # if we have a record of that location being meepled
            if loc in meepledLocs:
                meepled = self.board.meepled.get(loc)

                if meepled.feature and tile.chapel:
                    score = self.scoreChapel(node)
                    player = [meepled.id]
                elif not meepled.feature:
                    player, score = self.scoreGrass(node, meepled, meepledLocs)
                else:
                    player, score = self.scoreFeature(node, meepled, meepledLocs)

                for id in player:
                    finalScore[id] += score
        
        return tuple(finalScore)


    def scoreFeature(self, node: Node, meepled: meepleInfo, meepledLocs: list[tuple[int]]):
        bF = self.board.findTracked(node,meepled.edge,self.board.trackedFeatures)

        #combined = self.board.buildFeature(node.x,node.y,meepled.edge,meepled.featureObject.featType)
        if bF is not None and bF.meepled:
            countRed = bF.meepled.count('red')
            countBlue = len(bF.meepled) - countRed
            colorWinner = [0] if countRed > countBlue else [1] if countRed < countBlue else [0,1]
            score = bF.score if bF.featType == FeatType.ROAD else int(bF.score / 2)

            # remove records
            for loc in bF.coordsMeepled:
                meepledLocs.remove(loc)


            return colorWinner, score
        return [0], 0

    def scoreGrass(self, node: Node, meepled: meepleInfo, meepledLocs: list[tuple[int]]):
        bF = self.board.findTracked(node,meepled.edge,self.board.trackedFields)
        #field = self.board.buildFeature(node.x,node.y,meepled.edge,FeatType.GRASS)
        if bF is not None and bF.meepled:

            # find winner and score
            countRed = bF.meepled.count('red')
            countBlue = len(bF.meepled) - countRed
            colorWinner = [0] if countRed > countBlue else [1] if countRed < countBlue else [0,1]
            score = self.scoreAdjacentCities(bF)

            # remove records
            for loc in bF.coordsMeepled:
                meepledLocs.remove(loc)
            return colorWinner, score
        return [0], 0

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

        return score

    def scoreChapel(self, node: Node):
        return len(self.board.neighbors8(node.x, node.y)) + 1



    ## get a list of scores of actively meepled cities and the amount of open edges
    def activeCities(self):
        scores_holes = ([],[])
        for loc, node in self.board.board.items():
            tile = node.tile
            for loc in self.board.meepled.keys():
                meepled = self.board.meepled.get(loc)

                if meepled.feature and meepled.featureObject.featType == FeatType.CITY:
                    bF = self.board.findTracked(node,meepled.edge,self.board.trackedFeatures)
                    if bF is not None and bF.meepled and len(bF.holes) >0:    
                        scores_holes[meepled.id].append((bF.score,len(bF.holes)))
        
        return scores_holes