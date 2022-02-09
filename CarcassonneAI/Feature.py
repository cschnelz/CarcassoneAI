from enum import Enum
from typing import List
import sys

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

    def getOppositeEdge(self, inEdge: int) -> int:
        pass

class City(Feature):
    def __init__(self, edges: List[int], info: bool):
        super().__init__(edges, info)
        self.shield = info

    def getOppositeEdge(self, inEdge: int) -> int:
        return (inEdge + 2) % 4
 
    featType = FeatType.CITY

class Road(Feature):
    def __init__(self, edges: List[int], info: bool):
        super().__init__(edges, info)
        self.terminated = info

    def getOppositeEdge(self, inEdge: int) -> int:
        return (inEdge + 2) % 4

    featType = FeatType.ROAD

class Grass(Feature):
    def __init__(self, edges: List[int], info: bool):
        self.edges = edges

    featType = FeatType.GRASS

    def getOppositeEdge(self, inEdge: int) -> int:
        if inEdge % 2 == 0:
            return (inEdge) + 5 % 8
        return (inEdge + 3) % 8

class Chapel(Feature):
    def __init__(self, edges: List[int], info: bool):
        self.edges = []

    featType = FeatType.CHAPEL

    def getOppositeEdge(self, inEdge: int) -> int:
        pass