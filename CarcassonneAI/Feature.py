from enum import Enum
from typing import List
import sys

from bleach import clean
from Player import Player

class FeatType(Enum):
    CITY = 1
    ROAD = 2
    GRASS = 3
    CHAPEL = 4

class Feature():
    def __init__(self, edges: List[int], info: bool):
        if not isinstance(edges, List):
            sys.exit("bad edges")
        if not isinstance(info, bool):
            sys.exit("bad info")
        self.edges = edges
        self.featType = None
        self.occupiedBy: Player = None

    # def __str__(self):
    #     return f"Feature: {self.featType.name} on edges {self.edges}"

    def getOppositeEdge(self, inEdge: int) -> int:
        pass

    def score(self):
        pass

class City(Feature):
    def __init__(self, edges: List[int], info: bool):
        super().__init__(edges, info)
        self.shield = info
        self.featType = FeatType.CITY
        self.scorePer = 2

    def getOppositeEdge(self, inEdge: int) -> int:
        return (inEdge + 2) % 4
 
    def score(self):
        return 2 + (2 if self.shield else 0)

class Road(Feature):
    def __init__(self, edges: List[int], info: bool):
        super().__init__(edges, info)
        self.terminated = info
        self.featType = FeatType.ROAD
        self.scorePer = 1

    def getOppositeEdge(self, inEdge: int) -> int:
        return (inEdge + 2) % 4 

    def score(self):
        return 1

class Grass(Feature):
    def __init__(self, edges: List[int], info: bool):
        super().__init__(edges, info)
        self.featType = FeatType.GRASS
        self.scorePer = 0    

    def getOppositeEdge(self, inEdge: int) -> int:
        if inEdge % 2 == 0:
            return (inEdge + 5) % 8
        return (inEdge + 3) % 8

    def score(self):
        return 0

    def cleanEdges(self):
        cleanEdges = self.edges.copy()
        for i in range(4):
            if i*2 in cleanEdges and i*2+1 in cleanEdges:
                cleanEdges.remove(i*2+1)
        return cleanEdges


class Chapel(Feature):
    def __init__(self, edges: List[int], info: bool):
        self.edges = []
        self.featType = FeatType.CHAPEL
        self.scorePer = 9

    def getOppositeEdge(self, inEdge: int) -> int:
        pass

    def score(self):
        return 0