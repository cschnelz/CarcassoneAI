## Game state manager and core game loop
## Holds tile pool and delivers new tiles
## Polls for valid tile locations and tells board where to add tile

from Tile import Tile, rotate
from Board import Board
from typing import List

tileList = []

class Manager():
    def __init__(self):
        # to track tile in question an how it can be oriented
        self.orientation = []

        # self.board
        # self.players


    # given a tile, report locations and orientations it can be placed
    def validLocations(self, board: Board, tile: Tile):
        self.orientation[0] = tile
        for i in range(1, 4):
            self.orientation[i] = rotate(tile, i)

        openLocations = board.openLocations
        validLocations = [x for x in openLocations if board.isValid(x[0], x[1], tile)]
        print(validLocations)


    ## make a play decision
    def playTile(board: Board, validLocations: List[tuple]):
        pass


    def game():
        pass
