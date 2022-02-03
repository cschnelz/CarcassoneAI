from Tile import Tile
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
    Tile(5, [Road([2], True), Road([1], False)])
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
print("curr tile:\n")
Render.renderTile(tileList[5])
print("isValid -1 -1?\n")
print(board.isValid(-1, -1, tileList[5]))

board.addTile(-1, -1, tileList[5])