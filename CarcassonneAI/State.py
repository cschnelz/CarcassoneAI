## Holds all information about the current game state

from typing import List

from Board import Board
from Player import Player
from Import import importTiles

from random import random

class State:
    def __init__(self):
        self.players: List[Player] = [Player(0), Player(1)]
        self.currentPlayer = 0
        
        self.tileList = importTiles('TileSetSepRoads.json')
        self.currentTile = self.dispatchTile()

        self.board = Board(self.currentTile)
        self.currentTile = self.dispatchTile()
    
    def dispatchTile(self):
        dispatchId = int(random() * len(self.tileList))
        tile = self.tileList[dispatchId]
        del self.tileList[dispatchId]
        return tile
    