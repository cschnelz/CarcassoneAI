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





board = Board(tileList[70])
tile = tileList[46]
tile.occuped = tile.features[0]
tile.features[0].occupiedBy = Player(0)
board.addTile(0, 1, tile)
board.addTile(0, 2, tileList[46])

# board = Board(tileList[15])
# tile = rotate(tileList[50], 1)
# tile.occupied = tile.features[0]
# tile.features[0].occupiedBy = Player(0)
# board.addTile(-1, 0, tile)
# board.addTile(-1, -1, tileList[1])


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
