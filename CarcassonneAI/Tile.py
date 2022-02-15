import sys
from typing import List
from Feature import *

class Tile:
    def __init__(self, id: int, features: List[Feature], imgCode: str, orientation: int):
        if not isinstance(features, List):
            sys.exit("bad features")

        self.id: int = id
        self.features: List[Feature] = features
        self.grass = []
        self.edges: List[FeatType] = [None] * 4
        
        self.orientation = orientation
        self.occupied: Feature = None
        
        self.chapel = False
        self.imgCode: str = imgCode

        for feature in self.features:
            if feature.featType == FeatType.CHAPEL:
                self.chapel = True
            for edge in feature.edges:
                self.edges[edge] = feature.featType

        for i in range(4):
            if self.edges[i] is None:
                self.grass.append(Grass([i*2, i*2+1], None))
            if self.edges[i] == FeatType.ROAD:
                self.grass.append(Grass([i*2], None))
                self.grass.append(Grass([i*2+1], None))

    ## Checks if some otherTile can connect to this tile on given edge
    def canConnectTo(self, otherTile, edge: int) -> bool:
        return self.edges[edge] == otherTile.edges[(edge + 2) % 4]

    ## return the feature object of given edge, or None
    def featureAtEdge(self, edge: int) -> Feature:
        for feature in self.features:
            if feature.featType is not FeatType.GRASS and edge in feature.edges:
                return feature
        return None

# returns a rotated version of input tile where north becomes east = 1, south = 2, west = 3
def rotate(tile: Tile, i: int) -> Tile:
    newFeatures = []
    for feat in tile.features:
        if feat.featType == FeatType.CITY:
            newEdges = [(e + i) % 4 for e in feat.edges]
            newFeatures.append(City(newEdges, feat.shield))
        elif feat.featType == FeatType.ROAD:
            newEdges = [(e + i) % 4 for e in feat.edges]
            newFeatures.append(Road(newEdges, feat.terminated))
    return Tile(tile.id, newFeatures, tile.imgCode, (tile.orientation + i)%4)

