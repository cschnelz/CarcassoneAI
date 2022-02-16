## Game state manager and core game loop
## Holds tile pool and delivers new tiles
## Polls for valid tile locations and tells board where to add tile

from random import random
from Tile import Tile, rotate
from Board import Board
from typing import List
from Feature import *
from Render import *
from Import import importTiles
from Player import Player

# List of player classes that hold score, meeple counts, etc
players = [Player(0), Player(1)]
current_player = 0

# Load the tiles from the TileList json and initialize the list of Tile objects
tileList = importTiles('TileSetSepRoads.json')

# get a random tile from the tile list and remove it
def dispatchTile() -> Tile:
    dispatchId = int(random() * len(tileList))
    tile = tileList[dispatchId]
    del tileList[dispatchId]
    return tile

def dispatchForced(int) -> Tile:
    return tileList[int]

# set up board and players
def initialize(forcedOrder: List):
    if len(forcedOrder) > 0:
        startingTile = dispatchForced(forcedOrder.pop(0))
    else:
        startingTile = dispatchTile()

    # initialize board with a first tile
    board = Board(startingTile)
    #render2(board)
    # self.players
        # create player objects 

    # begin game loop
    runGame(board, forcedOrder)

# given a tile, report locations and orientations it can be placed
def printValidLocations(board: Board, tile: Tile):
    orientations = getOrientations(tile)
    openLocations = board.openLocations

    for i in range(4):
        validLocations = [x for x in openLocations if board.isValid(x[0], x[1], orientations[i])]
        print(f"Open coordinates for orientation {i}: " + str(validLocations))

def printValidLocationsSingle(board: Board, currTile: Tile):
    validLocations = [x for x in board.openLocations if board.isValid(x[0], x[1], currTile)]
    print(f"Open coordinates for current Tile: " + str(validLocations))


def getOrientations(tile: Tile) -> List[Tile]:
    return [rotate(tile, i) for i in range(4)] 

## make a play decision
def playTile(board: Board, currTile: Tile):
    x = 0
    y = 0

    while (True):
        print('\n')
        render3(board, currTile)
        try:
            printValidLocationsSingle(board, currTile)
            res = input("input r to rotate, coordinates x y to insert, or q to quit: ").split()
            if res[0] == 'q':
                sys.exit("Quitting")

            if res[0] == 'r':
                currTile = rotate(currTile, 1)
                continue

            x = int(res[0])
            y = int(res[1])
            if board.isValid(x, y, currTile):
                board.addTile(x, y, currTile)
                break
            print("Invalid insertion, please input again")
        except ValueError:
            print("Improper input, please try again")

    return x, y

# holds information about a connected feature - used for tracking meeple placement, scoring, completion, etc
class combinedFeature:
    def __init__(self):
        self.completed = True
        self.featType = None
        self.score = 0
        self.features = []
        self.meepled: List[Feature] = []
        self.tiles = []
        self.playersOn = []
        self.adjacentCities = set()

    def __eq__(self, __o: object) -> bool:
        return set(self.features) == set(__o.features)

# After a tile is inserted into the board
def checkCompletedFeatures(x, y, board: Board) -> List[combinedFeature]:
    completed = []
    for i in range(4):
        combined = finishedFeature(x,y,board.tileAt(x,y),i,board)
        if combined.completed:
            # prevents duping of looped features
            if combined not in completed:
                completed.append(combined)
    return completed

def shiftCoords(x, y, direction):
    if direction == 0:
        return (x, y-1)
    if direction == 2:
        return (x, y+1)
    if direction == 1:
        return (x+1, y)
    return (x-1, y)

def buildRecursive(x: int, y: int, tile: Tile, inEdge: int, board: Board, featureList):
    inFeature = tile.featureAtEdge(inEdge)

    for edge in inFeature.edges:
        if (tile.id, edge) not in featureList:
            # if there's more edges to this feature, add them
            featureList.append((tile.id, edge))

            # shift to the next tile and recurse
            nextEdge = (edge + 2) % 4
            nextX, nextY = shiftCoords(x, y, edge)
            nextTile = board.getNeighbor(x,y,edge)
            if nextTile is not None:
                buildRecursive(nextX, nextY, nextTile, nextEdge, board, featureList)

def buildFeatures(x, y, tile: Tile, featEdge: int, board: Board):
    featureList = []
    buildRecursive(x, y, tile, featEdge, board, featureList)
    return featureList

# check if a list of features is finished
def finishedFeature(x, y, tile: Tile, featEdge: int, board: Board) -> combinedFeature:
    combined = combinedFeature()
    combined.featType = tile.featureAtEdge(featEdge).featType if tile.featureAtEdge(featEdge) is not None else None
    finishedRecursive(x, y, tile, featEdge, board, combined)
    return combined

def finishedRecursive(x: int, y: int, tile: Tile, inEdge: int, board: Board, combined: combinedFeature):
    inFeature = tile.featureAtEdge(inEdge)
    if inFeature is None:
        combined.completed = False
        return
    if inFeature.occupiedBy is not None:
        if inFeature not in combined.meepled:
            combined.meepled.append(inFeature)
            combined.playersOn.append(inFeature.occupiedBy.color)
    
    if tile.id not in combined.tiles:
        combined.tiles.append(tile.id)
        combined.score += inFeature.score()

    for edge in inFeature.edges:
        if (tile.id, edge) not in combined.features:
            # if there's more edges to this feature, add them
            combined.features.append((tile.id, edge))

            # shift to the next tile and recurse
            nextEdge = inFeature.getOppositeEdge(edge)
            nextX, nextY = shiftCoords(x, y, edge)
            nextTile = board.getNeighbor(x,y,edge)
            if nextTile is not None:
                finishedRecursive(nextX, nextY, nextTile, nextEdge, board, combined)
            else:
                combined.completed = False

