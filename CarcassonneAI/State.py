## Holds all information about the current game state

from typing import List

from Board import Board
from Tile import Tile  
from Player import Player
from Import import importTiles
from Manager import *

class State:
    def __init__(self):
        self.players: List[Player] = [Player(0), Player(1)]
        self.currentPlayer = 0
        
        self.tileList: List[Tile] = importTiles('TileSetSepRoads.json')
        self.currentTile = dispatchTile()

        self.board = Board(self.currentTile)