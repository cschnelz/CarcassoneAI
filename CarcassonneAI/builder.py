import cProfile
import sys
import random
import time

from Agents import *
from Board import builtFeature
from Game import Game
from Action import Action
from State import State


def build(orderN):
    carcassonne = Game(players=[HumanAgent(), HumanAgent()], order=orderN)
    carcassonne.render()
    repeat = True
    action_string = ""
    state = carcassonne.state

    carcassonne.render()


    while(repeat):
        actions = carcassonne.getActions()
        currPlayer = carcassonne.currentPlayer()
        response:Action = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)
        
        if response.meeple:
            if response.feature.featType == FeatType.CHAPEL:
                action_string += f'carcassonne.applyAction(Action({response.x},{response.y},state.currentTile[{response.tile.orientation}],True,state.currentTile[{response.tile.orientation}].features[0]))\n'  
            elif response.feature.featType == FeatType.GRASS: 
                action_string += f'carcassonne.applyAction(Action({response.x},{response.y},state.currentTile[{response.tile.orientation}],True,state.currentTile[{response.tile.orientation}].grassAtEdge({response.feature.edges[0]})))\n'            
            else:
                action_string += f'carcassonne.applyAction(Action({response.x},{response.y},state.currentTile[{response.tile.orientation}],True,state.currentTile[{response.tile.orientation}].featureAtEdge({response.feature.edges[0]})))\n'
            
        else:
            action_string += f'carcassonne.applyAction(Action({response.x},{response.y},state.currentTile[{response.tile.orientation}],False,None))\n'
        carcassonne.applyAction(response)
        carcassonne.render()
        repeat = input("continue?")

    print(action_string)

def reconstruct(orderN):
    carcassonne = Game(players=[HumanAgent(), HumanAgent()], order=orderN)
    state = carcassonne.state

    # carcassonne.applyAction(Action(0,-1,state.currentTile[0],True,state.currentTile[0].grassAtEdge(0)))
    # carcassonne.applyAction(Action(-1,-1,state.currentTile[1],False,None))
    # carcassonne.applyAction(Action(1,0,state.currentTile[3],True,state.currentTile[3].grassAtEdge(0)))
    # carcassonne.applyAction(Action(0,-2,state.currentTile[2],False,None))
    # carcassonne.applyAction(Action(0,-3,state.currentTile[1],False,None))
    # carcassonne.applyAction(Action(0,-4,state.currentTile[2],False,None))
    # carcassonne.applyAction(Action(1,-4,state.currentTile[1],False,None))
    # carcassonne.applyAction(Action(-2,-1,state.currentTile[1],False,None))
    # carcassonne.applyAction(Action(-2,-2,state.currentTile[0],False,None))
    # carcassonne.applyAction(Action(1,-1,state.currentTile[3],False,None))

    carcassonne.applyAction(Action(-1,0,state.currentTile[2],False,None))
    carcassonne.applyAction(Action(-2,0,state.currentTile[0],False,None))
    carcassonne.applyAction(Action(0,-1,state.currentTile[1],True,state.currentTile[1].featureAtEdge(1)))
    carcassonne.applyAction(Action(1,0,state.currentTile[2],True,state.currentTile[2].featureAtEdge(0)))
    carcassonne.applyAction(Action(-3,0,state.currentTile[1],False,None))
    carcassonne.applyAction(Action(-3,-1,state.currentTile[2],False,None))
    carcassonne.applyAction(Action(-3,1,state.currentTile[2],False,None))
    carcassonne.applyAction(Action(-4,1,state.currentTile[0],False,None))
    carcassonne.applyAction(Action(2,0,state.currentTile[0],True,state.currentTile[0].featureAtEdge(0)))
    carcassonne.applyAction(Action(-4,0,state.currentTile[1],False,None))
    carcassonne.applyAction(Action(-4,-1,state.currentTile[3],False,None))
    carcassonne.applyAction(Action(-3,-2,state.currentTile[2],False,None))
    carcassonne.applyAction(Action(-2,-2,state.currentTile[0],False,None))
    carcassonne.applyAction(Action(-2,1,state.currentTile[2],False,None))
    carcassonne.applyAction(Action(-1,1,state.currentTile[0],False,None))
    carcassonne.applyAction(Action(2,-1,state.currentTile[3],False,None))
    carcassonne.applyAction(Action(-1,2,state.currentTile[0],False,None))
    carcassonne.applyAction(Action(-4,-2,state.currentTile[1],False,None))
    carcassonne.applyAction(Action(-4,2,state.currentTile[0],False,None))
    carcassonne.applyAction(Action(1,-1,state.currentTile[2],False,None))



    carcassonne.render()

    mutable = carcassonne.startSim()
    for i in range(20):
        mutable.applyAction(random.choice(mutable.currentActions))
        mutable.dispatchTile()
    
    carcassonne.refresh(mutable)
    carcassonne.compareStates(carcassonne.state, mutable)

    print(carcassonne.getScore())
    print(carcassonne.evaluate())

    #hueristic_evaluation(state)
    input()
    
