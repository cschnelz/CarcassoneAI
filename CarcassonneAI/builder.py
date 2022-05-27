import cProfile
import sys
import random
import time

from Agents import *
from Board import builtFeature
from Game import Game
from Action import Action
from State import State
from Render import Renderer


def build(orderN):
    carcassonne = Game(players=[HumanAgent(), HumanAgent()], order=orderN)
    rend = Renderer()
    carcassonne.render(rend)
    repeat = True
    action_string = ""
    state = carcassonne.state

  

  

    carcassonne.render(rend)

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
        carcassonne.render(rend)
        repeat = input("continue?")

    print(action_string)

def reconstruct(orderN):
    carcassonne = Game(players=[HumanAgent(), HumanAgent()], order=orderN)
    rend = Renderer()
    state = carcassonne.state
    state.turn = 50

    carcassonne.applyAction(Action(0,-1,state.currentTile[0],False,None))
    carcassonne.applyAction(Action(0,1,state.currentTile[0],False,None))
    carcassonne.applyAction(Action(0,2,state.currentTile[2],False,None))






    carcassonne.render(rend)
    print(carcassonne.getScore())
    hueristic_evaluation(None, carcassonne, carcassonne.state, print_individual=True)
    input()
    

def hueristic_evaluation(xx:Saver_Node,game:Game,muteState:State,print_individual=False):
    from Board import Board, builtFeature
    from Feature import FeatType

    #muteState.applyAction(node.action, quiet=True)
    state = muteState
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
    featsRed = [feat for feat in featsRed if feat is not None]

    meepleCountRed = state.players[0].meepleCount
    redRoads = heuristic_roads(state, [feat for feat in featsRed if feat.featType == FeatType.ROAD], meepleCountRed)
    redCities = heuristic_city(state, [feat for feat in featsRed if feat.featType == FeatType.CITY], meepleCountRed)
    redChapel = heuristic_chapel(state, [feat for feat in featsRed if feat.featType == FeatType.CHAPEL], meepleCountRed)
    redField = heuristic_field(state, [feat for feat in featsRed if feat.featType == FeatType.GRASS], meepleCountRed)
    redMeeples = hueristic_meeples(meepleCountRed)
    baseRed += redRoads + redCities + redChapel + redField + redMeeples

    if print_individual:
        print(f'Red Scores: roads {redRoads} | cities {redCities} | chapels {redChapel} | fields {redField} | meeples {redMeeples} total {baseRed}')

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
    featsBlue = [feat for feat in featsBlue if feat is not None]

    meepleCountBlue = state.players[1].meepleCount
    blueRoads = heuristic_roads(state, [feat for feat in featsBlue if feat.featType == FeatType.ROAD], meepleCountBlue)
    blueCities = heuristic_city(state, [feat for feat in featsBlue if feat.featType == FeatType.CITY], meepleCountBlue)
    blueChapel = heuristic_chapel(state, [feat for feat in featsBlue if feat.featType == FeatType.CHAPEL], meepleCountBlue)
    blueField = heuristic_field(state, [feat for feat in featsBlue if feat.featType == FeatType.GRASS], meepleCountBlue)
    blueMeeples = hueristic_meeples(meepleCountBlue)
    baseBlue += blueRoads + blueCities + blueChapel + blueField + blueMeeples

    if print_individual:
        print(f'Blue Scores: roads {blueRoads} | cities {blueCities} | chapels {blueChapel} | fields {blueField} | meeples {blueMeeples} total {baseBlue}')


    return baseRed - baseBlue




TOTAL_TURNS = 72.0
ROAD_BIAS = 0.025
ROAD_CAPPED_BONUS = 1.25

CITY_BIAS = 0.075

TOTAL_TURNS = 72.0
ROAD_BIAS = 0.025
ROAD_CAPPED_BONUS = 1.25

CITY_BIAS = 0.075

def heuristic_roads(state:State, roads:list[builtFeature], meeples_left:int):
    total_road_score = 0.0
    for road in roads:
        base = road.score   # start with the road score
        bias = MCTS_Saver.ROAD_BIAS * ((MCTS_Saver.TOTAL_TURNS - state.turn) / 2.0) # add an amount representing future additions
        if len(road.holes) == 1:
            bias *= MCTS_Saver.ROAD_CAPPED_BONUS  # give a bonus to half-ended roads over no-ended roads
        
        road_score = base + bias
        total_road_score += road_score

    return total_road_score

def heuristic_city(state:State, cities:list[builtFeature], meeples_left:int):
    total_city_score = 0.0
    for city in cities:
        base = city.score / 2  # start with city score
        odds = MCTS_Saver.CITY_BIAS * (((MCTS_Saver.TOTAL_TURNS - state.turn) / 2.0) / (len(city.holes)*.5)) # add a bias for finishing city divided by edges left open
        
        city_score = min(base * odds, ((base + 1)*2)-.1)
        total_city_score += city_score
    
    return total_city_score

def heuristic_chapel(state:State, chapels:list[builtFeature], meeples_left:int):
    chapel_score = 0.0
    for chapel in chapels:
        chapel_neighbors = len(state.board.neighbors8(chapel.locs[0][0], chapel.locs[0][1]))
        chapel_score += min(9, ((MCTS_Saver.TOTAL_TURNS - state.turn) / 2) - (9 - chapel_neighbors))
    
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

    return max(0,field_score - (.15 * (TOTAL_TURNS - state.turn) / 2))


def hueristic_meeples(meeples_left:int):
    if meeples_left == 0:
        return 0
    elif meeples_left == 1:
        return 4
    elif meeples_left == 2:
        return 6
    else:
        return 4 + meeples_left

# 19, 43
# [56,10,8,32,28,30,2,21,11,40,58,49,29,59,24,55,37,69,41,23,67,22,71,42,25,47,15,9,27,63,6,48,1,39,45,68,60,51,38,26,33,5,35,34,64,46,72,17,50,4,3,31,65,52,36,16,54,62,20,12,18,66,14,57,61,53,7,70,13,44]
if __name__ == '__main__':
    o = [4,14,9,19]
    if len(sys.argv) > 1:
        build(o)
    else:
        reconstruct(o)