## Holds all information about the current game state

from typing import List

from Board import Board, combinedFeature, Node, meepleInfo
from Feature import *
from Player import Player
from Import import importTiles
from Action import Action
from random import random
import copy


class State:
    def __init__(self, players: List[Player], order):
        self.players = players
        self.currentPlayer = 0
        self.order = order
        
        self.tileList = importTiles('TileSetSepRoads.json')
        self.currentTile = self.dispatchTile() if len(self.order) == 0 else self.dispatchTile(self.order.pop(0))

        self.board = Board(self.currentTile)
        self.currentTile = self.dispatchTile() if len(self.order) == 0 else self.dispatchTile(self.order.pop(0))
    
    # Get a new tile for current tile
    def dispatchTile(self, index=None):
        if index is None:
            dispatchId = int(random() * len(self.tileList))
            tile = self.tileList[dispatchId]
            del self.tileList[dispatchId]
        
        else:
            dispatchId = index
            tile = self.tileList[dispatchId]
        
        return tile
    
    def playTile(self, action: Action, quiet=False):
        node = self.board.addTile(action.x, action.y, action.tile)
        self.board.connectFeatures(node, action.feature, self.players[self.currentPlayer].color)

        completed = self.checkCompletedFeatures(action.x, action.y)
        self.calculateScore(completed, quiet)

        self.currentTile = self.dispatchTile() if len(self.order) == 0 else self.dispatchTile(self.order.pop(0))

    def scoreDelta(self):
        score = (self.players[0].score,self.players[1].score)
        fscore = self.finalScore()
        return (score[0] + fscore[0]) - (score[1] + fscore[1])

    ## Called in PlayTile
    def checkCompletedFeatures(self, x, y) -> List[combinedFeature]:
        completed = []
        for i in range(4):
            tile = self.board.tileAt(x,y)
            combined = self.board.buildFeature(x,y,i,tile.featureAtEdge(i))
            if combined.completed and combined.featType is not None:
                # prevents duping of looped features
                if combined not in completed:
                    for record in set(combined.meepleRecords):
                        self.board.meepled.pop(record)
                    completed.append(combined)

        ## check each neighbor to see if a chapel has been finished
        for node in self.board.neighbors8(x,y):
            # if the neighbor coords are in our meepled dictioanry
            if (x,y) in self.board.meepled.keys():
                meepled = self.board.meepled.get((x,y))
                # and that meepled record is of the feature on a chapel tile
                if meepled.feature and node.tile.chapel:
                    # check if it has tiles in all 8 neighbor spots
                    if len(self.board.neighbors8(node.x,node.y)) == 8:
                        combined = combinedFeature()
                        combined.score = 9
                        combined.playersOn.append(meepled.color)
                        combined.meepled.append(node.tile.features[0]) 
                        completed.append(combined)

            # if node.tile.occupied is not None and node.tile.occupied.featType == FeatType.CHAPEL:
            #     if len(self.board.neighbors8(node.x,node.y)) == 8:
            #         combined = combinedFeature()
            #         combined.score = 9
            #         combined.playersOn.append(node.tile.features[0].occupiedBy.color)
            #         combined.meepled.append(node.tile.features[0]) 
            #         completed.append(combined)
            # dispatchId = int(random() * len(self.tileList))
        return completed

     
    def calculateScore(self, completed: List[combinedFeature], quiet):
        for c in completed:
            for feat in c.meepled:
                feat.occupiedBy = None
            if len(c.playersOn) > 0:
                redCount = c.playersOn.count('red')
                blueCount = c.playersOn.count('blue')

                if redCount == blueCount:
                    self.players[0].score += c.score
                    self.players[1].score += c.score
                    if not quiet:
                        print(f"Score! Both players earned {c.score} points!")
                elif redCount > blueCount:
                    self.players[0].score += c.score
                    if not quiet:
                        print(f"Score! Red player earned {c.score} points!")
                else:
                    self.players[1].score += c.score
                    if not quiet:
                        print(f"Score! Blue player earned {c.score} points!")
                
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
        combined = self.board.buildFeature(node.x,node.y,meepled.edge,meepled.featureObject.featType)
        if combined.meepled:
            return combined.score if combined.featType == FeatType.ROAD else int(combined.score / 2)
        return 0

    def scoreGrass(self, node: Node, meepled: meepleInfo):
        field = self.board.buildFeature(node.x,node.y,meepled.edge,FeatType.GRASS)
        if field.meepled:
            score = self.scoreAdjacentCities(field)
            return score
        return 0

    def scoreAdjacentCities(self, completed: combinedFeature):
        citiesChecked = []
        score = 0
        
        for i in range(0, len(completed.nodeEdges)):
            node: Node = completed.nodeEdges[i][0]
            edge = completed.nodeEdges[i][1]
            ## get the edge numbers of the city adjacent to the current portion of the field
            adjacent = list(set(node.tile.adjacentCity(node.tile.grassAtEdge(edge))))
            
            
            for cityEdge in adjacent:
                city = node.tile.featureAtEdge(cityEdge)
                ## if we havent explored it yet
                if city not in citiesChecked:
                    # explore it
                    combinedCity = self.board.buildFeature(node.x, node.y,cityEdge,FeatType.CITY)
                    # add the cities we've seen to our checked list so we don't double score
                    for tf in combinedCity.tileFeat:
                        citiesChecked.append(tf[1])
                    # add score if the city is completed (carcassone field rules)
                    if combinedCity.completed:
                        score += 3

        return score

    def scoreChapel(self, node: Node):
        return len(self.board.neighbors8(node.x, node.y)) + 1