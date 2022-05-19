from __future__ import annotations
import multiprocessing

from typing import List, TYPE_CHECKING, Dict
import multiprocessing as mp


from Agents.Agent import Agent

import math
import random
import copy
import string
import queue
import sys

#from tqdm import tqdm

## Performance enhacement idea 1

class Saver_Node:
    if TYPE_CHECKING:
       from Game import Game
       from Action import Action
       from State import State

    ## Node for MCTS_saver, uses action history to recreate states rather than storing each one
    def __init__(self, action:Action, parent:'Saver_Node', maxPlayer: int):
        if TYPE_CHECKING:
            from Game import Game
            from Action import Action
            from State import State
        self.zero_wins = 0.0
        self.one_wins = 0.0
        self.visits = 0.0

        if parent is None:
            self.num_parents = 0
        else:
            self.num_parents = parent.num_parents + 1

        self.terminal = False

        #self.state = state ## The state we are in
        self.action = action ## The action that got us here
        self.parent = parent ## The parent node we are descendent from

        ## will be a dict of {action : childNode } where childnode state is the result of applying action to this node state
        self.children: dict[Action,Saver_Node] = {}
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
        
        return spacer + f'Player {self.player} Action {self.action}\n' + spacer + f' Visits={self.visits} Zero Wins={self.zero_wins} One Wins={self.one_wins}\n' + spacer + f' Expected Value= {expected_value} UCB= {self.get_ucb(0)}'

    ## given a mutable rootState, reconstructs the state associated with this node
    def construct_state(self, rootState: State) -> State:
        action_hist = []
        curr = self
        while curr.parent is not None:
            action_hist.insert(0,curr.action)
            curr = curr.parent
        
        for action in action_hist:
            rootState.applyAction(action,quiet=True)
            rootState.dispatchTile()
        return rootState

    ## MAKE SURE TO FLIP PLAYER BEFORE CALLING
    def add_child(self, action:Action, player:int) -> 'Saver_Node':
        if action in self.children.keys():
            raise ValueError('dupe child')
        else:
            self.children[action] = Saver_Node(action, self, player)
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

    def get_explore_term(self, parent:'Saver_Node', c) -> float:
        if self.parent is not None:
            return c * ((2*math.log(parent.visits) / self.visits) ** (1/2))
        return 0
    
    def get_ucb(self, c, default=6) -> float:
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

    def get_first_actions(self) -> list[Action]:
        acts = list(self.children.keys())
        acts.sort(key=lambda action: (action.x, action.y, action.tile.orientation, action.meeple))
        return acts

    def get_first_nodes(self) -> list[tuple[Action,Saver_Node]]:
        nodes = list(self.children.items())
        nodes.sort(key=lambda item:(item[0].x, item[0].y, item[0].tile.orientation, item[0].meeple))
        return nodes

