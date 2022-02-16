import sys
from typing import List
from Feature import *

class Tile:
    def __init__(self, id: int, features: List[Feature], grasses: List[Grass], imgCode: str, orientation: int):
        if not isinstance(features, List):
            sys.exit("bad features")

        self.id: int = id
        self.features: List[Feature] = features
        self.grasses = grasses
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


    ## Checks if some otherTile can connect to this tile on given edge
    def canConnectTo(self, otherTile, edge: int) -> bool:
        return self.edges[edge] == otherTile.edges[(edge + 2) % 4]

    ## return the feature object of given edge, or None
    def featureAtEdge(self, edge: int) -> Feature:
        for feature in self.features:
            if feature.featType is not FeatType.GRASS and edge in feature.edges:
                return feature
        return None

    def grassAtEdge(self, edge: int) -> Grass:
        for grass in self.grasses:
            if edge in grass.edges:
                return grass
        return None

    ## given a field object, return any cities adjacent to it
    def adjacentCity(self, grass: Grass):
        cities = []
        for edge in grass.edges:
            if edge == 2 or edge == 7:
                if self.edges[0] == FeatType.CITY:
                    cities.append(self.featureAtEdge(0))
            elif edge == 1 or edge == 4:
                if self.edges[1] == FeatType.CITY:
                    cities.append(self.featureAtEdge(1))
            elif edge == 3 or edge == 6:
                if self.edges[2] == FeatType.CITY:
                    cities.append(self.featureAtEdge(2))
            else: # 0 or 5
                if self.edges[3] == FeatType.CITY:
                    cities.append(self.featureAtEdge(3))

        # div 2
        # if original odd add 1
        # if original even - 1
        return cities

# returns a rotated version of input tile where north becomes east = 1, south = 2, west = 3
def rotate(tile: Tile, i: int) -> Tile:
    newFeatures = []
    newGrass = []
    for feat in tile.features:
        if feat.featType == FeatType.CITY:
            newEdges = [(e + i) % 4 for e in feat.edges]
            newFeatures.append(City(newEdges, feat.shield))
        elif feat.featType == FeatType.ROAD:
            newEdges = [(e + i) % 4 for e in feat.edges]
            newFeatures.append(Road(newEdges, feat.terminated))
    for grass in tile.grasses:
        newEdges = [(e + (i * 2)) % 8 for e in grass.edges]
        newGrass.append(Grass(newEdges, False))
    return Tile(tile.id, newFeatures, newGrass, tile.imgCode, (tile.orientation + i)%4)

