from enum import Enum
from typing import List
import sys

class FeatType(Enum):
    CITY = 1
    ROAD = 2


class Feature():
    def __init__(self, edges: List[int], info: bool):
        if not isinstance(edges, List):
            sys.exit("bad edges")
        if not isinstance(info, bool):
            sys.exit("bad info")
        self.edges = edges

class City(Feature):
    def __init__(self, edges: List[int], info: bool):
        super().__init__(edges, info)
        self.shield = info

    featType = FeatType.CITY

class Road(Feature):
    def __init__(self, edges: List[int], info: bool):
        super().__init__(edges, info)
        self.terminated = info

    featType = FeatType.ROAD