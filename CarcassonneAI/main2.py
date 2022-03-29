import cProfile
import sys
import random

from Game import Game
from Agents import *

def launch():
    players=[RandomAgent(), RandomAgent()]
    carcassonne = Game(players,order=[int(x) for x in sys.argv[1:len(sys.argv)]]) if len(sys.argv) > 1 else Game(players)
    carcassonne.render()
    #input()
    while carcassonne.gameOver() is False:
        actions = carcassonne.getActions()

        if carcassonne.currentPlayerId() == 0:
            carcassonne.applyAction(carcassonne.currentPlayer().agent.getResponse(actions,game=carcassonne,maxPlayer=0))
            
        else:
            carcassonne.applyAction(carcassonne.currentPlayer().agent.getResponse(actions,game=carcassonne,maxPlayer=1))
        #carcassonne.render()
        #input(".")
        
        #carcassonne.applyAction(random.choice(actions))
    print(carcassonne.finalScore())
    # carcassonne.render()
    # input() 

if __name__ == '__main__':
    #launch()
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    launch()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()