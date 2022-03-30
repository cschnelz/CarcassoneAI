from turtle import back
from xmlrpc.client import Boolean
from Board import Board
from Tile import Tile, rotate
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

        self.forwardBoard: Board = None

    def __str__(self):
        string = f"Location: [{self.x}, {self.y}] "
        string += f"Orientation: {self.tile.orientation} "
        if self.meeple:
            string+= f"Meeple: {self.feature}"
        return string

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __o: object) -> bool:
        if (self.feature is None) != (__o.feature is None):
            return False

        if self.feature is not None:    
            return self.tile == __o.tile and \
            self.x == __o.x and self.y == __o.y and \
            self.meeple == __o.meeple and \
            self.feature.featType == __o.feature.featType and \
            self.feature.edges == __o.feature.edges

        return self.tile == __o.tile and \
            self.x == __o.x and self.y == __o.y and \
            self.meeple == __o.meeple
 
def validActions(board: Board, currTile: Tile, meepleAvailable: Boolean) -> List[Action]:
    actions = []
    orientations = [rotate(currTile,i) for i in range(4)]
    backupBoard = copy.deepcopy(board)

    for tile in orientations:
        for location in backupBoard.openLocations:
            if board.isValid(location[0], location[1], tile):
                # check if meeple is valid by inserting tile and running feature expansion      
                actions.append(Action(location[0],location[1], tile, False, None))
                if meepleAvailable:
                    actions.extend(validMeeples(board, tile, location))
                # revert board state for next run
                board.board = backupBoard.board.copy()
                board.openLocations = backupBoard.openLocations.copy()
                board.trackedFeatures = backupBoard.trackedFeatures.copy()
                board.trackedFields = backupBoard.trackedFields.copy()
                board.meepled = backupBoard.meepled.copy()
    #tuples.sort(key=lambda x: (x[0], x[1]))
    actions.sort(key=lambda action: (action.x, action.y))
    return actions
        
def validMeeples(board: Board, tile: Tile, location: Tuple[int]) -> List[Action]:
    # for a specific tile orientation at a specific location, how could one put meeples on it
    #forwardBoard = copy.deepcopy(board)
    node = board.addTile(location[0], location[1], tile)
    board.connectFeatures(node,False,None)

    actions = []
    if tile.chapel:
        openFeatures = [tile.features[0]]
    else:
        openFeatures = [feat for feat in tile.features if 
            not(board.featureMeepled(location[0], location[1], feat.edges[0], tile.features[0].featType))]

    openFeatures.extend([grass for grass in tile.grasses if 
        not (board.featureMeepled(location[0],location[1],grass.edges[0],FeatType.GRASS))])

    actions.extend([Action(location[0], location[1], tile, True, feat) for feat in openFeatures])
    return actions