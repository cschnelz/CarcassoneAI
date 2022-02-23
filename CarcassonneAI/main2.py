import sys
import random

from Game import Game

if __name__ == '__main__':
    carcassonne = Game()
    while carcassonne.gameOver() is False:
        carcassonne.render()
        actions = carcassonne.getActions()

        #action = carcassonne.currentPlayer().agent.getResponse(actions)
        carcassonne.applyAction(random.choice(actions))
        
        carcassonne.render()
    input()