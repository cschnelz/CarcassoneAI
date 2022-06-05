import cProfile
from email import policy
import sys
import random
import time

from Agents import *
from Game import Game
from Render import Renderer
from Action import Action

def launch():
    players=[MCTS_Saver(), Greedy2()]
    carcassonne = Game(players,order=list(range(72)))

    for i in range(11):
        actions = carcassonne.getActions()
        carcassonne.applyAction(random.choice(actions))

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
    #carcassonne = Game(players=[MCTS_Saver(info='Heuristic'), MCTS_Saver(info='Rollout')])
    carcassonne = Game(players=[GreedyAgent(), Greedy2()])
    rend = Renderer()
    #carcassonne.render(rend)
    
    while(carcassonne.gameOver() is False):
        start_time = time.time()
        tile_num = carcassonne.state.currentTile[0].id
        #print(f'Current tile: {carcassonne.state.currentTile[0]}')
        actions = carcassonne.getActions()
        currPlayer = carcassonne.currentPlayer()
        response = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)

        end_time = time.time()
        print(f'turn: {carcassonne.state.turn} tile: {tile_num} {response} in {int(end_time-start_time)} seconds')
        carcassonne.applyAction(response)

        if carcassonne.state.turn %2 == 0:
            print()

        #carcassonne.render(rend)
        # input()
        
    print(f'score: {carcassonne.finalScore()}')
    print(f'meeples placed: {(carcassonne.state.players[0].meeplesPlaced,carcassonne.state.players[1].meeplesPlaced)}')
    

def launchX():
    players=[MCTS_Saver(info='Rollout'), MCTS_Saver(info='Heuristic')]
    rend = Renderer()
    carcassonne = Game(players,order=[1, 53, 31, 14,8, 26,62, 5,47, 0,38, 44,67, 59,50, 37,25])
    state = carcassonne.state

    carcassonne.applyAction(Action(1,0,state.currentTile[0],True,state.currentTile[0].featureAtEdge(1)))


    carcassonne.render(rend)
    actions = carcassonne.getActions()
    currPlayer = carcassonne.currentPlayer()
    response = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)
    print(response)
    carcassonne.applyAction(response)

    carcassonne.render(rend)
    input()





if __name__ == '__main__':
    launch2()


    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()
    # launch()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('cumtime')
    # stats.print_stats()