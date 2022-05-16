from Agents.Agent import RandomAgent
from Board import meepleInfo
from Feature import FeatType
from Player import Player
from State import State
from Render import render3
from Action import validActions, Action

from typing import List
import copy

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
        self.state.dispatchTile()

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
        simState = State([Player(0, RandomAgent()), Player(1,RandomAgent())], self.state.order.copy())
        self.refresh(simState)

        return simState

    ## Applies an action to an independent state
    def simApply(self, simState: State, action: Action):
        simState.applyAction(action,quiet=True)        
        simState.dispatchTile()
    
    def refresh(self, simState: State):
        simState.players[0].meepleCount = self.state.players[0].meepleCount
        simState.players[1].meepleCount = self.state.players[1].meepleCount
        simState.players[0].score = self.state.players[0].score
        simState.players[1].score = self.state.players[1].score

        simState.tileHist = self.state.tileHist.copy()
        simState.currentActions = self.state.currentActions.copy()
        simState.currentPlayer = self.state.currentPlayer
        simState.order = self.state.order.copy()
        simState.turn = self.state.turn

        simState.tileList = self.state.tileList.copy()
        simState.currentTile = self.state.currentTile

        simState.board.board = self.state.board.board.copy()
        simState.board.openLocations = self.state.board.openLocations.copy()
        simState.board.trackedFeatures = self.state.board.trackedFeatures.copy()
        simState.board.trackedFields = self.state.board.trackedFields.copy()
        simState.board.meepled = self.state.board.meepled.copy()

        simState.board.cityEdges = self.state.board.cityEdges.copy()
        simState.board.roadEdges = self.state.board.roadEdges.copy()
        simState.board.grassEdges = self.state.board.grassEdges.copy()

    def refreshSpecific(self,mutatedState:State, backupState:State):
        mutatedState.players[0].meepleCount = backupState.players[0].meepleCount
        mutatedState.players[1].meepleCount = backupState.players[1].meepleCount
        mutatedState.players[0].score = backupState.players[0].score
        mutatedState.players[1].score = backupState.players[1].score

        mutatedState.tileHist = mutatedState.tileHist.copy()
        mutatedState.currentActions = backupState.currentActions.copy()
        mutatedState.currentPlayer = backupState.currentPlayer
        mutatedState.order = backupState.order.copy()
        mutatedState.turn = backupState.turn

        mutatedState.tileList = backupState.tileList.copy()
        mutatedState.currentTile = backupState.currentTile

        mutatedState.board.board = backupState.board.board.copy()
        mutatedState.board.openLocations = backupState.board.openLocations.copy()
        mutatedState.board.trackedFeatures = backupState.board.trackedFeatures.copy()
        mutatedState.board.trackedFields = backupState.board.trackedFields.copy()
        mutatedState.board.meepled = backupState.board.meepled.copy()

        mutatedState.board.cityEdges = backupState.board.cityEdges.copy()
        mutatedState.board.roadEdges = backupState.board.roadEdges.copy()
        mutatedState.board.grassEdges = backupState.board.grassEdges.copy()

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

