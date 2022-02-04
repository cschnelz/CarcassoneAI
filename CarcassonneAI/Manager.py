## Game state manager and core game loop
## Holds tile pool and delivers new tiles
## Polls for valid tile locations and tells board where to add tile

from random import random
from Tile import Tile, rotate
from Board import Board
from typing import List
from Feature import *
from Render import *

#tileList = IMPORT FROM TILESET.JSON
sampleTileList = [ 
    Tile(0, [Road([1,3], False), City([0], True)]), 
    Tile(1, [City([0], True)]),
    Tile(2, [Road([0, 1, 2], True)]),
    Tile(3, [City([1], False)]),
    Tile(4, [City([2], False), City([3], True)]),
    Tile(5, [Road([2], True), City([1], False)])
]


def dispatchTile() -> Tile:
    dispatchId = int(random() * len(sampleTileList))
    tile = sampleTileList[dispatchId]
    del sampleTileList[dispatchId]
    return tile

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
def validLocations(board: Board, tile: Tile):
    orientation = []
    for i in range(4):
        orientation.append(rotate(tile, i))
        openLocations = board.openLocations
        validLocations = [x for x in openLocations if board.isValid(x[0], x[1], orientation[i])]
        print(f"Open coordinates for orientation {i}: " + str(validLocations))

def getOrientations(tile: Tile) -> List[Tile]:
    return [rotate(tile, i) for i in range(4)] 

## make a play decision
def playTile(board: Board, validLocations: List[tuple]):
    pass


def runGame(board: Board):
    # run the game until we have used all tiles
    while len(sampleTileList) > 0:
        currTile = dispatchTile()
        renderPlayOptions(currTile)
        orientations = getOrientations(currTile)
        validLocations(board, currTile)
        o, x, y = input("input orientation and x and y coords: ").split()
        board.addTile(int(x), int(y), orientations[int(o)])
        render2(board)