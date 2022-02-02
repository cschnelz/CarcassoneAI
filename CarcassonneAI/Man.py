from Tile import Tile
from Feature import *
from Board import Board
import Render 

## 0 === North, 1 === East, 2 === South, 3 === West

tileList = [ 
    Tile(0, [Road([1,3], False)]), 
    Tile(1, [City([0], True)]),
    Tile(2, [Road([1, 2], True)]),
    Tile(3, [City([1], False)])
]


tile = tileList[0]
print(tile.edges)
print(tile.id)

print("\n")
print(tileList[0].canConnectTo(tileList[2], 3))
print(tileList[1].canConnectTo(tileList[3], 0))

board = Board(tileList[0])
board.addTile(-1, 0, tileList[2])
print(board.board)

print('\n\n')
Render.render(board)