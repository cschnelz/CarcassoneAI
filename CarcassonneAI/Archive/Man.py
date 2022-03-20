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

# board = Board(rotate(tileList[0], 1))
# board.addTile(0, -1, rotate(tileList[30], 2))
# board.addTile(1, -1, rotate(tileList[27], 0))
# board.addTile(1, 0, rotate(tileList[56], 1))
# board.addTile(2, -1, rotate(tileList[15], 3))
# board.addTile(2, 0, tileList[50])

boardC = Board(rotate(tileList[4],1))
chapelTile = tileList[35]
chapelTile.occupied = chapelTile.features[0]
chapelTile.occupied.occupiedBy = players[1]

boardC.addTile(0,-1,chapelTile)
boardC.addTile(0,-2,rotate(tileList[9],1))
boardC.addTile(1,-1,tileList[25])
boardC.addTile(-1,-1,tileList[34])
boardC.addTile(1,-2,tileList[14])
boardC.addTile(1,0, rotate(tileList[24],1))
boardC.addTile(-1,0, rotate(tileList[28],2))
boardC.addTile(-1,-2, rotate(tileList[41],3))

render3(boardC, tileList[50], players)
input()
comp = checkCompletedFeatures(-1,-2,boardC)
for c in comp:
    for feat in c.meepled:
        feat.occupiedBy = None
    if len(c.playersOn) > 0:
        calculateScore(c)

#print([tile.id for tile in board.neighbors8(0,-1)])

render3(boardC, tileList[50], players)
render2(boardC)
input()
#2, 0, 4


