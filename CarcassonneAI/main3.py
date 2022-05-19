import cProfile
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
    carcassonne = Game(players=[MCTS_Saver(), MCTS_Saver()])
    rend = Renderer()
    carcassonne.render(rend)

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

        carcassonne.render(rend)
        # input()
        
    print(f'score: {carcassonne.finalScore()}')
    print(f'meeples placed: {(carcassonne.state.players[0].meeplesPlaced,carcassonne.state.players[1].meeplesPlaced)}')
    

def launchX():
    players=[MCTS_Saver(), MCTS_Saver()]
    rend = Renderer()
    carcassonne = Game(players,order=[1, 53, 31, 14,8, 26,62, 5,47, 0,38, 44,67, 59,50, 37,25])
    state = carcassonne.state

    # carcassonne.applyAction(Action(0,-1,state.currentTile[0],True,state.currentTile[0].grassAtEdge(0)))
    # carcassonne.applyAction(Action(0,1,state.currentTile[3],False,None))
    # carcassonne.applyAction(Action(1,1,state.currentTile[0],True,state.currentTile[0].featureAtEdge(3)))
    # carcassonne.applyAction(Action(0,-2,state.currentTile[1],False,None))
    # carcassonne.applyAction(Action(2,1,state.currentTile[1],False,None))
    # carcassonne.applyAction(Action(2,0,state.currentTile[1],True,state.currentTile[1].featureAtEdge(1)))
    # carcassonne.applyAction(Action(1,2,state.currentTile[0],True,state.currentTile[0].featureAtEdge(0)))
    # carcassonne.applyAction(Action(-1,0,state.currentTile[3],True,state.currentTile[3].grassAtEdge(2)))
    # carcassonne.applyAction(Action(3,0,state.currentTile[0],True,state.currentTile[0].grassAtEdge(2)))
    # carcassonne.applyAction(Action(-1,1,state.currentTile[1],False,None))
    # carcassonne.applyAction(carcassonne.getActions()[0])

    carcassonne.applyAction(Action(1,0,state.currentTile[0],True,state.currentTile[0].grassAtEdge(4)))


    carcassonne.render(rend)
    actions = carcassonne.getActions()
    currPlayer = carcassonne.currentPlayer()
    response = currPlayer.agent.getResponse(actions,game=carcassonne,maxPlayer=currPlayer.id)
    print(response)
    carcassonne.applyAction(response)

    carcassonne.render(rend)
    input()





if __name__ == '__main__':
    #launch2()
    launchX()


    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()
    # launch()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('cumtime')
    # stats.print_stats()