import cProfile
import sys
import random
import time

from Agents import *
from Game import Game
from Action import Action

def launch():
    players=[RandomAgent(), GreedyDeterminized()]
    carcassonne = Game(players,order=list(range(72)))

    for i in range(21):
        actions = carcassonne.getActions()
        carcassonne.applyAction(actions[0])

    # carcassonne.render()
    # input()
    carcassonne.render()
    actions = carcassonne.getActions()
    currPlayer = carcassonne.currentPlayer()
    response = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)
    carcassonne.applyAction(response)

    #carcassonne.render()
    # input()


def launch2():
    carcassonne = Game(players=[RandomAgent(), GreedyDeterminized()])
    carcassonne.render()

    # carcassonne.state.turn = 68
    # carcassonne.state.order = carcassonne.state.order[66:70]
    # carcassonne.state.players[1].meepleCount = 0
    
    while(carcassonne.gameOver() is False):
        start_time = time.time()
        tile_num = carcassonne.state.currentTile[0].id
        #print(f'Current tile: {carcassonne.state.currentTile[0]}')
        actions = carcassonne.getActions()
        currPlayer = carcassonne.currentPlayer()
        response = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)

        end_time = time.time()
        print(f'tile: {tile_num} {response} in {int(end_time-start_time)} seconds')
        carcassonne.applyAction(response)

        if carcassonne.state.turn %2 == 0:
            print()

        carcassonne.render()
        # input()
        
    print(f'score: {carcassonne.finalScore()}')
    print(f'meeples placed: {(carcassonne.state.players[0].meeplesPlaced,carcassonne.state.players[1].meeplesPlaced)}')
    

def launchX():
    players=[RandomAgent(), GreedyDeterminized()]
    carcassonne = Game(players,order=list(range(72)))
    state = carcassonne.state

    for i in range(60):
        while carcassonne.gameOver() is False:
            carcassonne.applyAction(carcassonne.getActions()[0])
        carcassonne = Game(players,order=list(range(72)))




if __name__ == '__main__':
    #launch()
    #launch2()
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    launch()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()