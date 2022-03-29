from Agents import *
from Board import meepleInfo
from Feature import FeatType
from Player import Player
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
    def __init__(self, players=[RandomAgent(), RandomAgent()], order=[]):
        self.state = State([Player(0, players[0]), Player(1, players[1])], order)  
        #self.state.tileList = self.state.tileList[0:15]      

    def getState(self):
        # get the current game state
        return self.state

    def getScore(self):
        return self.state.players[0].score, self.state.players[1].score

    def getActions(self): #-> List[Action]
        # get current valid actions, where each action represents a 
        # tile placement, orientation, and meeple decision
        actions = validActions(self.state.board, self.state.currentTile, self.state.players[self.state.currentPlayer].meepleCount > 0)
        return actions

    def applyAction(self, action: Action):
        # update the state based on the action

        if action.meeple:

            
            meeple = meepleInfo(self.currentPlayer(),action.feature)
            self.state.board.meepled[(action.x, action.y)] = meeple
        
            # action.tile.occupied = action.feature
            # action.tile.occupied.occupiedBy = self.state.players[self.state.currentPlayer]
            self.state.players[self.state.currentPlayer].meepleCount -= 1

        self.state.playTile(action)
        self.state.currentPlayer = (self.state.currentPlayer + 1) % 2
        
    def currentPlayer(self):
        return self.state.players[self.state.currentPlayer]

    def currentPlayerId(self):
        return self.state.currentPlayer

    def gameOver(self) -> bool:
        # check for end of game
        return len(self.state.tileList) == 0

    def finalScore(self):
        if not self.gameOver():
            print("game not over")
            return (0,0)
        
        return tuple(map(sum, zip(self.getScore(), self.state.finalScore())))

    def render(self):
        # render the board
        render3(self.state.board, self.state.currentTile,self.state.players)

    ## Agent-side
    def copyState(self):
        # get a deep copy of the state
        pass

    def simulate(self, action: Action) -> State:
        # apply an action to a copy of the state and get the result state
        simState = copy.deepcopy(self.state)
        simAction = copy.deepcopy(action)

        if simAction.meeple:
            simAction.tile.occupied = simAction.feature
            simAction.tile.occupied.occupiedBy = simState.players[simState.currentPlayer]
            simState.players[simState.currentPlayer].meepleCount -= 1
        simState.playTile(simAction, quiet=True)
        simState.currentPlayer = (simState.currentPlayer + 1) % 2
        return simState

    def evaluate(self):
        # evaluate the position, to some positive or negative numeric score
        score = self.getScore()
        finalScore = self.state.finalScore()
        return (score[0]+finalScore[0],score[1]+finalScore[1])
    
    def scoreDelta(self):
        return self.evaluate[0] - self.evaluate[1]

    def board(self):
        return self.state.board


    ## Creates a simulation state that is independent of the real state
    def startSim(self) -> State:
        return copy.deepcopy(self.state)

    ## Applies an action to an independent state
    def simApply(self, simState: State, action: Action):
        #action.tile = copy.deepcopy(action.tile)
        simAction = copy.deepcopy(action)
        if simAction.meeple:
            meeple = meepleInfo(self.currentPlayer(),action.feature)
            simState.board.meepled[(action.x, action.y)] = meeple
            simState.players[simState.currentPlayer].meepleCount -= 1
        simState.playTile(simAction, quiet=True)
        simState.currentPlayer = (simState.currentPlayer + 1) % 2
        
    
    def refresh(self, simState: State):
        simState.players = copy.deepcopy(self.state.players)
        simState.currentPlayer = self.state.currentPlayer
        simState.order = self.state.order.copy()

        simState.tileList = self.state.tileList.copy()
        simState.currentTile = copy.deepcopy(self.state.currentTile)

        simState.board.board = self.state.board.board.copy()
        simState.board.openLocations = self.state.board.openLocations.copy()
        simState.board.trackedFeatures = self.state.board.trackedFeatures.copy()
        simState.board.trackedFields = self.state.board.trackedFields.copy()
        simState.board.meepled = self.state.board.meepled.copy()


    ## cache partially made features
    # when adding tiles, check if the tile's feature link to a previous feature
    # and check if they are meepled


    ## node
    # player 0, 1 or chance
        # UCT ignored random chance nodes (tree policy just picks a random one)
    # map from node to child random nodes where key is id of random node delivered

    ## node owned by p2
    # interstitial nodes representing the random tile being handed out
    ## node owned by p1
    # random deal node