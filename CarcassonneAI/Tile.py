import sys
from typing import List
from Feature import *

class Tile:
    def __init__(self, id: int, features: List[Feature]):
        if not isinstance(features, List):
            sys.exit("bad features")

        self.id: int = id
        self.features: List[Feature] = features
        self.edges: List[FeatType] = [None] * 4

        for feature in self.features:
            for edge in feature.edges:
                self.edges[edge] = feature.featType

    ## Checks if some otherTile can connect to this tile on given edge
    def canConnectTo(self, otherTile, edge: int) -> bool:
        return self.edges[edge] == otherTile.edges[(edge + 2) % 4]



# returns a rotated version of input tile where north becomes east = 1, south = 2, west = 3
def rotate(tile: Tile, i: int) -> Tile:
    newFeatures = tile.features
    for feat in newFeatures:
        
