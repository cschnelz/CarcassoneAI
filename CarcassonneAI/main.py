import sys
import random

from Game import Game
from Action import *

if __name__ == '__main__':
    carcassonne = Game(order=[52,53,1,1,1,1,1,1,1,1,1,1,1,1])
    state = carcassonne.state
    tiles = state.tileList
        
    #carcassonne.applyAction(random.choice(validActions(state.board,state.currentTile)))
    #carcassonne.applyAction(random.choice(validActions(state.board,state.currentTile)))

    tile = rotate(tiles[53],1)
    carcassonne.applyAction(Action(0,-1,tile,True,tile.features[0]))
    #carcassonne.applyAction(Action(-1,-1,rotate(tiles[4],0),False,None))
   
    state.currentTile = tiles[54]
    carcassonne.render()
    carcassonne.applyAction(carcassonne.currentPlayer().agent.getResponse(carcassonne.getActions()))
    # tile = rotate(tiles[9],0)
    # carcassonne.applyAction(Action(-1,-2,tile,True,tile.grasses[1]))

    # carcassonne.applyAction(Action(1,-1,rotate(tiles[35],0),False,None))
    # carcassonne.applyAction(Action(1,-2,rotate(tiles[26],3),False,None))
    # carcassonne.render()

    # tile = rotate(tiles[54],2)
    #carcassonne.applyAction(Action(0,-2,tile,False,None))

        #carcassonne.applyAction(random.choice(actions))
        
    carcassonne.render()
    input()