#from Action import Action

from __future__ import annotations
from re import L
from tempfile import TemporaryFile
from typing import List, Dict, TYPE_CHECKING
from abc import ABC, abstractmethod

import random
import os
import copy
import math
import queue

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
    
class GreedyAgent(Agent):
    if TYPE_CHECKING:
        from Game import Game
        from Action import Action

    def getResponse(self, validActions: List['Action'], game:'Game'=None, maxPlayer=None) -> 'Action':
        bestAction = validActions[0]
        bestDelta = -math.inf

        ## Starts a simulation, required before simulating
        simState = game.startSim()

        for action in validActions:
            game.simApply(simState, action)

            ## if maxPlayer == 0 we want delta to be positive because its P0 - P1
            lead = simState.scoreDelta() if maxPlayer == 0 else -1 * simState.scoreDelta()
            if lead > bestDelta:
                bestDelta = lead
                bestAction = action

            game.refresh(simState)
        return bestAction
        
## A greedy agent that prioritizes completing features to return meeples
class Greedy2(Agent):
    def getResponse(self, validActions, game=None, maxPlayer=None):
        pass

class MCTS_Agent(Agent):
    if TYPE_CHECKING:
       from Game import Game
       from Action import Action
       from State import State

    def __init__(self) -> None:
        # A list of rollback states 
        self.headStates = []
    
    def getLegalMoves(state:State) -> List[Action]:
        return state.getActions()

    def nextPlayer(currentPlayer:int) -> int:
        return (currentPlayer + 1) % 2

    def getResult(state:State) -> None|int:
        if state.gameOver() is False:
            return None
        return state.scoreDelta()

    ####*******####
    #             #  
    # ENTRY POINT #
    #             #
    ####*******####

    def getResponse(self, validActions: List[Action], game:Game=None, maxPlayer:int=None) -> Action:
        root = MCTS_Node(game.state,None,None,maxPlayer)
        for iteration in range(50):
            v = MCTS_Agent.tree_policy(root, maxPlayer)
            score = MCTS_Agent.default_policy(v, game)
            MCTS_Agent.backProp(v, score)
        move = MCTS_Agent.bestChild(root, 0)

        root.print_tree()
        print(f"\n\nBEST NODE: {move.action} UCB: {move.get_ucb()}")

        return move.action


    ####*******####
    #             #  
    # POLICYFUNCS #
    #             #
    ####*******####

    ## MCTS tree policy (selects child node to examine)
    def tree_policy(node: MCTS_Node, player:int) -> MCTS_Node:
        ## return the node if its a terminal
        if MCTS_Agent.getResult(node.state) is not None:
            return node 
        
        ## otherwise expand a new possible childNode <--- This is where the random will come in but for now its deterministic
        moves = MCTS_Agent.getLegalMoves(node.state)
        if len(moves) > len(node.children):
            return MCTS_Agent.expand(node, player)
        
        ## if all children have been expanded, go down the tree by what we think is the best candidate and recurs
        return MCTS_Agent.tree_policy(MCTS_Agent.bestChild(node), MCTS_Agent.nextPlayer(player))

    ## Adds a random successor node
    def expand(node:MCTS_Node, player:int) -> MCTS_Node:
        child = None
        for action in MCTS_Agent.getLegalMoves(node.state):
            if action not in node.children.keys():
                nextState = copy.deepcopy(node.state)
                nextState.applyAction(action,quiet=True)
                child = node.add_child(nextState,action,MCTS_Agent.nextPlayer(player))
                return child
        raise ValueError("Ran out of children when we shouldn't")

    ## Selection heuristic for following tree and finally move choice
    def bestChild(node:MCTS_Node, c=1) -> MCTS_Node:
        bestNode = list(node.children.values())[0]
        for action, node in node.children.items():
            if node.get_ucb(c) > bestNode.get_ucb(c):
                bestNode = node
        return bestNode

    ## Recurse up the tree now, incrementing vists and accumulating score
    def backProp(node:MCTS_Node,score:int) -> None:
        while node is not None:
            node.visits += 1
            if score > 0:
                node.zero_wins += score
            elif score < 0:
                node.one_wins += score
            node = node.parent

    ## Rollout randomly from a gamestate to game end
    def default_policy(node:MCTS_Node,game:Game,print_final=False) -> None|int:
        #current_state = copy.deepcopy(node.state)
        current_state = copy.deepcopy(node.state)

        while(current_state.gameOver() is False):
            moves = MCTS_Agent.getLegalMoves(current_state)
            current_state.applyAction(random.choice(moves), quiet=True)
            #game.simApply(current_state, random.choice(moves))
        return MCTS_Agent.getResult(current_state)


