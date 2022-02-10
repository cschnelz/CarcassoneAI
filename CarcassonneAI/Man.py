from Tile import Tile, rotate
from Feature import *
from Board import Board
from Render import *
from Import import importTiles
from Manager import buildFeatures, finishedFeature

## 0 === North, 1 === East, 2 === South, 3 === West


tileList = importTiles('TileSetSepRoads.json')


tile = tileList[0]
print(tile.edges)
print(tile.id)

print("\n")
print(tileList[0].canConnectTo(tileList[2], 3))
print(tileList[1].canConnectTo(tileList[3], 0))


board = Board(rotate(tileList[0], 1))
board.addTile(0, -1, rotate(tileList[30], 2))
board.addTile(1, -1, rotate(tileList[27], 0))
board.addTile(1, 0, rotate(tileList[56], 1))
board.addTile(2, -1, rotate(tileList[15], 3))




board.addTile(2, 0, tileList[50])
for i in range(4):
    if finishedFeature(2,0,board.tileAt(2,0),i,board):
        print(f"finished feature originating from {2}, {0}, direction: {i}")
    else:
        print(f"no finished features in direction {i}")


render3(board, tileList[50])
render2(board)
input()
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

#validLocations(board, dispatchTile)
