from Tile import Tile
from typing import List
import sys

# Tracks the construction of the game board

def neighborCoordinates(x: int, y: int) -> List[tuple]:
    return [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]

def neighborCoordinates8(x: int, y:int) -> List[tuple]:
    eight = neighborCoordinates(x,y)
    eight.extend([(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)])
    return eight

class Node:
    def __init__(self, x: int, y: int, tile: Tile):
        self.tile = tile
        self.x = x
        self.y = y

        ## 0 === North, 1 === east, 2 === south, 3 === west
        self.neighbors = [None] * 4
           
    

class Board:
    def __init__(self, startingTile: Tile):
        self.board = {(0, 0) : Node(0, 0, startingTile)}
        self.openLocations = {(0,1), (1, 0), (0, -1), (-1, 0)}
        self.minX = self.minY = -1
        self.maxX = self.maxY = 1

    #def copy(self):

    
    def addTile(self, x:int, y: int, tile: Tile):
        if not self.isValid(x, y, tile):
            sys.exit("invalid placement")

        node = Node(x, y, tile)
        neighbors = neighborCoordinates(x, y)
        
        # for all neighbor coordinates of new node
        for i in range(4):
            coord = neighbors[i]
            # if there is a prev node at that coordinate
            neighbor = self.board.get(coord)
            if neighbor is not None:
                # it is a neighbor of the new node
                node.neighbors[i] = neighbor
                # the new node is a neighbor of the prev node to the opposite cardinal
                neighbor.neighbors[(i+2)%4] = node
            # if there is no node there
            elif coord not in self.openLocations:
                # add the coords as a new open location for tiles
                self.openLocations.add(coord)

        self.board[(x, y)] = node
        self.openLocations.remove((x, y))
        self.expandBounds(neighbors)

    # given a tile and a location, checks if it can be inserted there
    def isValid(self, x: int, y: int, tile: Tile) -> bool:
        # for this location
        # for all neighbor tiles of this location
            # can the tile link to that neighbor in that direction
        if (x, y) not in self.openLocations:
            return False
        neighbors = neighborCoordinates(x, y)

        # for all adjacent coords
        for i in range(4):
            coord = neighbors[i]
            # if there is a tile there
            if self.board.get(coord) is not None:
                # test if the new tile is valid in that direction
                if not tile.canConnectTo(self.board.get(coord).tile, i):
                    return False

        # if we get through all directions, the tile can fit
        return True

    def getNeighbor(self, x: int, y: int, direction: int) -> Tile:
        node = self.board.get((x, y))
        if node.neighbors[direction] is not None:
            return node.neighbors[direction].tile
        return None

    def tileAt(self, x: int, y: int) -> Tile:
        node = self.board.get((x,y))
        return node.tile if node is not None else None

    # track the bounding coords of the game board
    def expandBounds(self, coords: List[tuple]):
        for coord in coords:
            self.minX = min(self.minX, coord[0])
            self.minY = min(self.minY, coord[1])
            self.maxX = max(self.maxX, coord[0])
            self.maxY = max(self.maxY, coord[1])

    ## orthogonal and diagonal neighbors 
    def neighbors8(self, x:int, y:int) -> list[Node]:
       return [self.board.get(coord) for coord in neighborCoordinates8(x,y) if self.board.get(coord) is not None]
    