######################
#  Save a head state copy for the mcts search
#  when you get to default policy instead of copying the current node's state
#  create a new state by applying actions from the original state
#  when done, shallow-copy-restore the head state copy


class MCTS_Node:
    if TYPE_CHECKING:
        from Game import Game
        from State import State
        from Action import Action

    def __init__(self, state:'State', action:'Action', parent:'MCTS_Node', maxPlayer: int):
        self.zero_wins = 0
        self.one_wins = 0
        self.visits = 0

        if parent is None:
            self.num_parents = 0
        else:
            self.num_parents = parent.num_parents + 1

        self.state = state ## The state we are in
        self.action = action ## The action that got us here
        self.parent = parent ## The parent node we are descendent from

        ## will be a dict of {action : childNode } where childnode state is the result of applying action to this node state
        self.children: Dict['Action','MCTS_Node'] = {}
        self.player = maxPlayer # needs to be changed to "zero" "one" and "random"

    def __str__(self) -> str:
        if self.parent is None:
            p = "None"
        else:
            p = "TODO: Hash"
            ## p = get_hash(self.parent.state)
        try:
            expected_value = self.get_expected_value()
        except ValueError:
            expected_value = 0
        spacer = "   " * self.num_parents
        return spacer + f'Action {self.action}\n' + spacer + f' Visits={self.visits} Zero Wins={self.zero_wins} One Wins={self.one_wins}\n' + spacer + f' Expected Value={expected_value} UCB={self.get_ucb()}'

    ## MAKE SURE TO FLIP PLAYER BEFORE CALLING
    def add_child(self, nextState:'State', action:'Action', player:int) -> 'MCTS_Node':
        if action in self.children.keys():
            raise ValueError('dupe child')
        else:
            self.children[action] = MCTS_Node(nextState, action, self, player)
            return self.children[action]

    def get_p_win(self, player:int):
        try:
            if player == 0:
                return self.zero_wins / self.visits
            elif player == 1:
                return self.one_wins / self.visits
            else:
                raise ValueError(f'Given {player} for player, need 1 or 0')
        except ZeroDivisionError:
            raise ValueError('need atleast one visit before getting pwin')


    def get_expected_value(self) -> float:
        try:
            return (self.zero_wins - self.one_wins) / self.visits
        except ZeroDivisionError:
            raise ValueError('need atleast one visit before getting expected value')

    def get_explore_term(self, parent:MCTS_Node, c=1) -> float:
        if self.parent is not None:
            return c * (2*math.log(parent.visits) / self.visits) ** (1/2)
        return 0
    
    def get_ucb(self, c=1, default=6) -> float:
        if self.visits:
            p_win = self.get_expected_value()
            if self.player == 0:
                p_win *= -1
            explore_term = self.get_explore_term(self.parent,c)
            return p_win + explore_term
        return default

    def print_tree(self, max_nodes = 50):
        if max_nodes is None:
            max_nodes = len(self.children)+1
        print(f"Printing from node TODO: Hash {self}")
        q = queue.Queue()
        q.put(self)
        node_count = 0
        while not q.empty() and node_count < max_nodes:
            node_count += 1
            n = q.get()
            print(n)
            print()
            for key in n.children.keys():
                q.put(n.children[key])