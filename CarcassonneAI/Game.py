from State import State
from Render import render3
## game class

## usage:

# game = Game(**Options)
# while not game.gameOver:
#   get action from human or ai
#   apply action
#   render

class Game:
    def __init__(self):
        self.state = State()

    def getState(self):
        # get the current game state
        return self.state

    def getActions(self): #-> List[Action]
        # get current valid actions, where each action represents a 
        # tile placement, orientation, and meeple decision
        pass

    def applyAction(self, action):
        # update the state based on the action

        # get a new tile as currentTile
        pass

    def gameOver(self) -> bool:
        # check for end of game
        pass

    def render(self):
        # render the board
        render3(self.state.board, self.state.currentTile,self.state.players)

    ## Agent-side
    def copyState(self):
        # get a deep copy of the state
        pass

    def simulate(self, action) -> State:
        # apply an action to a copy of the state and get the result state
        pass

    def evaluate(self) -> float:
        # evaluate the position, to some positive or negative numeric score
        pass