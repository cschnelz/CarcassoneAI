from platform import node
from Tile import Tile, featureAtEdgeStatic, grassAtEdgeStatic
from typing import List, Dict
from Feature import *
import sys

# Tracks the construction of the game board
def neighborCoordinates(x: int, y: int) -> List[tuple]:
    return [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]

def neighborCoordinates8(x: int, y:int) -> List[tuple]:
    eight = neighborCoordinates(x,y)
    eight.extend([(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)])
    return eight

def shiftCoords(x, y, direction):
    if direction == 0:
        return (x, y-1)
    if direction == 2:
        return (x, y+1)
    if direction == 1:
        return (x+1, y)
    return (x-1, y)

def shiftCoordsGrass(x, y, direction):
    direction = int(direction / 2)
    if direction == 0:
        return (x, y-1)
    if direction == 2:
        return (x, y+1)
    if direction == 1:
        return (x+1, y)
    return (x-1, y)

def cleanEdges(edges: List):
    cleanEdges = edges.copy()
    for i in range(4):
        if i*2 in cleanEdges and i*2+1 in cleanEdges:
            cleanEdges.remove(i*2+1)
    return cleanEdges

class Node:
    def __init__(self, x: int, y: int, tile: Tile):
        self.tile = tile
        self.id = tile.id
        self.x = x
        self.y = y

        ## 0 === North, 1 === east, 2 === south, 3 === west
        self.neighbors = [None] * 4
           
class combinedFeature:
    def __init__(self):
        self.completed = True
        self.featType = None
        self.score = 0
        self.features = []
        self.tileFeat = []
        self.meepled: List[Feature] = []
        self.tiles = []
        self.playersOn = []
        self.nodes: List[Node] = []
        self.nodeEdges = []
        self.meepleRecords: List[(int,int)] = []

    def __eq__(self, __o: object) -> bool:
        return set(self.features) == set(__o.features)


## might split this into a bF for fields if it gets too unwieldy
class builtFeature:
    def __init__(self, featType, tracked, coord, info, holes):
        self.featType = featType
        ## { node id : edge feature occupies }
        self.tracked = tracked
        self.locs = [coord]
        
        self.meepled = [] # list of colors on it
        self.coordsMeepled: List[tuple[int]] = [] # list of tiles meepled

        self.score = info if self.featType != FeatType.GRASS else 0
        self.adjacentCities: Dict[Node,int] = info if self.featType == FeatType.GRASS else {}

        ## track empty locations for the feature
        # update it when tiles are added, and if a tile closes all the holes the feat is completed
        self.holes = holes
        self.completed = False
        
class meepleInfo:
    def __init__(self, player: Player, feature: Feature):
        self.feature = feature.featType != FeatType.GRASS # false -> field
        self.edge = -1 if feature.featType == FeatType.CHAPEL else feature.edges[0]
        self.featureObject: Feature = feature
        self.color = player.color
        self.id = player.id

