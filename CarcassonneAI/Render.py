from Board import Board, Node
from Feature import *
from Tile import Tile

def printFeature(tile: Tile, cardinal: int) -> str:
    if tile.edges[cardinal] == FeatType.CITY:
        return "C"
    elif tile.edges[cardinal] == FeatType.ROAD:
        return "R"
    
    if cardinal == 0 or cardinal == 2:
        return "-"
    return "|"

def renderTile(tile: Tile):
    print(" -  " + printFeature(tile, 0) + "  - ")   
    print("|       |")
    print(printFeature(tile,3) + "  T." + str(tile.id) + "  " + printFeature(tile,1))
    print("|       |")
    print(" -  " + printFeature(tile, 2) + "  - ")

# render a board with basic characters - goes row by row 
def render2(board: Board):
    # print the coordinate grid
    output = "   "
    for x in range(board.minX, board.maxX + 1):
        if x < 0:
            output += f"   {x}    "
        else:
            output += f"    {x}    "
    print(output + "\n")

    basicEdge = " - - - - "
    # print the top edge of the tile
    for y in range(board.minY, board.maxY+1):
        output = "   "
        for x in range(board.minX, board.maxX+1):
            node = board.board.get((x,y))
            if (x, y) in board.openLocations or node is None:
                output += basicEdge
            else:
                output += " -  " + printFeature(node.tile, 0) + "  - "
        print(output)

        # print some vertical edges
        print("   " + "|       |" * (board.maxX - board.minX + 1))

        # print the middle vert segment, with care for tile features
        if y < 0:
            output = f"{y} "
        else:
            output = f" {y} "
        for x in range(board.minX, board.maxX+1):
            node = board.board.get((x,y))
            if (x, y) in board.openLocations:
                output += "|  opn  |"
            elif node is None:
                output += "|       |"
            else:
                output += printFeature(node.tile,3) + "  T." + str(node.tile.id) + "  " + printFeature(node.tile,1)
        print(output)

        print("   " + "|       |" * (board.maxX - board.minX + 1))

        # print the bottom edge
        output = "   "
        for x in range(board.minX, board.maxX+1):
            node = board.board.get((x,y))
            if (x, y) in board.openLocations or node is None:
                output += basicEdge
            else:
                output += " -  " + printFeature(node.tile, 2) + "  - "
        print(output)
