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
    render2(board)
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
    features: List[Feature] = []
    meepled: List[Feature] = []

# After a tile is inserted into the board
def checkCompletedFeatures(x, y, board: Board) -> List[combinedFeature]:
    completed = []
    for i in range(4):
        combined = finishedFeature(x,y,board.tileAt(x,y),i,board)
        if combined.completed:
            print(f"finished feature originating from {x}, {y}, direction: {i}")
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
        combined.meepled.append(inFeature)

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

def placeMeeple(x: int, y: int, board: Board):
    # if player has meeples and there are places to put meeples, ask where theyd like to place meeple
    
    # get list of open features
    tile = board.tileAt(x, y)
    openEdges = []

    if tile.features[0].featType is not FeatType.CHAPEL:
        openFeatures = [feat for feat in tile.features if not(isOccupied(x, y, tile, feat.edges[0], board))]
    else:
        openFeatures = [tile.features[0]]

    if len(openFeatures) > 0:
        print("Free features: ")
        for feature in openFeatures:
            print(f"Feature: {feature.featType.name} on edges: {feature.edges}")
            openEdges.extend(feature.edges)

        while(True):
            feat = input("Place Meeple? input feat number or n for no: ")
            try:
                if feat != 'n':
                    # denote that the tile played and the feature selected is occupied
                    if int(feat) > len(openFeatures) - 1:
                        print("out of range")
                        continue
                    tile.occupied = openFeatures[int(feat)]
                    openFeatures[int(feat)].occupiedBy = players[current_player]
                    break
            except ValueError:
                print("improper input")
                continue
    else:
        print("No available features for placement")

def runGame(board: Board, forcedOrder: List):
    # run the game until we have used all tiles
    while len(tileList) > 0:
        if len(forcedOrder) > 0:
            currTile = dispatchForced(forcedOrder.pop(0))
        else:
            currTile = dispatchTile()
        
        x, y = playTile(board, currTile)
        placeMeeple(x, y, board)
        completed = checkCompletedFeatures(x, y, board)
        
        #for feature in completed:

        global current_player
        current_player = (current_player + 1) % 2
        ## board.test