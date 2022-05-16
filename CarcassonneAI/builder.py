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
    print(carcassonne.getScore())
    print(carcassonne.evaluate())

    #hueristic_evaluation(state)
    input()
    

# 19, 43
# [56,10,8,32,28,30,2,21,11,40,58,49,29,59,24,55,37,69,41,23,67,22,71,42,25,47,15,9,27,63,6,48,1,39,45,68,60,51,38,26,33,5,35,34,64,46,72,17,50,4,3,31,65,52,36,16,54,62,20,12,18,66,14,57,61,53,7,70,13,44]
if __name__ == '__main__':
    build([0,1,2,3,4,5,6,7,8])
    #reconstruct([18,55,9,7,31,27,29,1,20,10,39,57,48,28,58,23,54, 36,68, 40,22, 66,21, 70,41, 24,46, 14,8, 26,62, 5,47, 0,38, 44,67, 59,50, 37,25, 32,4, 34,33, 63,45, 71,16, 49,3, 2,30, 64,51, 35,15, 53,61, 19,11, 17,65, 13,56,  60,52, 6,69, 12,43])