import cProfile
import sys
import random

from Agents import *
from Game import Game

def launch():
    players=[MCTS_Saver(), GreedyAgent()]
    carcassonne = Game(players,order=list(range(72)))

    actions = carcassonne.getActions()
    currPlayer = carcassonne.currentPlayer()

    response = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)
    carcassonne.applyAction(response)

    # carcassonne.render()
    # input()


def launch2():
    carcassonne = Game(players=[MCTS_Saver(), GreedyAgent()])
    print(f'tile order: {carcassonne.state.order}')
    #carcassonne.render()
    while(carcassonne.gameOver() is False):
        #print(f'Current tile: {carcassonne.state.currentTile[0]}')
        actions = carcassonne.getActions()
        currPlayer = carcassonne.currentPlayer()
        response = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)

        carcassonne.applyAction(response)

        # carcassonne.render()
        # input()
        
    print(carcassonne.finalScore())
    

if __name__ == '__main__':
    launch()
    #launch()
    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()
    # launch()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('cumtime')
    # stats.print_stats()