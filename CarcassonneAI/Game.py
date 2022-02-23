from State import State
from Render import render3
from Action import validActions, Action
from Tile import Tile
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
        self.state.tileList = self.state.tileList[0:15]

    def getState(self):
        # get the current game state
        return self.state

    def getActions(self): #-> List[Action]
        # get current valid actions, where each action represents a 
        # tile placement, orientation, and meeple decision
        actions = validActions(self.state.board, self.state.currentTile)
        return actions

    def applyAction(self, action: Action):
        # update the state based on the action
        tile = action.tile

        if action.meeple:
            tile.occupied = action.feature
            tile.occupied.occupiedBy = self.state.players[self.state.currentPlayer]
            self.state.players[self.state.currentPlayer].meepleCount -= 1

        self.state.board.addTile(action.x,action.y,action.tile)
        self.state.currentTile = self.state.dispatchTile()
        self.state.currentPlayer = (self.state.currentPlayer + 1) % 2
        
    def currentPlayer(self):
        return self.state.players[self.state.currentPlayer]

    def gameOver(self) -> bool:
        # check for end of game
        return len(self.state.tileList) == 0

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