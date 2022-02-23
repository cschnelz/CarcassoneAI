from Tile import Tile, rotate
from Feature import *
from Board import Board
from Render import *
from Import import importTiles
from Manager import *

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


t3 = rotate(tileList[0], 1)
board = Board(t3)
c3 = t3.features[0]

t2 = rotate(tileList[30],2)
board.addTile(0, -1, t2)
c2 = t2.features[0]

t1 = rotate(tileList[27], 0)
board.addTile(1, -1, t1)
c1 = t1.features[0]

t4 = rotate(tileList[56], 1)
board.addTile(1, 0, t4)
c4 = t4.features[0]

board.addTile(1,-2, rotate(tileList[25], 1))
board.addTile(0,-2, rotate(tileList[14], 3))
board.addTile(-1,-1, rotate(tileList[24], 3))
board.addTile(-1,0, rotate(tileList[28], 2))

completed = buildFeature(0,0,7,board, FeatType.GRASS)
#self.assertEqual(completed.adjacentCities, {c1,c2,c3})
cities = adjacentCities(completed)

render3(board, tileList[50], players)
render2(board)
input()
#2, 0, 4


