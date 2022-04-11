import cProfile
import sys
import random

from Game import Game
from Agents import *

def launch():
    players=[MCTS_Agent(), MCTS_Agent()]
    carcassonne = Game(players,order=[int(x) for x in sys.argv[1:len(sys.argv)]]) if len(sys.argv) > 1 else Game(players)
    #carcassonne.render()
    #input()


    carcassonne.applyAction(carcassonne.currentPlayer().agent.getResponse(carcassonne.getActions(),game=carcassonne,maxPlayer=carcassonne.currentPlayerId()))
    #carcassonne.applyAction(carcassonne.currentPlayer().agent.getResponse(carcassonne.getActions(),game=carcassonne,maxPlayer=carcassonne.currentPlayerId()))
        
  
        #carcassonne.render()
        #input(".")
        
        #carcassonne.applyAction(random.choice(actions))
    print(carcassonne.finalScore())
    #carcassonne.render()
    # input() 

if __name__ == '__main__':
    #launch()
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    launch()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()