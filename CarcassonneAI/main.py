import sys
import random
from Agents import GreedyAgent, MCTS_Agent, RandomAgent

from Game import Game
from Action import *

def launch():
    for i in range(100):
        carcassonne = Game([RandomAgent(), RandomAgent()],order=[52,53,10,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        state = carcassonne.state
        tiles = state.tileList
            
        while(carcassonne.gameOver() is False):
            carcassonne.applyAction(carcassonne.currentPlayer().agent.getResponse(carcassonne.getActions(),game=carcassonne,maxPlayer=carcassonne.currentPlayerId()))


    # while carcassonne.gameOver() is False:
    # carcassonne.applyAction(carcassonne.currentPlayer().agent.getResponse(carcassonne.getActions(), carcassonne, carcassonne.currentPlayerId()))
    # carcassonne.applyAction(carcassonne.currentPlayer().agent.getResponse(carcassonne.getActions(), carcassonne, carcassonne.currentPlayerId()))

    # carcassonne.applyAction(Action(1,-1,rotate(tiles[35],0),False,None))
    # carcassonne.applyAction(Action(1,-2,rotate(tiles[26],3),False,None))
    # carcassonne.render()

    # tile = rotate(tiles[54],2)
    #carcassonne.applyAction(Action(0,-2,tile,False,None))

        #carcassonne.applyAction(random.choice(actions))
        
        
    print(carcassonne.evaluate())
    # carcassonne.render()
    # input()

if __name__ == '__main__':
    launch()
    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()
    # launch()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('tottime')
    # stats.print_stats()