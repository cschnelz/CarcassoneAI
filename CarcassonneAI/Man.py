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

board = Board(rotate(tileList[25], 0))
board.addTile(0, -1, rotate(tileList[34], 2))
board.addTile(0, -2, rotate(tileList[43], 0))
board.addTile(0, 1, rotate(tileList[16], 2))
board.addTile(-1, 1, rotate(tileList[46], 3))


render3(board, tileList[50])
render2(board)

featureList = buildFeatures(0, 0, board.tileAt(0,0), 0, board)
print(featureList)
#print(finishedFeature(0, 0, board.tileAt(0,0), 0, board))

tile1 = Tile(888, [City([0], False), Road([1,2], False)], 'zz', 0)
print(tile1.grass)


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
