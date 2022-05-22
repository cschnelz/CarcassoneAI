from turtle import back
from Agents.Agent import RandomAgent
from Board import meepleInfo, builtFeature, Node
from Feature import FeatType
from Player import Player
from State import State
from Render import Renderer
from Action import validActions, Action
import collections

from typing import List
import copy


class Game:
    def __init__(self, players=[RandomAgent(info=None), RandomAgent(info=None)], order=[]):
        self.state = State([Player(0, players[0]), Player(1, players[1])], order)  

    def getState(self) -> State:
        return self.state

    def getScore(self) -> tuple[int]:
        return self.state.players[0].score, self.state.players[1].score

    # get current valid actions, where each action represents a tile placement, orientation, and meeple decision
    def getActions(self) -> List[Action]:
        return self.state.currentActions

    # update the state based on the action
    def applyAction(self, action: Action) -> list[tuple[int]]: 
        locs = self.state.applyAction(action)
        self.state.dispatchTile()
        return locs

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

    def render(self, renderer:Renderer):
        renderer.render3(self.state.board, self.state.currentTile,self.state.players)



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

    def compareStates(self, stateA:State, stateB:State):
        if  stateA.players[0].meepleCount != stateB.players[0].meepleCount or \
            stateA.players[1].meepleCount != stateB.players[1].meepleCount or \
            stateA.players[0].score != stateB.players[0].score or \
            stateA.players[1].score != stateB.players[1].score:
            print("mismatch in player")

        if stateA.turn != stateB.turn:
            print("mismatch in turn")

        if collections.Counter(stateA.order) != collections.Counter(stateB.order):
            print("mismatch in order")

        if collections.Counter(stateA.currentActions) != collections.Counter(stateB.currentActions):
            print("mismatch in current actions")

        if collections.Counter(stateA.currentTile) != collections.Counter(stateB.currentTile):
            print("mismatch in current tile")

        if collections.Counter(stateA.board.trackedFeatures) != collections.Counter(stateB.board.trackedFeatures):
            a = stateA.board.trackedFeatures
            b = stateB.board.trackedFeatures
            print("mismatch in tracked features")
        if collections.Counter(stateA.board.trackedFields) != collections.Counter(stateB.board.trackedFields):
            print("mismatch in tracked fields")

        if collections.Counter(stateA.board.meepled) != collections.Counter(stateB.board.meepled):
            print("mismatch in meepled")
        
    
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
        
        
        #simState.board.trackedFeatures = self.state.board.trackedFeatures.copy()
        simState.board.trackedFeatures = []
        for tF in self.state.board.trackedFeatures:
            newTF = builtFeature(tF.featType, None, None, None, None)
            newTF.tracked = tF.tracked.copy()
            newTF.locs = tF.locs.copy()
            newTF.meepled = tF.meepled.copy()
            newTF.coordsMeepled = tF.coordsMeepled.copy()
            newTF.score = tF.score
            newTF.adjacentCities = tF.adjacentCities.copy()
            newTF.holes = tF.holes.copy()
            newTF.completed = tF.completed
            simState.board.trackedFeatures.append(newTF)

       # simState.board.trackedFields = self.state.board.trackedFields.copy()
        simState.board.trackedFields = []
        for tF in self.state.board.trackedFields:
            newTF = builtFeature(tF.featType, None, None, None, None)
            newTF.tracked = tF.tracked.copy()
            newTF.locs = tF.locs.copy()
            newTF.meepled = tF.meepled.copy()
            newTF.coordsMeepled = tF.coordsMeepled.copy()
            newTF.score = tF.score
            newTF.adjacentCities = tF.adjacentCities.copy()
            newTF.holes = tF.holes.copy()
            newTF.completed = tF.completed
            simState.board.trackedFields.append(newTF)

        simState.board.meepled = self.state.board.meepled.copy()

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

        #mutatedState.board.board = backupState.board.board.copy()
        mutatedState.board.board = {}
        for loc, node in backupState.board.board.items():
            newNode = Node(node.x, node.y, node.tile)
            newNode.neighbors = node.neighbors.copy()
            mutatedState.board.board[loc] = newNode
        mutatedState.board.openLocations = backupState.board.openLocations.copy()

        #mutatedState.board.trackedFeatures = backupState.board.trackedFeatures.copy()
        mutatedState.board.trackedFeatures = []
        for tF in backupState.board.trackedFeatures:
            newTF = builtFeature(tF.featType, None, None, None, None)
            newTF.tracked = tF.tracked.copy()
            newTF.locs = tF.locs.copy()
            newTF.meepled = tF.meepled.copy()
            newTF.coordsMeepled = tF.coordsMeepled.copy()
            newTF.score = tF.score
            newTF.adjacentCities = tF.adjacentCities.copy()
            newTF.holes = tF.holes.copy()
            newTF.completed = tF.completed
            mutatedState.board.trackedFeatures.append(newTF)

        #mutatedState.board.trackedFields = backupState.board.trackedFields.copy()
        mutatedState.board.trackedFields = []
        for tF in backupState.board.trackedFields:
            newTF = builtFeature(tF.featType, None, None, None, None)
            newTF.tracked = tF.tracked.copy()
            newTF.locs = tF.locs.copy()
            newTF.meepled = tF.meepled.copy()
            newTF.coordsMeepled = tF.coordsMeepled.copy()
            newTF.score = tF.score
            newTF.adjacentCities = tF.adjacentCities.copy()
            newTF.holes = tF.holes.copy()
            newTF.completed = tF.completed
            mutatedState.board.trackedFields.append(newTF)

        #mutatedState.board.meepled = backupState.board.meepled.copy()
        mutatedState.board.meepled = {}
        for tuple, mI in backupState.board.meepled.items():
            newMI = meepleInfo(mutatedState.players[mI.id], mI.featureObject)
            mutatedState.board.meepled[tuple] = newMI

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

