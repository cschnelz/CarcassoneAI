## Static functions for management and calculations

from math import comb
from random import random
from Tile import Tile, featureAtEdgeStatic, grassAtEdgeStatic, rotate
from Board import Board, neighborCoordinates8
from typing import List
from Feature import *
from Render import *
from Import import importTiles
from Player import Player

# List of player classes that hold score, meeple counts, etc
players = [Player(0), Player(1)]
current_player = 0

# Load the tiles from the TileList json and initialize the list of Tile objects
tileList = importTiles('TileSetSepRoads.json')
playedTiles = []

# get a random tile from the tile list and remove it
def dispatchTile() -> Tile:
    dispatchId = int(random() * len(tileList))
    tile = tileList[dispatchId]
    del tileList[dispatchId]
    return tile

def dispatchForced(int) -> Tile:
    return tileList[int]

# set up board and players
def initialize(forcedOrder: List):
    if len(forcedOrder) > 0:
        startingTile = dispatchForced(forcedOrder.pop(0))
    else:
        startingTile = dispatchTile()

    # initialize board with a first tile
    playedTiles.append(startingTile)
    board = Board(startingTile)
    #render2(board)
    # self.players
        # create player objects 

    # begin game loop
    runGame(board, forcedOrder)

# given a tile, report locations and orientations it can be placed
def printValidLocations(board: Board, tile: Tile):
    orientations = getOrientations(tile)
    openLocations = board.openLocations

    for i in range(4):
        validLocations = [x for x in openLocations if board.isValid(x[0], x[1], orientations[i])]
        print(f"Open coordinates for orientation {i}: " + str(validLocations))

def printValidLocationsSingle(board: Board, currTile: Tile):
    validLocations = [x for x in board.openLocations if board.isValid(x[0], x[1], currTile)]
    print(f"Open coordinates for current Tile: " + str(validLocations))


def getOrientations(tile: Tile) -> List[Tile]:
    return [rotate(tile, i) for i in range(4)] 

## make a play decision
def playTile(board: Board, currTile: Tile):
    x = 0
    y = 0

    while (True):
        print('\n')
        render3(board, currTile, players)
        try:
            printValidLocationsSingle(board, currTile)
            res = input("input r to rotate, coordinates x y to insert, or q to quit: ").split()
            if res[0] == 'q':
                sys.exit("Quitting")

            if res[0] == 'r':
                currTile = rotate(currTile, 1)
                continue

            x = int(res[0])
            y = int(res[1])
            if board.isValid(x, y, currTile):
                board.addTile(x, y, currTile)
                break
            print("Invalid insertion, please input again")
        except ValueError:
            print("Improper input, please try again")

    return x, y

# holds information about a connected feature - used for tracking meeple placement, scoring, completion, etc
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

    def __eq__(self, __o: object) -> bool:
        return set(self.features) == set(__o.features)

# After a tile is inserted into the board
def checkCompletedFeatures(x, y, board: Board) -> List[combinedFeature]:
    completed = []
    for i in range(4):
        tile = board.tileAt(x,y)
        combined = buildFeature(x,y,i,board,tile.featureAtEdge(i))
        if combined.completed and combined.featType is not None:
            # prevents duping of looped features
            if combined not in completed:
                completed.append(combined)

    for node in board.neighbors8(x,y):
        if node.tile.chapel and node.tile.occupied.featType == FeatType.CHAPEL:
            neigh = board.neighbors8(node.x, node.y)
            if len(board.neighbors8(node.x,node.y)) == 8:
                combined = combinedFeature()
                combined.score = 9
                combined.playersOn.append(node.tile.features[0].occupiedBy.color)
                combined.meepled.append(node.tile.features[0]) 
                completed.append(combined)
        
    return completed

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

# check if a list of features is finished
def buildFeature(x, y, featEdge: int, board: Board, featType: FeatType) -> combinedFeature:
    combined = combinedFeature()
    tile = board.tileAt(x,y)
    if featType is None:
        return combined

    if featType is FeatType.GRASS:
        if tile.grasses is not []:
            combined.featType = FeatType.GRASS
            finishedRecursive(x, y, featEdge, board, combined, grassAtEdgeStatic, shiftCoordsGrass)
    else:
        if tile.featureAtEdge(featEdge) is not None:
            combined.featType = tile.featureAtEdge(featEdge).featType
            finishedRecursive(x, y, featEdge, board, combined, featureAtEdgeStatic, shiftCoords)

    return combined