# check if a feature has a meeple on it already
def isOccupied(x, y, tile: Tile, featEdge: int, board: Board) -> bool:
    featureList = []
    flag = [False]
    occupiedRecursive(x, y, tile, featEdge, board, featureList, flag)
    return flag[0]

def occupiedRecursive(x: int, y: int, tile: Tile, inEdge: int, board: Board, featureList, flag):
    inFeature = tile.featureAtEdge(inEdge)
    if inFeature is None:
        return
    if inFeature.occupiedBy is not None:
        flag[0] = True

    for edge in inFeature.edges:
        if (tile.id, edge) not in featureList:
            # if there's more edges to this feature, add them
            featureList.append((tile.id, edge))

            # shift to the next tile and recurse
            nextEdge = inFeature.getOppositeEdge(edge)
            nextX, nextY = shiftCoords(x, y, edge)
            nextTile = board.getNeighbor(x,y,edge)
            if nextTile is not None:
                occupiedRecursive(nextX, nextY, nextTile, nextEdge, board, featureList, flag)

def buildField(x: int, y: int, tile: Tile, inEdge: int, board: Board):
    combined = combinedFeature()
    if tile.grasses is not []:
        combined.featType = FeatType.GRASS
        fieldRecursive(x, y, tile, inEdge, board, combined)
    return combined

def fieldRecursive(x: int, y: int, tile: Tile, inEdge: int, board: Board, combined: combinedFeature):
    inField = tile.grassAtEdge(inEdge)

    if inField is None:
        return
    if inField.occupiedBy is not None:
        if inField not in combined.meepled:
            combined.meepled.append(inField)
            combined.playersOn.append(inField.occupiedBy.color)
    
    if tile.id not in combined.tiles:
        combined.tiles.append(tile.id)

    for edge in inField.edges:
        if (tile.id, edge) not in combined.features:
            # if there's more edges to this feature, add them
            combined.features.append((tile.id, edge))
            adjacentCity = set(tile.adjacentCity(inField))
            combined.adjacentCities = combined.adjacentCities.union(adjacentCity)

            # shift to the next tile and recurse
            nextEdge = inField.getOppositeEdge(edge)
            nextX, nextY = shiftCoords(x, y, int(edge / 2))
            nextTile = board.getNeighbor(x,y, int(edge / 2))
            if nextTile is not None:
                fieldRecursive(nextX, nextY, nextTile, nextEdge, board, combined)

def placeMeeple(x: int, y: int, board: Board):
    # if player has meeples and there are places to put meeples, ask where theyd like to place meeple
    
    # get list of open features
    tile = board.tileAt(x, y)

    if tile.features[0].featType is not FeatType.CHAPEL:
        openFeatures = [feat for feat in tile.features if not(isOccupied(x, y, tile, feat.edges[0], board))]
    else:
        openFeatures = [tile.features[0]]

    meeps = players[current_player].meepleCount
    if len(openFeatures) > 0 and meeps > 0:
        print("\nFree features: ")
        option = 0
        for feature in openFeatures:
            print(f"Option: {option} - Feature: {feature.featType.name} on edges: {feature.edges}")
            option += 1

        while(True):
            feat = input(f"Place Meeple ({meeps} remaining)? input feat number or n for no: ")
            try:
                if feat != 'n':
                    # denote that the tile played and the feature selected is occupied
                    if int(feat) > len(openFeatures) - 1:
                        print("out of range")
                        continue
                    tile.occupied = openFeatures[int(feat)]
                    tile.occupied.occupiedBy = players[current_player]
                    players[current_player].meepleCount -= 1
                    break
                break
            except ValueError:
                print("improper input")
                continue
    else:
        if meeps == 0:
            print("Sorry, out of meeples!")
        else:
            print("No available features for placement")

def calculateScore(c: combinedFeature):
    redCount = c.playersOn.count('red')
    blueCount = c.playersOn.count('blue')

    if redCount == blueCount:
        players[0].score += c.score
        players[1].score += c.score
        print(f"Score! Both players earned {c.score} points!")
    elif redCount > blueCount:
        players[0].score += c.score
        print(f"Score! Red player earned {c.score} points!")
    else:
        players[1].score += c.score
        print(f"Score! Blue player earned {c.score} points!")
    
    print(f"Current score: Red {players[0].score} - Blue {players[1].score}")
    players[0].meepleCount += redCount
    players[1].meepleCount += blueCount



def runGame(board: Board, forcedOrder: List):
    # run the game until we have used all tiles
    while len(tileList) > 0:
        if len(forcedOrder) > 0:
            currTile = dispatchForced(forcedOrder.pop(0))
        else:
            currTile = dispatchTile()

        global current_player
        print(f"\nCurrent player: {'red' if current_player == 0 else 'blue'}")

        # get placement location, meeple placement, and then check for completed features and update score
        x, y = playTile(board, currTile)
        placeMeeple(x, y, board)
        completed = checkCompletedFeatures(x, y, board)

        for c in completed:
            for feat in c.meepled:
                feat.occupiedBy = None
            if len(c.playersOn) > 0:
                calculateScore(c)
                
        
        current_player = (current_player + 1) % 2
        ## board.test