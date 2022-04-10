from Agents import *
from Board import meepleInfo
from Feature import FeatType
from Player import Player
from State import State
from Render import render3
from Action import validActions, Action


class Game:
    def __init__(self, players=[RandomAgent(), RandomAgent()], order=[]):
        self.state = State([Player(0, players[0]), Player(1, players[1])], order)  

    def getState(self) -> State:
        return self.state

    def getScore(self) -> tuple[int]:
        return self.state.players[0].score, self.state.players[1].score

    # get current valid actions, where each action represents a tile placement, orientation, and meeple decision
    def getActions(self) -> List[Action]:
        return self.state.currentActions

    # update the state based on the action
    def applyAction(self, action: Action) -> None: 
        self.state.applyAction(action)

    def currentPlayer(self) -> Player:
        return self.state.players[self.state.currentPlayer]

    def currentPlayerId(self) -> int:
        return self.state.currentPlayer

    def gameOver(self) -> bool:
        # check for end of game
        return self.state.turn >= 72

    def finalScore(self) -> tuple[int]:
        if not self.gameOver():
            print("game not over")
            return (0,0)
        
        return tuple(map(sum, zip(self.getScore(), self.state.finalScore())))

    def render(self):
        render3(self.state.board, self.state.currentTile,self.state.players)



    def copyState(self):
        pass
        
    # evaluate the position as if the game ended now
    def evaluate(self):
        score = self.getScore()
        finalScore = self.state.finalScore()
        return (score[0]+finalScore[0],score[1]+finalScore[1])
    
    # single digit eval difference of scores
    def scoreDelta(self):
        return self.evaluate[0] - self.evaluate[1]

    def board(self):
        return self.state.board


    ## Creates a simulation state that is independent of the real state
    def startSim(self) -> State:
        return copy.deepcopy(self.state)

    ## Applies an action to an independent state
    def simApply(self, simState: State, action: Action):
        simState.applyAction(action,quiet=True)        
    
    def refresh(self, simState: State):
        simState.players[0].meepleCount = self.state.players[0].meepleCount
        simState.players[1].meepleCount = self.state.players[1].meepleCount
        simState.players[0].score = self.state.players[0].score
        simState.players[1].score = self.state.players[1].score

        simState.currentPlayer = self.state.currentPlayer
        simState.order = self.state.order.copy()

        simState.tileList = self.state.tileList.copy()
        simState.currentTile = self.state.currentTile

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

