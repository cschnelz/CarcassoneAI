#from Action import Action

from typing import List
from abc import ABC, abstractmethod

import random
import os
import copy
import math

class Agent(ABC):
    @abstractmethod
    def getResponse(self, validActions, board=None, maxPlayer=None):
        pass

class HumanAgent(Agent):
    def getResponse(self, validActions, board=None, maxPlayer=None):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        while True:
            res = input("desired location: ").split()
            x = int(res[0])
            y = int(res[1])
            
            for index, action in enumerate(validActions):
                if action.x == x and action.y == y:
                    print(f"Option {index}: {action}")

            res = int(input("placement option or -1 to relocate: "))
            if res == -1:
                continue
            return validActions[res]

class RandomAgent(Agent):
    def getResponse(self, validActions, game=None, maxPlayer=None):
        return random.choice(validActions)
    

class GreedyAgent(Agent):
    def getResponse(self, validActions, game=None, maxPlayer=None):
        bestAction = validActions[0]
        bestDelta = -math.inf

        for action in validActions:
            state = game.simulate(action)

            ## if maxPlayer == 0 we want delta to be positive because its P0 - P1
            lead = state.scoreDelta() if maxPlayer == 0 else -1 * state.scoreDelta()
            if lead > bestDelta:
                bestDelta = lead
                bestAction = action

        return bestAction
        