class MCTS_Saver(Agent):
    if TYPE_CHECKING:
       from Game import Game
       from Action import Action
       from State import State
       from Board import Board, builtFeature
    
    def getLegalMoves(state: State) -> list[Action]:
        return state.currentActions

    def nextPlayer(currentPlayer:int) -> int:
        return (currentPlayer + 1) % 2

    def getResult(state: State) -> int:
        if state.gameOver() is False:
            return None
        return state.scoreDelta()

    ####*******####
    #             #  
    # ENTRY POINT #
    #             #
    ####*******####

    def getResponse(self, validActions, game=None, maxPlayer=None):
        #return self.determinizedMCTS(validActions,game,maxPlayer)
        return self.determinizedMP(validActions,game,maxPlayer)

    DET = 100
    ITER = 1000

    C = 3
    CORES = 8

    def determinizedMCTS(self, vA,  game:Game=None, maxPlayer:int=None) -> Action:
        determinzation = game.state.order.copy()       
        
        stats = []
        self.backup = game.startSim()
        self.muteState = game.startSim()
        self.game = game

        for i in range(self.DET):
            random.shuffle(determinzation)
            self.backup.order = determinzation.copy()
            self.muteState.order = determinzation.copy()
            root = Saver_Node(None, None, maxPlayer)
            curr_stats = []

            for iteration in range(self.ITER):
                v = MCTS_Saver.tree_policy(root, maxPlayer, self.muteState, self.C)
                #score = MCTS_Saver.heuristic_policy(v,game,self.muteState)         
                       
                score = MCTS_Saver.hueristic_evaluation(v, self.game, self.muteState)
                self.game.refreshSpecific(self.muteState,self.backup)
                MCTS_Saver.backProp(v, score)

            for action, node in root.get_first_nodes():
               curr_stats.append(node.get_ucb(0))
            
            stats.append(curr_stats)
            game.refreshSpecific(self.muteState,self.backup)
        
        actions = root.get_first_actions()

        ## make a list of all first level nodes for each determinzation
        best_avg_ucb = -math.inf
        best_avg_action = None
        ## we want to compare average performace of actions across deterinzations
        ## so outer loop has a range of the number of possible actions
        for i in range(len(actions)):
            avg_ucb = 0.0
            ## and the inner loop ranges the number of determinzations
            for det in range(self.DET):
                ## add the ucb of this determinzations ith action
                avg_ucb += stats[det][i]
            avg_ucb = avg_ucb / self.DET
            ## if its better, we have a new candidate action
            if avg_ucb > best_avg_ucb:
                best_avg_ucb = avg_ucb
                ## we can use the nth determinization bc all the actions are equal
                best_avg_action = actions[i]
            
        #print(f"\n\nBEST AVG Action: {best_avg_action} AvgUcb: {best_avg_ucb}")
        return best_avg_action
    
    def determinizedMP(self, validActions, game:Game=None, maxPlayer=None):
        ## setup
        self.determinization = game.state.order.copy()
        self.backups = [game.startSim() for i in range(self.CORES)]
        self.muteStates = [game.startSim() for i in range(self.CORES)]
        self.game = game
        self.maxPlayer = maxPlayer

        ## pool and call mcts func for each determinization
        determinization_pool = mp.Pool(self.CORES)
        dets = list(range(self.CORES)) * int(self.DET / self.CORES)
        stats = determinization_pool.map(self.MpSub, dets)

        ## collect stats        
        actions = MCTS_Saver.getLegalMoves(game.state)

        ## make a list of all first level nodes for each determinzation
        best_avg_ucb = -math.inf
        best_avg_action = None
        ## we want to compare average performace of actions across deterinzations
        ## so outer loop has a range of the number of possible actions
        for i in range(len(stats[0])):
            avg_ucb = 0.0
            ## and the inner loop ranges the number of determinzations
            for det in range(len(stats)):
                ## add the ucb of this determinzations ith action
                avg_ucb += stats[det][i]
                
            avg_ucb = avg_ucb / self.DET
            ## if its better, we have a new candidate action
            if avg_ucb > best_avg_ucb:
                best_avg_ucb = avg_ucb
                ## we can use the nth determinization bc all the actions are equal
                best_avg_action = actions[i]
            
        #print(f"\n\nBEST AVG Action: {best_avg_action} AvgUcb: {best_avg_ucb}")
        return best_avg_action

    
    ## inner routine for the multiprocessing, runs the MCTS search for a tile order shuffle and returns the top level UCBs
    def MpSub(self, i):
        random.shuffle(self.determinization)
        #identity = mp.current_process()._identity[0] - 1
        try:
            self.muteStates[i].order = self.determinization.copy()
            self.backups[i].order = self.determinization.copy()
        except:
            print(i)
            sys.exit()
        
        root = Saver_Node(None, None, 0)
        for iteration in range(self.ITER):
            v = MCTS_Saver.tree_policy(root, self.maxPlayer, self.muteStates[i], self.C)

            #score = MCTS_Saver.default_fast(v, self.game, self.muteStates[i])
            score = MCTS_Saver.hueristic_evaluation(v, self.game, self.muteStates[i])
            self.game.refreshSpecific(self.muteStates[i],self.backups[i])
            MCTS_Saver.backProp(v, score)

        self.game.refreshSpecific(self.muteStates[i],self.backups[i])

        ## FINAL BEST CHILD POLICY -- MOST VISITED
        return [node.get_ucb(0) for action, node in root.get_first_nodes()]


    ####*******####
    #             #  
    # POLICYFUNCS #
    #             #
    ####*******####

    ## MCTS tree policy (selects child node to examine)
    def tree_policy(node: Saver_Node, player:int, muteState: State, explore) -> Saver_Node:
        ## return the node if its a terminal
        if node.terminal:
            return node 
        
        ## otherwise expand a new possible childNode <--- This is where the random will come in but for now its deterministic
        if node.action is not None:
            muteState.applyAction(node.action,quiet=True)
            muteState.dispatchTile()
        moves = MCTS_Saver.getLegalMoves(muteState)
        if len(moves) > len(node.children):
            return MCTS_Saver.expand(node, player, moves)
        
        ## if all children have been expanded, go down the tree by what we think is the best candidate and recurs
        return MCTS_Saver.tree_policy(MCTS_Saver.bestChild(node, explore), MCTS_Saver.nextPlayer(player), muteState, explore)

    ## Adds a random splayersuccessor node
    def expand(node:Saver_Node, player:int, actions: list[Action]) -> Saver_Node:
        child = None
        for action in actions:
            if action not in node.children.keys():
                child = node.add_child(action,MCTS_Saver.nextPlayer(player))
                return child
        raise ValueError("Ran out of children when we shouldn't")

    ## Selection heuristic for following tree and finally move choice
    def bestChild(node:Saver_Node, c) -> Saver_Node:
        max = float("-inf")
        best_child_key = None
        for key in node.children.keys():
            child = node.children[key]
            score = child.get_ucb(c)
            if score > max:
                max = score
                best_child_key = key
        key = best_child_key
        return node.children[key]

    ## Recurse up the tree now, incrementing vists and accumulating score
    def backProp(node:Saver_Node,score:int) -> None:
        while node is not None:
            node.visits += 1
            if score > 0:
                node.zero_wins += score
            elif score < 0:
                node.one_wins += (-1 * score)
            node = node.parent


    def default_fast(node:Saver_Node,game:Game,muteState:State,print_final=False) -> int:
        #node.construct_state(muteState)
        muteState.applyAction(node.action,quiet=True)
        muteState.dispatchTileOptimized()

        while(not muteState.gameOver()):
            moves = MCTS_Saver.getLegalMoves(muteState)
            muteState.applyAction(random.choice(moves),quiet=True)
            ## don't use the standard dispatchTile
            muteState.dispatchTileOptimized()

        return MCTS_Saver.getResult(muteState)


    ##
    ##
    ## HUERISTIC 1: CURRENT SCORE + SOME ODDS RATIO OF CITIES BEING FINISHED
    ##
    ##
    
    def hueristic_evaluation(node:Saver_Node,game:Game,muteState:State,print_final=False):
        from Board import Board, builtFeature
        from Feature import FeatType

        muteState.applyAction(node.action, quiet=True)
        state = muteState
        board = state.board

        ## RED
        baseRed = state.players[0].score
        meeplesRed = [(loc,info) for loc,info in board.meepled.items() if info.color == 'red']
        featsRed: list[builtFeature] = []
        for loc, info in meeplesRed:
            node = board.nodeAt(loc[0],loc[1])
            if info.featureObject.featType == FeatType.CHAPEL:
                featsRed.append(builtFeature(FeatType.CHAPEL,None,loc,None,None))
            elif info.feature:
                featsRed.append(board.findTracked(node,info.edge,board.trackedFeatures))
            else:
                featsRed.append(board.findTracked(node,info.edge,board.trackedFields))
        featsRed = [feat for feat in featsRed if feat is not None]

        meepleCountRed = state.players[0].meepleCount
        baseRed += MCTS_Saver.heuristic_roads(state, [feat for feat in featsRed if feat.featType == FeatType.ROAD], meepleCountRed)
        baseRed += MCTS_Saver.heuristic_city(state, [feat for feat in featsRed if feat.featType == FeatType.CITY], meepleCountRed)
        baseRed += MCTS_Saver.heuristic_chapel(state, [feat for feat in featsRed if feat.featType == FeatType.CHAPEL], meepleCountRed)
        baseRed += MCTS_Saver.heuristic_field(state, [feat for feat in featsRed if feat.featType == FeatType.GRASS], meepleCountRed)
        baseRed += MCTS_Saver.hueristic_meeples(meepleCountRed)

        ## BLUE
        baseBlue = state.players[1].score
        meeplesBlue = [(loc,info) for loc,info in board.meepled.items() if info.color == 'blue']
        featsBlue: list[builtFeature] = []
        for loc, info in meeplesBlue:
            node = board.nodeAt(loc[0],loc[1])
            if info.featureObject.featType == FeatType.CHAPEL:
                featsBlue.append(builtFeature(FeatType.CHAPEL,None,loc,None,None))
            elif info.feature:
                featsBlue.append(board.findTracked(node,info.edge,board.trackedFeatures))
            else:
                featsBlue.append(board.findTracked(node,info.edge,board.trackedFields))
        featsBlue = [feat for feat in featsBlue if feat is not None]

        meepleCountBlue = state.players[1].meepleCount
        baseBlue += MCTS_Saver.heuristic_roads(state, [feat for feat in featsBlue if feat.featType == FeatType.ROAD], meepleCountBlue)
        baseBlue += MCTS_Saver.heuristic_city(state, [feat for feat in featsBlue if feat.featType == FeatType.CITY], meepleCountBlue)
        baseBlue += MCTS_Saver.heuristic_chapel(state, [feat for feat in featsBlue if feat.featType == FeatType.CHAPEL], meepleCountBlue)
        baseBlue += MCTS_Saver.heuristic_field(state, [feat for feat in featsBlue if feat.featType == FeatType.GRASS], meepleCountBlue)
        baseBlue += MCTS_Saver.hueristic_meeples(meepleCountBlue)

        return baseRed - baseBlue




    TOTAL_TURNS = 72.0
    ROAD_BIAS = 0.025
    ROAD_CAPPED_BONUS = 1.25

    CITY_BIAS = 0.075

    def heuristic_roads(state:State, roads:list[builtFeature], meeples_left:int):
        total_road_score = 0.0
        for road in roads:
            base = road.score   # start with the road score
            bias = MCTS_Saver.ROAD_BIAS * ((MCTS_Saver.TOTAL_TURNS - state.turn) / 2.0) # add an amount representing future additions
            if len(road.holes) == 1:
                bias *= MCTS_Saver.ROAD_CAPPED_BONUS  # give a bonus to half-ended roads over no-ended roads
            
            road_score = base + bias
            total_road_score += road_score

        return total_road_score

    def heuristic_city(state:State, cities:list[builtFeature], meeples_left:int):
        total_city_score = 0.0
        for city in cities:
            base = city.score / 2  # start with city score
            odds = MCTS_Saver.CITY_BIAS * (((MCTS_Saver.TOTAL_TURNS - state.turn) / 2.0) / (len(city.holes)*.5)) # add a bias for finishing city divided by edges left open
            
            city_score = min(base * odds, ((base + 1)*2)-.1)
            total_city_score += city_score
        
        return total_city_score

    def heuristic_chapel(state:State, chapels:list[builtFeature], meeples_left:int):
        chapel_score = 0.0
        for chapel in chapels:
            chapel_neighbors = len(state.board.neighbors8(chapel.locs[0][0], chapel.locs[0][1]))
            chapel_score += min(9, ((MCTS_Saver.TOTAL_TURNS - state.turn) / 2) - (9 - chapel_neighbors))
        
        return chapel_score

    def heuristic_field(state:State, fields:list[builtFeature], meeples_left:int):
        field_score = 0.0
        for field in fields:
            adjacent_cities = set()
            for node,edge in field.adjacentCities.items():

                adjacent = list(set(node.tile.adjacentCity(node.tile.grassAtEdge(edge))))
                
                for cityEdge in adjacent:
                    builtCity = state.board.findTracked(node,cityEdge,state.board.trackedFeatures)
                    if builtCity is not None: #and builtCity not in citiesChecked:
                        adjacent_cities.add(builtCity)

            for city in adjacent_cities:
                field_score += (2.5 - len(city.holes))

        return field_score


    def hueristic_meeples(meeples_left:int):
        if meeples_left == 0:
            return 0
        elif meeples_left == 1:
            return 4
        elif meeples_left == 2:
            return 6
        else:
            return 4 + meeples_left