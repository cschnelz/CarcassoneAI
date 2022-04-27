#from Action import Action

from __future__ import annotations
from re import L
import string
from tempfile import TemporaryFile
from typing import List, Dict, TYPE_CHECKING
from abc import ABC, abstractmethod


import random
import os
import copy
import math
import queue

from attr import mutable

class Agent(ABC):
    @abstractmethod
    def getResponse(self, validActions, game=None, maxPlayer=None):
        pass

class HumanAgent(Agent):
    def getResponse(self, validActions, game=None, maxPlayer=None):
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

class DummyAgent(Agent):
    def getResponse(self, validActions, game=None, maxPlayer=None):
        raise ValueError("Dummy Agent shouldn't ever be called")