def hueristic_evaluation(state:State):
    from Feature import FeatType
    board = state.board

    ## RED
    baseRed = state.players[0].score
    meeplesRed = [(loc,info) for loc,info in board.meepled.items() if info.color == 'red']
    featsRed: list[builtFeature] = []
    for loc, info in meeplesRed:
        node = board.nodeAt(loc[0],loc[1])
        if info.featureObject.featType == FeatType.CHAPEL:
            featsRed.append(builtFeature(FeatType.CHAPEL,None,loc,None,None))
        elif info.feature:
            featsRed.append(board.findTracked(node,info.edge,board.trackedFeatures))
        else:
            featsRed.append(board.findTracked(node,info.edge,board.trackedFields))

    meepleCountRed = state.players[0].meepleCount
    baseRed += heuristic_roads(state, [feat for feat in featsRed if feat.featType == FeatType.ROAD], meepleCountRed)
    baseRed += heuristic_city(state, [feat for feat in featsRed if feat.featType == FeatType.CITY], meepleCountRed)
    baseRed += heuristic_chapel(state, [feat for feat in featsRed if feat.featType == FeatType.CHAPEL], meepleCountRed)
    baseRed += heuristic_field(state, [feat for feat in featsRed if feat.featType == FeatType.GRASS], meepleCountRed)

    ## BLUE
    baseBlue = state.players[1].score
    meeplesBlue = [(loc,info) for loc,info in board.meepled.items() if info.color == 'blue']
    featsBlue: list[builtFeature] = []
    for loc, info in meeplesBlue:
        node = board.nodeAt(loc[0],loc[1])
        if info.featureObject.featType == FeatType.CHAPEL:
            featsBlue.append(builtFeature(FeatType.CHAPEL,None,loc,None,None))
        elif info.feature:
            featsBlue.append(board.findTracked(node,info.edge,board.trackedFeatures))
        else:
            featsBlue.append(board.findTracked(node,info.edge,board.trackedFields))

    meepleCountBlue = state.players[1].meepleCount
    baseBlue += heuristic_roads(state, [feat for feat in featsBlue if feat.featType == FeatType.ROAD], meepleCountBlue)
    baseBlue += heuristic_city(state, [feat for feat in featsBlue if feat.featType == FeatType.CITY], meepleCountBlue)
    baseBlue += heuristic_chapel(state, [feat for feat in featsBlue if feat.featType == FeatType.CHAPEL], meepleCountBlue)
    baseBlue += heuristic_field(state, [feat for feat in featsBlue if feat.featType == FeatType.GRASS], meepleCountBlue)

    print()

TOTAL_TURNS = 72.0
ROAD_BIAS = 0.025
ROAD_CAPPED_BONUS = 1.25

CITY_BIAS = 0.075

def heuristic_roads(state:State, roads:list[builtFeature], meeples_left:int):
    total_road_score = 0.0
    for road in roads:
        base = road.score   # start with the road score
        bias = ROAD_BIAS * ((TOTAL_TURNS - state.turn) / 2.0) # add an amount representing future additions
        if len(road.holes) == 1:
            bias *= ROAD_CAPPED_BONUS  # give a bonus to half-ended roads over no-ended roads
        
        road_score = base + bias
        total_road_score += road_score

    return total_road_score

def heuristic_city(state:State, cities:list[builtFeature], meeples_left:int):
    total_city_score = 0.0
    for city in cities:
        base = city.score / 2  # start with city score
        odds = CITY_BIAS * (((TOTAL_TURNS - state.turn) / 2.0) / len(city.holes)) # add a bias for finishing city divided by edges left open
        
        city_score = base * odds
        total_city_score += city_score
    
    return total_city_score

def heuristic_chapel(state:State, chapels:list[builtFeature], meeples_left:int):
    chapel_score = 0.0
    for chapel in chapels:
        chapel_neighbors = len(state.board.neighbors8(chapel.locs[0]))
        chapel_score += min(9, (9 - chapel_neighbors) - ((TOTAL_TURNS - state.turn) / 2))
    
    return chapel_score

def heuristic_field(state:State, fields:list[builtFeature], meeples_left:int):
    field_score = 0.0
    for field in fields:
        adjacent_cities = set()
        for node,edge in field.adjacentCities.items():

            adjacent = list(set(node.tile.adjacentCity(node.tile.grassAtEdge(edge))))
            
            for cityEdge in adjacent:
                builtCity = state.board.findTracked(node,cityEdge,state.board.trackedFeatures)
                if builtCity is not None: #and builtCity not in citiesChecked:
                    adjacent_cities.add(builtCity)

        for city in adjacent_cities:
            field_score += (2.5 - len(city.holes))

    return field_score

# 19, 43
# [56,10,8,32,28,30,2,21,11,40,58,49,29,59,24,55,37,69,41,23,67,22,71,42,25,47,15,9,27,63,6,48,1,39,45,68,60,51,38,26,33,5,35,34,64,46,72,17,50,4,3,31,65,52,36,16,54,62,20,12,18,66,14,57,61,53,7,70,13,44]
if __name__ == '__main__':
    #build([18,55,9,7,31,27,29,1,20,10,39,57,48,28,58,23,54, 36,68, 40,22, 66,21, 70,41, 24,46, 14,8, 26,62, 5,47, 0,38, 44,67, 59,50, 37,25, 32,4, 34,33, 63,45, 71,16, 49,3, 2,30, 64,51, 35,15, 53,61, 19,11, 17,65, 13,56,  60,52, 6,69, 12,43])
    reconstruct([18,55,9,7,31,27,29,1,20,10,39,57,48,28,58,23,54, 36,68, 40,22, 66,21, 70,41, 24,46, 14,8, 26,62, 5,47, 0,38, 44,67, 59,50, 37,25, 32,4, 34,33, 63,45, 71,16, 49,3, 2,30, 64,51, 35,15, 53,61, 19,11, 17,65, 13,56,  60,52, 6,69, 12,43])