def finishedRecursive(x: int, y: int, inEdge: int, board: Board, combined: combinedFeature, featureFunc, shiftFunc):
    tile = board.tileAt(x,y)
    inFeature: Feature = featureFunc(tile, inEdge)
    
    # add info about meeples on this feature    
    if inFeature.occupiedBy is not None:
        if inFeature not in combined.meepled:
            combined.meepled.append(inFeature)
            combined.playersOn.append(inFeature.occupiedBy.color)
    
    # check that the tile hasn't been scored yet, and add the score for the feature
    if tile.id not in combined.tiles:
        combined.tiles.append(tile.id)
        combined.score += inFeature.score()

    # recursively search across all other edges this feature is on
    for edge in inFeature.edges:
        if (tile.id, edge) not in combined.features:
            # if there's more edges to this feature, add them
            combined.features.append((tile.id, edge))
            combined.tileFeat.append((tile,inFeature))

            # shift to the next tile and recurse
            nextEdge = inFeature.getOppositeEdge(edge)
            nextX, nextY = shiftFunc(x, y, edge)
            if board.tileAt(nextX, nextY) is not None:
                finishedRecursive(nextX, nextY, nextEdge, board, combined, featureFunc, shiftFunc)
            else:
                combined.completed = False

def adjacentCities(completed: combinedFeature):
    cities = set()
    for tf in completed.tileFeat:
        tileCities = tf[0].adjacentCity(tf[1])
        cities = cities.union(tileCities)
    return cities

def placeMeeple(x: int, y: int, board: Board):
    # if player has meeples and there are places to put meeples, ask where theyd like to place meeple
    
    # get list of open features
    tile = board.tileAt(x, y)

    if tile.features[0].featType is not FeatType.CHAPEL:
        openFeatures = [feat for feat in tile.features if not(buildFeature(x, y, feat.edges[0], board,tile.features[0].featType).meepled)]
    else:
        openFeatures = [tile.features[0]]
    
    openFeatures.extend([grass for grass in tile.grasses if not (buildFeature(x,y,grass.edges[0],board,FeatType.GRASS).meepled)])

    meeps = players[current_player].meepleCount
    if len(openFeatures) > 0 and meeps > 0:
        print("\nFree features: ")
        option = 0
        for feature in openFeatures:
            print(f"Option: {option} - Feature: {feature.featType.name} on edges: {feature.edges}")
            option += 1

        while(True):
            feat = input(f"Place Meeple ({meeps} remaining)? input feat number or n for no: ")
            try:
                if feat != 'n':
                    # denote that the tile played and the feature selected is occupied
                    if int(feat) > len(openFeatures) - 1:
                        print("out of range")
                        continue
                    tile.occupied = openFeatures[int(feat)]
                    tile.occupied.occupiedBy = players[current_player]
                    players[current_player].meepleCount -= 1
                    break
                break
            except ValueError:
                print("improper input")
                continue
    else:
        if meeps == 0:
            print("Sorry, out of meeples!")
        else:
            print("No available features for placement")

def calculateScore(c: combinedFeature):
    redCount = c.playersOn.count('red')
    blueCount = c.playersOn.count('blue')

    if redCount == blueCount:
        players[0].score += c.score
        players[1].score += c.score
        print(f"Score! Both players earned {c.score} points!")
    elif redCount > blueCount:
        players[0].score += c.score
        print(f"Score! Red player earned {c.score} points!")
    else:
        players[1].score += c.score
        print(f"Score! Blue player earned {c.score} points!")
    
    print(f"Current score: Red {players[0].score} - Blue {players[1].score}")
    players[0].meepleCount += redCount
    players[1].meepleCount += blueCount



def runGame(board: Board, forcedOrder: List):
    # run the game until we have used all tiles
    while len(tileList) > 0:
        if len(forcedOrder) > 0:
            currTile = dispatchForced(forcedOrder.pop(0))
        else:
            currTile = dispatchTile()

        global current_player
        print(f"\nCurrent player: {'red' if current_player == 0 else 'blue'}")

        # get placement location, meeple placement, and then check for completed features and update score
        x, y = playTile(board, currTile)
        playedTiles.append(currTile)
        placeMeeple(x, y, board)
        completed = checkCompletedFeatures(x, y, board)

        for c in completed:
            for feat in c.meepled:
                feat.occupiedBy = None
            if len(c.playersOn) > 0:
                calculateScore(c)
                
        
        current_player = (current_player + 1) % 2
        ## board.test