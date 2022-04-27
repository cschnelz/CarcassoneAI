from turtle import back
from xmlrpc.client import Boolean
from Board import Board, shiftCoords, shiftCoordsGrass
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


def validActions(board: Board, currTileOrientations: List[Tile], meepleAvailable: Boolean) -> List[Action]:
    actions = set()

    for tile in currTileOrientations:
        for location in board.openLocations:
            if board.isValid(location[0], location[1], tile):
                # check if meeple is valid by inserting tile and running feature expansion      
                actions.add(Action(location[0],location[1], tile, False, None))
                if meepleAvailable:
                    for feat in tile.features:
                        bFMeepled = False # <--- check if the built feature this feature would connect to is already meepled
                        for edge in feat.edges:
                            neighborLoc = shiftCoords(location[0],location[1],edge)
                            oppEdge = (edge+2) % 4
                            bF = board.findTracked(board.nodeAt(neighborLoc[0],neighborLoc[1]),oppEdge,board.trackedFeatures)
                            if bF is not None and len(bF.meepled) > 0:
                                # the built feat that the current feat would connect to is already meepled :(
                                bFMeepled = True
                        if bFMeepled is False:
                            actions.add(Action(location[0],location[1],tile,True,feat))
                    
                    for field in tile.grasses:
                        fieldMeepled = False
                        for edge in field.edges:
                            neighborLoc = shiftCoordsGrass(location[0],location[1],edge)
                            if edge % 2 == 0:
                                oppEdge = (edge + 5) % 8
                            else:
                                oppEdge = (edge + 3) % 8
                            bF = board.findTracked(board.nodeAt(neighborLoc[0],neighborLoc[1]),oppEdge,board.trackedFields)
                            if bF is not None and len(bF.meepled) > 0:
                                fieldMeepled = True
                        if fieldMeepled is False:
                            actions.add(Action(location[0],location[1],tile,True,field))
                       
    actions = list(actions)
    actions.sort(key=lambda action: (action.x, action.y, action.tile.orientation, action.meeple))
    return actions  

## get valid locations for a single tile for a single location
def validActionsLocation(board:Board,location:Tuple[int],currTile:Tile,meepleAvailable:Boolean) -> List[Action]:
    actions = {Action(location[0],location[1],currTile,False,None)}
    if meepleAvailable:
        for feat in currTile.features:
            bFMeepled = False # <--- check if the built feature this feature would connect to is already meepled
            for edge in feat.edges:
                neighborLoc = shiftCoords(location[0],location[1],edge)
                oppEdge = (edge+2) % 4
                bF = board.findTracked(board.nodeAt(neighborLoc[0],neighborLoc[1]),oppEdge,board.trackedFeatures)
                if bF is not None and len(bF.meepled) > 0:
                    # the built feat that the current feat would connect to is already meepled :(
                    bFMeepled = True
            if bFMeepled is False:
                actions.add(Action(location[0],location[1],currTile,True,feat))
        
        for field in currTile.grasses:
            fieldMeepled = False
            for edge in field.edges:
                neighborLoc = shiftCoordsGrass(location[0],location[1],edge)
                if edge % 2 == 0:
                    oppEdge = (edge + 5) % 8
                else:
                    oppEdge = (edge + 3) % 8
                bF = board.findTracked(board.nodeAt(neighborLoc[0],neighborLoc[1]),oppEdge,board.trackedFields)
                if bF is not None and len(bF.meepled) > 0:
                    fieldMeepled = True
            if fieldMeepled is False:
                actions.add(Action(location[0],location[1],currTile,True,field))
    
    actions = list(actions)
    actions.sort(key=lambda action: (action.x, action.y, action.tile.orientation, action.meeple))
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