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

def runGame(board: Board, forcedOrder: List):
    # run the game until we have used all tiles
    while len(tileList) > 0:
        if len(forcedOrder) > 0:
            currTile = dispatchForced(forcedOrder.pop(0))
        else:
            currTile = dispatchTile()

        ## draws the board and current tile
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
        
        for i in range(4):
            if finishedFeature(x,y,board.tileAt(x,y),i,board):
                print(f"finished feature originating from {x}, {y}, direction: {i}")
        ## board.test