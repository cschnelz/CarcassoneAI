from Board import Board
from Tile import Tile, rotate
from Manager import buildFeature
from Feature import Feature, FeatType

import copy
from typing import List, Tuple

class Action:
    def __init__(self, x, y, tile, meeple, feature):
        self.tile: Tile = tile
        self.x: int = x
        self.y: int = y
        self.meeple: bool = meeple
        self.feature: Feature = feature

    def __str__(self):
        string = f"Location: [{self.x}, {self.y}] "
        string += f"Orientation: {self.tile.orientation} "
        if self.meeple:
            string+= f"Meeple: {self.feature}"
        return string

def validActions(board: Board, currTile: Tile) -> List[Action]:
    actions = []
    orientations = [rotate(currTile,i) for i in range(4)]

    for tile in orientations:
        for location in board.openLocations:
            if board.isValid(location[0], location[1], tile):
                # action = Action()
                # action.x = location[0]
                # action.y = location[1]
                actions.extend(validMeeples(board, tile, location))
    return actions
        
def validMeeples(board: Board, tile: Tile, location: Tuple[int]) -> List[Action]:
    # for a specific tile orientation at a specific location, how could one put meeples on it
    forwardBoard = copy.deepcopy(board)
    forwardBoard.addTile(location[0], location[1], tile)

    actions = [Action(location[0],location[1], tile, False, None)]
    if tile.chapel:
        openFeatures = [tile.features[0]]
    else:
        openFeatures = [feat for feat in tile.features if 
            not(buildFeature(location[0], location[1], feat.edges[0], forwardBoard, tile.features[0].featType).meepled)]

    openFeatures.extend([grass for grass in tile.grasses if 
        not (buildFeature(location[0],location[1],grass.edges[0],forwardBoard,FeatType.GRASS).meepled)])

    actions.extend([Action(location[0], location[1], tile, True, feat) for feat in openFeatures])
    return actions