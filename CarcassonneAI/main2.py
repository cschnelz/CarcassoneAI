import sys

from Game import Game

if __name__ == '__main__':
    carcassonne = Game()
    #while carcassonne.gameOver is False:
    carcassonne.render()
    input()