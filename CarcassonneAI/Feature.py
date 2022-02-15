from enum import Enum
from typing import List
import sys
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

    def getOppositeEdge(self, inEdge: int) -> int:
        pass

class City(Feature):
    def __init__(self, edges: List[int], info: bool):
        super().__init__(edges, info)
        self.shield = info
        self.featType = FeatType.CITY

    def getOppositeEdge(self, inEdge: int) -> int:
        return (inEdge + 2) % 4
 
    

class Road(Feature):
    def __init__(self, edges: List[int], info: bool):
        super().__init__(edges, info)
        self.terminated = info
        self.featType = FeatType.ROAD

    def getOppositeEdge(self, inEdge: int) -> int:
        return (inEdge + 2) % 4 

class Grass(Feature):
    def __init__(self, edges: List[int], info: bool):
        self.edges = edges
        self.featType = FeatType.GRASS    

    def getOppositeEdge(self, inEdge: int) -> int:
        if inEdge % 2 == 0:
            return (inEdge) + 5 % 8
        return (inEdge + 3) % 8

class Chapel(Feature):
    def __init__(self, edges: List[int], info: bool):
        self.edges = []
        self.featType = FeatType.CHAPEL

    def getOppositeEdge(self, inEdge: int) -> int:
        pass