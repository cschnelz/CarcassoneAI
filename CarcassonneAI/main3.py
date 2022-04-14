import cProfile
import sys
import random

from Game import Game
from Agents import *

def launch():
    players=[MCTS_Saver(), MCTS_Saver()]
    carcassonne = Game(players,order=list(range(0,72)))
    
    actions = carcassonne.getActions()
    currPlayer = carcassonne.currentPlayer()

    response = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)
    carcassonne.applyAction(response)

    carcassonne.render()
    #input()


def launch2():
    carcassonne = Game(players=[MCTS_Saver(), GreedyAgent()],order=list(range(0,72)))
    while(carcassonne.gameOver() is False):
        actions = carcassonne.getActions()
        currPlayer = carcassonne.currentPlayer()

        response = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)
        carcassonne.applyAction(response)

        #carcassonne.render()
        #input()
    print(carcassonne.finalScore())
    

if __name__ == '__main__':
    #launch()
    #launch()
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    launch()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()