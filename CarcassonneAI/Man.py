from Tile import Tile, rotate
from Feature import *
from Board import Board
from Render import *
from Import import importTiles
from Manager import buildFeatures, checkCompletedFeatures, finishedFeature, buildField

## 0 === North, 1 === East, 2 === South, 3 === West


tileList: List[Tile] = importTiles('TileSetSepRoads.json')


tile = tileList[0]
print(tile.edges)
print(tile.id)

print("\n")
print(tileList[0].canConnectTo(tileList[2], 3))
print(tileList[1].canConnectTo(tileList[3], 0))

players = [Player(0), Player(1)]
current_player = 0



tile = tileList[70]
board = Board(tile)

t1 = tileList[40]
t1.occupied = tile.grasses[1]
t1.occupied.occupiedBy = players[0]
board.addTile(0, 1, t1)

tile = rotate(tileList[14],2)
tile.occupied = tile.features[0]
tile.occupied.occupiedBy = players[1]
board.addTile(0, 2, tile)
# board = Board(tileList[15])
# tile = rotate(tileList[50], 1)
# tile.occupied = tile.features[0]
# tile.features[0].occupiedBy = Player(0)
# board.addTile(-1, 0, tile)
# board.addTile(-1, -1, tileList[1])

combined = buildField(0,0,board.tileAt(0,0),5,board)

render3(board, tileList[50])
render2(board)
input()
#2, 0, 4


