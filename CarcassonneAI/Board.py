from Tile import Tile
from typing import List

def neighborCoordinates(x: int, y: int) -> List[int]:
    return [(x, y+1), 
        (x+1, y), 
        (x, y-1), 
        (x-1, y)]

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
        self.openLocations = [(0,1), (1, 0), (0, -1), (-1, 0)]

    
    def addTile(self, x:int, y: int, tile: Tile):
        node = Node(x, y, tile)

        neighbors = neighborCoordinates(x, y)
        
        # for all neighbor coordinates of new node
        for i in range(4):
            # if there is a prev node at that coordinate
            neighbor = self.board.get(neighbors[i])
            if neighbor is not None:
                # it is a neighbor of the new node
                node.neighbors[i] = neighbor
                # the new node is a neighbor of the prev node to the opposite cardinal
                neighbor.neighbors[(i+2)%4] = node

        self.board[(x, y)] = node



        

    