class Board:
    def __init__(self, startingTile: Tile):
        startingNode = Node(0, 0, startingTile)
        self.board = {(0, 0) : startingNode}
        self.openLocations = {(0,1), (1, 0), (0, -1), (-1, 0)}
        self.minX = self.minY = -1
        self.maxX = self.maxY = 1

        self.trackedFeatures: List[builtFeature] = [builtFeature(feat.featType, {startingNode.id: feat.edges},(0,0),feat.score(),feat.getHoles((0,0))) for feat in startingTile.features]
        self.trackedFields: List[builtFeature] = [builtFeature(FeatType.GRASS, {startingNode.id: grass.edges},(0,0),{self.nodeAt(0,0):grass.edges[0]},set()) for grass in startingTile.grasses]
        

        ## { (x, y) : meepleInfo }
        self.meepled: Dict[tuple, meepleInfo] = {}

    #def copy(self):

    def addTile(self, x:int, y: int, tile: Tile) -> Node:
        if not self.isValid(x, y, tile):
            sys.exit("invalid placement")

        node = Node(x, y, tile)
        neighbors = neighborCoordinates(x, y)
        
        # for all neighbor coordinates of new node
        for i in range(4):
            coord = neighbors[i]
            # if there is a prev node at that coordinate
            neighbor = self.board.get(coord)
            if neighbor is not None:
                # it is a neighbor of the new node
                node.neighbors[i] = neighbor
                # the new node is a neighbor of the prev node to the opposite cardinal
                neighbor.neighbors[(i+2)%4] = node
            # if there is no node there
            elif coord not in self.openLocations:
                # add the coords as a new open location for tiles
                self.openLocations.add(coord)

        self.board[(x, y)] = node
        self.openLocations.remove((x, y))
        self.expandBounds(neighbors)
        return node

    def findTracked(self, node: Node, edge: int, trackedList : List[builtFeature]) -> builtFeature:
        for built in trackedList:
            if node.id in built.tracked and edge in built.tracked[node.id]:
                return built
        return None
 
    def connectFeatures(self, node: Node, meepled: Feature, color: str):
        # find the built features that the new tile connects to and merge them
        for feat in node.tile.features:
            foundFeats: set[builtFeature] = set()
            for edge in feat.edges:
                if shiftCoords(node.x,node.y,edge) in self.board:
                    neighborNode = self.board[shiftCoords(node.x,node.y,edge)]
                    tracked = self.findTracked(neighborNode, feat.getOppositeEdge(edge), self.trackedFeatures)
                    if tracked is not None:
                        foundFeats.add(tracked)

            ## make a new bF that represents the current feat of the tile being added
            newFeat = builtFeature(feat.featType,{node.id : feat.edges},(node.x,node.y),feat.score(),feat.getHoles((node.x,node.y)))
            ## if the tile being played has been meepled on this feat, add color to list
            if meepled == feat:
                newFeat.meepled = [color]
                newFeat.coordsMeepled.append((node.x,node.y))

            ## for each nearby feature
            for feat in foundFeats:
                ## extend color list if needed
                if feat.meepled:
                    newFeat.meepled.extend(feat.meepled)
                    newFeat.coordsMeepled.extend(feat.coordsMeepled)
                ## merge the tracked dictionaries
                newFeat.tracked.update(feat.tracked)
                ## union holes
                newFeat.holes = newFeat.holes.union(feat.holes)
                ## extend locations
                newFeat.locs.extend(feat.locs)
                ## accrue score
                newFeat.score += feat.score
                ## remove old bF
                self.trackedFeatures.remove(feat)
            ## add new bF
            self.trackedFeatures.append(newFeat)
            self.checkCompleted(newFeat)
        
        # same operation but intending to do fields
        for grass in node.tile.grasses:
            foundFields: set[builtFeature] = set()
            for edge in grass.edges:
                if shiftCoordsGrass(node.x, node.y, edge) in self.board:
                    neighborNode = self.board[shiftCoordsGrass(node.x, node.y, edge)]
                    tracked = self.findTracked(neighborNode, grass.getOppositeEdge(edge), self.trackedFields)
                    if tracked is not None:
                        foundFields.add(tracked)

            newField = builtFeature(FeatType.GRASS,{node.id: grass.edges},(node.x,node.y),{node:grass.edges[0]},set())
            if meepled == grass:
                newField.meepled = [color]
                newField.coordsMeepled.append((node.x,node.y))

            for field in foundFields:
                if field.meepled:
                    newField.meepled.extend(field.meepled) 
                    newField.coordsMeepled.extend(field.coordsMeepled)
                newField.tracked.update(field.tracked)
                newField.holes = newField.holes.union(field.holes)
                newField.locs.extend(field.locs)
                newField.adjacentCities.update(field.adjacentCities)

                ## keep track of adjacent cities for fields maybe?
                self.trackedFields.remove(field)
            self.trackedFields.append(newField)
            #self.checkCompleted(newField) ## DONT TRY TO COMPLETE FIELDS OR COULD INTRODUCE BUGG WITH REMOVING FROM FIELDS

    ## Checks if an updated bF is now "complete" by removing filled holes
    def checkCompleted(self, bF: builtFeature):
        toRemove = set()
        for hole in bF.holes:
            if hole in bF.locs:
                toRemove.add(hole)
        bF.holes = bF.holes - toRemove
        bF.completed = len(bF.holes) == 0


    ## Given coordinates, an edge, and feature or grass, returns if that builtFeature is meeepled
    def featureMeepled(self, x:int, y:int, edge:int, featType: FeatType) -> bool:
        node = self.board.get((x,y))
        search = self.trackedFields if featType == FeatType.GRASS else self.trackedFeatures
        tracked = self.findTracked(node, edge, search)
        return tracked.meepled if tracked is not None else False


    # given a tile and a location, checks if it can be inserted there
    def isValid(self, x: int, y: int, tile: Tile) -> bool:
        # for this location
        # for all neighbor tiles of this location
            # can the tile link to that neighbor in that direction
        if (x, y) not in self.openLocations:
            return False
        neighbors = neighborCoordinates(x, y)

        # for all adjacent coords
        for i in range(4):
            coord = neighbors[i]
            # if there is a tile there
            if self.board.get(coord) is not None:
                # test if the new tile is valid in that direction
                if not tile.canConnectTo(self.board.get(coord).tile, i):
                    return False

        # if we get through all directions, the tile can fit
        return True

    def getNeighbor(self, x: int, y: int, direction: int) -> Tile:
        node = self.board.get((x, y))
        if node.neighbors[direction] is not None:
            return node.neighbors[direction].tile
        return None

    def tileAt(self, x: int, y: int) -> Tile:
        node = self.board.get((x,y))
        return node.tile if node is not None else None

    def nodeAt(self, x: int, y: int) -> Node:
        return self.board.get((x,y))

    # track the bounding coords of the game board
    def expandBounds(self, coords: List[tuple]):
        for coord in coords:
            self.minX = min(self.minX, coord[0])
            self.minY = min(self.minY, coord[1])
            self.maxX = max(self.maxX, coord[0])
            self.maxY = max(self.maxY, coord[1])

    ## orthogonal and diagonal neighbors 
    def neighbors8(self, x:int, y:int) -> list[Node]:
       return [self.board.get(coord) for coord in neighborCoordinates8(x,y) if self.board.get(coord) is not None]
    
     
    def buildFeature(self, x, y, featEdge: int, featType: FeatType) -> combinedFeature:
        combined = combinedFeature()
        tile = self.tileAt(x,y)
        if featType is None:
            return combined

        if featType is FeatType.GRASS:
            if tile.grasses is not []:
                combined.featType = FeatType.GRASS
                self.finishedRecursive(x, y, featEdge, combined, grassAtEdgeStatic, shiftCoordsGrass, False)
        else:
            if tile.featureAtEdge(featEdge) is not None:
                combined.featType = tile.featureAtEdge(featEdge).featType
                self.finishedRecursive(x, y, featEdge, combined, featureAtEdgeStatic, shiftCoords, True)

        return combined

     
    def finishedRecursive(self, x: int, y: int, inEdge: int, combined: combinedFeature, featureFunc, shiftFunc, feature):
        tile = self.tileAt(x,y)
        inFeature: Feature = featureFunc(tile, inEdge)
        
        # add info about meeples on this feature
         
        if (x, y) in self.meepled.keys() and (x,y) not in combined.meepleRecords:
            meepled = self.meepled.get((x,y))
            if feature:
                if meepled.feature:
                    if inEdge in self.meepled.get((x,y)).featureObject.edges:
                        combined.meepled.append(inFeature)
                        combined.playersOn.append(self.meepled.get((x,y)).color)
                        combined.meepleRecords.append((x,y))
            else:
                if not meepled.feature:
                    if inEdge in self.meepled.get((x,y)).featureObject.edges:
                        combined.meepled.append(inFeature)
                        combined.playersOn.append(self.meepled.get((x,y)).color)
                        combined.meepleRecords.append((x,y))
        
        # check that the tile hasn't been scored yet, and add the score for the feature
        if tile.id not in combined.tiles:
            combined.tiles.append(tile.id)
            combined.nodes.append(self.board.get((x,y)))
            combined.nodeEdges.append((self.board.get((x,y)),inEdge))
            combined.tileFeat.append((tile,inFeature))
            combined.score += inFeature.score()

        # recursively search across all other edges this feature is on
        for edge in inFeature.edges:
            if (tile.id, edge) not in combined.features:
                # if there's more edges to this feature, add them
                combined.features.append((tile.id, edge))
  
                # shift to the next tile and recurse
                nextEdge = inFeature.getOppositeEdge(edge)
                nextX, nextY = shiftFunc(x, y, edge)
                if self.tileAt(nextX, nextY) is not None:
                    self.finishedRecursive(nextX, nextY, nextEdge, combined, featureFunc, shiftFunc, feature)
                else:
                    combined.completed = False
