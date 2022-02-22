## Holds all information about the current game state

from typing import List

from Board import Board
from Tile import Tile    

class State:
    def __init__(self):
        self.board: Board = None
        self.players: List[Player] = None
        self.tileList: List[Tile] = None