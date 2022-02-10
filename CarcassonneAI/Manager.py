## Game state manager and core game loop
## Holds tile pool and delivers new tiles
## Polls for valid tile locations and tells board where to add tile

from random import random
from xmlrpc.client import Boolean
from Tile import Tile, rotate
from Board import Board
from typing import List
from Feature import *
from Render import *
from Import import importTiles

# List of player classes that hold score, meeple counts, etc
players = []
current_player = 0

# Load the tiles from the TileList json and initialize the list of Tile objects
tileList = importTiles('TileSetSepRoads.json')


# get a random tile from the tile list and remove it
def dispatchTile() -> Tile:
    dispatchId = int(random() * len(tileList))
    tile = tileList[dispatchId]
    del tileList[dispatchId]
    return tile

# set up board and players
def initialize():
    startingTile = dispatchTile()

    # initialize board with a first tile
    board = Board(startingTile)
    render2(board)
    # self.players
        # create player objects 

    # begin game loop
    runGame(board)

# given a tile, report locations and orientations it can be placed
def printValidLocations(board: Board, tile: Tile):
    orientations = getOrientations(tile)
    openLocations = board.openLocations

    for i in range(4):
        validLocations = [x for x in openLocations if board.isValid(x[0], x[1], orientations[i])]
        print(f"Open coordinates for orientation {i}: " + str(validLocations))

def getOrientations(tile: Tile) -> List[Tile]:
    return [rotate(tile, i) for i in range(4)] 

## make a play decision
def playTile(board: Board, validLocations: List[tuple]):
    pass

# After a tile is inserted into the board
def checkCompletedFeatures():
    pass


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




# check if a list of city Features is finished
def finishedFeature(x, y, tile: Tile, featEdge: int, board: Board) -> bool:
    featureList = []
    flag = [True]
    finishedRecursive(x, y, tile, featEdge, board, featureList, flag)
    return flag[0]

def finishedRecursive(x: int, y: int, tile: Tile, inEdge: int, board: Board, featureList, flag):
    inFeature = tile.featureAtEdge(inEdge)
    if inFeature is None:
        flag[0] = False
        return

    for edge in inFeature.edges:
        if (tile.id, edge) not in featureList:
            # if there's more edges to this feature, add them
            featureList.append((tile.id, edge))

            # shift to the next tile and recurse
            nextEdge = inFeature.getOppositeEdge(edge)
            nextX, nextY = shiftCoords(x, y, edge)
            nextTile = board.getNeighbor(x,y,edge)
            if nextTile is not None:
                finishedRecursive(nextX, nextY, nextTile, nextEdge, board, featureList, flag)
            else:
                flag[0] = False

def runGame(board: Board):
    # run the game until we have used all tiles
    while len(tileList) > 0:
        currTile = dispatchTile()
        orientations = getOrientations(currTile)


        renderPlayOptions(currTile)
        printValidLocations(board, currTile)

        ## draws the board and current tile
        render3(board, currTile)

        o, x, y = input("input orientation and x and y coords: ").split()
        x = int(x)
        y = int(y)
        o = int(o)
        board.addTile(x, y, orientations[o])
        
        for i in range(4):
            if finishedFeature(x,y,board.tileAt(x,y),i,board):
                print(f"finished feature originating from {x}, {y}, direction: {o}")
        ## board.test
        render2(board)