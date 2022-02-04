from Manager import Manager
from Tile import Tile, rotate
from Feature import *
from Board import Board
import Render 

## 0 === North, 1 === East, 2 === South, 3 === West

tileList = [ 
    Tile(0, [Road([1,3], False), City([0], True)]), 
    Tile(1, [City([0], True)]),
    Tile(2, [Road([0, 1, 2], True)]),
    Tile(3, [City([1], False)]),
    Tile(4, [City([2], False), City([3], True)]),
    Tile(5, [Road([2], True), City([1], False)])
]


tile = tileList[0]
print(tile.edges)
print(tile.id)

print("\n")
print(tileList[0].canConnectTo(tileList[2], 3))
print(tileList[1].canConnectTo(tileList[3], 0))

board = Board(tileList[0])
board.addTile(-1, 0, tileList[2])
board.addTile(0, -1, tileList[4])
print(board.board)

print(board.board.get((0,0)).neighbors[3].tile.id)

print('\n\n')
Render.render2(board)
print('\n\n')


#t = rotate(tileList[5], 1)
Render.renderPlayOptions(tileList[5])

#2, 0, 4

## def game():
    # core game loop:
        # draw board

        # give tile to current player
        # report valid placement options

        # place tile in accordance to player/computer input

        # poll for meeple placement

        # check for finished features
        # remove any meeples on said features
        # increment score accordingly

        # advance to next player
        # continue

print("\n\nsimulate a turn")
dispatchTile = tileList[5]
#validLocations(board, dispatchTile)
