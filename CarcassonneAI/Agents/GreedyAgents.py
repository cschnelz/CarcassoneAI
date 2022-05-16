from __future__ import annotations
from calendar import TUESDAY
import queue

from typing import List, TYPE_CHECKING

from Agents.Agent import Agent

import math
import random
import copy
import string

import multiprocessing
from Feature import FeatType


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
        #print(f'BA: {bestAction}')
        return bestAction
        
## A greedy agent with a 3 depth exhaustive search of all follow up tile possibilities
class Greedy3(Agent):
    if TYPE_CHECKING:
        from Game import Game
        from Action import Action
        from State import State

    def getResponse(self, validActions: List[Action], game:Game=None, maxPlayer:int=None):
        return self.getScore3(game)



    def getScore3(self, game:Game):
        mutable = game.startSim()
        backup_A = game.startSim()

        bestAvgOppEval = -math.inf
        bestAction = None
        for actionA in backup_A.currentActions:
            mutable.applyAction(actionA, quiet=True)        ## zero player

            ## find the average best eval the opponent could do for all possible next tiles
            cumulativeOppEval = 0.0
            tilesEvaluated = 0.0
            for tileB in mutable.uniqueRemainingTiles():    ## random dispatch of tiles
                if mutable.dispatchSpecific(tileB):     

                    ## find the best way the opposing player could play this tile
                    minEval = math.inf
                    for actionB in mutable.currentActions.copy():
                        mutable.applyAction(actionB, quiet=True) 
                        
                        res = mutable.scoreDelta()
                        if res < minEval:
                            minEval = res

                        ## refresh to before the random dispatch, but after we made our actionA
                        game.refreshSpecific(mutable, backup_A)
                        mutable.applyAction(actionA, quiet=True)
                    
                    ## add the eval for the best action the opponent would take given the current tile
                    cumulativeOppEval += minEval
                    tilesEvaluated += 1.0

            ## see if the average game eval for taking this action is higher than the previous best action
            averageOppEval = cumulativeOppEval  / tilesEvaluated
            if averageOppEval > bestAvgOppEval:
                bestAvgOppEval = averageOppEval
                bestAction = actionA

            game.refreshSpecific(mutable, backup_A)
        
        return bestAction

    def getScore(self, game:Game, sim:State, action:Action, depth, player):
        if depth == 0: ## or game is over
            return sim.scoreDelta(), action #<< - evaluate the state HUERISTIC

        bestAction = None
        level_save = copy.deepcopy(sim)
        
        if player == 'zero':
            maxEval = -math.inf
            for action in level_save.getActions():
                game.simApply(sim, action)
                res = self.getScore(game, sim, action, depth-1, 'one')
                eval = res[0]
                if eval > maxEval:
                    maxEval = eval
                    bestAction = action
                game.refreshSpecific(sim, level_save)
            
            return maxEval, bestAction

        if player == 'one':
            minEval = math.inf

            for action in level_save.getActions():
                game.simApply(sim, action)
                res = self.getScore(game, sim, action, depth-1, 'zero')
                eval = res[0]
                if eval < minEval:
                    minEval = eval
                    bestAction = action
                game.refreshSpecific(sim, level_save)

            return minEval, bestAction
   
    def randomLayer(self,game:Game,sim:State,action:Action,depth:int,nextPlayer):
        possible_tiles = sim.order.copy()
        cumulative = 0.0
        tiles_dispatched = 0.0
        if depth == 0:
            return sim.scoreDelta(), action

        for index in possible_tiles:
            if sim.dispatchSpecific(index):
                cumulative += self.getScoreRandom(game,sim,action,depth,nextPlayer)[0]
                tiles_dispatched += 1
        return cumulative / tiles_dispatched, action
    
 
class GreedyDeterminized(Agent):
    if TYPE_CHECKING:
        from Game import Game
        from Action import Action
        from State import State

    DETERMINZATIONS = 1
    CORES = 0
    TOTINNER = 0
    TOTONEDEP = 0
    
#     def getResponse(self, validActions, game:Game=None, maxPlayer=None):
        
#         self.game = game
#         ## generate a sample of random shuffles of possible next tiles - "determinzations"
#         self.determinzations = [game.state.order.copy() for i in range(self.DETERMINZATIONS)]
#         [random.shuffle(d) for d in self.determinzations]
        
#         ## goal: find the tile play that will get the best average continuation eval 
#         best_avg_eval = math.inf
#         best_avg_action = None


#         self.mutables = [game.startSim() for i in range(self.CORES)]
#         self.actions = game.state.getActions()
#         #print(len(self.actions))
#         self.action_stacks = [[] for i in range(self.CORES)] 

#         action_pool = multiprocessing.Pool(self.CORES)
#         action_stat = action_pool.map(self.getResMp, list(range(len(self.actions))))
             
#             ## find average after examining the determinzations and compare it to current best
#         for i in range(len(self.actions)):
#             if action_stat[i] < best_avg_eval:
#                 best_avg_eval = action_stat[i]
#                 best_avg_action = self.actions[i]

       
#         ## finally, return the action that we found to be the best across the sampled determinzations
#         return best_avg_action

#     def getResMp(self, i):
#         avg_eval = 0.0
#         examined = 0.0
#         poolNum = i%self.CORES
#         self.mutables[poolNum].applyAction(self.actions[i], quiet=True)
#         self.action_stacks[poolNum].append(self.actions[i])
#         depth = min(2, 71 - self.game.state.turn)

#         ## for this action, what the avg evaluation look like across sampled determinizations?
#         for det in self.determinzations:

#             if self.mutables[poolNum].dispatchSpecific(det[0]):
#                 ## two deep greedy search the continuation
#                 curr_eval, ret = self.search(self.mutables[poolNum], self.game, det[1:len(det)], depth, 'zero', self.action_stacks[poolNum])
#                 ## accrue stats
#                 avg_eval += curr_eval
#                 examined += 1.0
#         self.action_stacks[poolNum].clear()  
#         self.game.refresh(self.mutables[poolNum])
#         return avg_eval / examined

#     def search(self, mutable:State, game:Game, order:List[int], depth:int, maximizing:string, action_stack) -> tuple(int, Action):
#         if depth == 0:
#             return mutable.scoreDelta(), None

#         bestAction = None
#         if maximizing == 'zero':
#             maxEval = -math.inf
#             if mutable.players[mutable.currentPlayer].meepleCount > 0:
#                 actions = [a for a in mutable.getActions() if a.meeple]
#             else:
#                 actions = [a for a in mutable.getActions()]
#             for action in actions:
#                 self.TOTONEDEP += 1
#                 ## apply action and save it to stack
#                 mutable.applyAction(action, quiet=True)
#                 if mutable.dispatchSpecific(order[0]):
#                     action_stack.append(action)
                    
#                     ## recurse in and get evaluation
#                     res = self.search(mutable,game,order[1:len(order)],depth-1,'one',action_stack)
#                     if res[0] > maxEval:
#                         maxEval = res[0]
#                         bestAction = action

#                     ## pop action, rollback mutable state for next action
#                     action_stack.pop()
#                 game.refresh(mutable)
#                 [mutable.applyAction(a, quiet=True) for a in action_stack]
            
#             return maxEval, bestAction
                
#         if maximizing == 'one':
#             minEval = math.inf
#             for action in [a for a in mutable.getActions()]:
#                 self.TOTINNER += 1
#                 mutable.applyAction(action, quiet=True)
#                 if mutable.dispatchSpecific(order[0]):
#                     action_stack.append(action)

#                     res = self.search(mutable,game,order[1:len(order)],depth-1,'zero',action_stack)
#                     if res[0] < minEval:
#                         minEval = res[0]
#                         bestAction = action

#                     action_stack.pop()
#                 game.refresh(mutable)
#                 [mutable.applyAction(a, quiet=True) for a in action_stack]
            
#             return minEval, bestAction

    ## 46 sec for 

    # def getResponse(self, validActions, game:Game=None, maxPlayer=None):
      
    #     ## generate a sample of random shuffles of possible next tiles - "determinzations"
    #     self.action_stack = []    
    #     determinzations = [game.state.order.copy() for i in range(self.DETERMINZATIONS)]
        
    #     #[random.shuffle(d) for d in determinzations]
        
    #     ## goal: find the tile play that will get the best average continuation eval 
    #     best_avg_eval = math.inf
    #     best_avg_action = None

    #     mutable = game.startSim()
    #     self.backup = game.startSim()
    #     self.backupInner = game.startSim()

    #     depth = min(2, 71 - game.state.turn)

    #     for action in mutable.getActions(): ## if a.meeple and a.feature.featType is not FeatType.GRASS]:
    #         len_outer = len(mutable.getActions())
    #         avg_eval = 0.0
    #         examined = 0.0
    #         mutable.applyAction(action, quiet=True)
    #         self.backup.applyAction(action, quiet=True)
    #         self.backupInner.applyAction(action, quiet=True)

    #         self.action_stack.append(action)

    #         ## for this action, what the avg evaluation look like across sampled determinizations?
    #         for det in determinzations:

    #             if mutable.dispatchSpecific(det[0]):
    #                 ## two deep greedy search the continuation
    #                 curr_eval, ret = self.search(mutable, game, det[1:len(det)], depth, 'zero')
    #                 ## accrue stats
    #                 avg_eval += curr_eval
    #                 examined += 1.0
                    
    #         ## find average after examining the determinzations and compare it to current best
    #         avg_eval = avg_eval / examined
    #         if avg_eval < best_avg_eval:
    #             best_avg_eval = avg_eval
    #             best_avg_action = action

    #         self.action_stack.pop()  
    #         game.refresh(mutable)
    #         game.refresh(self.backup)
    #         game.refresh(self.backupInner)

    #     ## finally, return the action that we found to be the best across the sampled determinzations
    #     return best_avg_action

    # def search(self, mutable:State, game:Game, order:List[int], depth:int, maximizing:string) -> tuple(int, Action):
    #     if depth == 0:
    #         return mutable.scoreDelta(), None

    #     bestAction = None
    #     if maximizing == 'zero':
    #         maxEval = -math.inf
    #         for action in mutable.getActions():
    #             len_inner_z = len(mutable.getActions())
    #             ## apply action and save it to stack
    #             mutable.applyAction(action, quiet=True)
    #             self.backupInner.applyAction(action, quiet=True)
    #             if mutable.dispatchSpecific(order[0]):
    #                 self.action_stack.append(action)
                    
    #                 ## recurse in and get evaluation
    #                 res = self.search(mutable,game,order[1:len(order)],depth-1,'one')
    #                 if res[0] > maxEval:
    #                     maxEval = res[0]
    #                     bestAction = action

    #                 ## pop action, rollback mutable state for next action
    #                 self.action_stack.pop()
    #             game.refreshSpecific(mutable, self.backup)
    #             game.refreshSpecific(self.backupInner, self.backup)
    #             #[mutable.applyAction(a, quiet=True) for a in self.action_stack]
            
    #         return maxEval, bestAction
                
    #     if maximizing == 'one':
    #         minEval = math.inf
    #         for action in mutable.getActions():
    #             len_inner_o = len(mutable.getActions())
    #             mutable.applyAction(action, quiet=True)
    #             if mutable.dispatchSpecific(order[0]):
    #                 self.action_stack.append(action)

    #                 res = self.search(mutable,game,order[1:len(order)],depth-1,'zero')
    #                 if res[0] < minEval:
    #                     minEval = res[0]
    #                     bestAction = action

    #                 self.action_stack.pop()
    #             game.refreshSpecific(mutable, self.backupInner)
    #             #[mutable.applyAction(a, quiet=True) for a in self.action_stack]
            
    #         return minEval, bestAction




    def getResponse(self, validActions, game:Game=None, maxPlayer=None):
      
        ## generate a sample of random shuffles of possible next tiles - "determinzations"
        self.action_stack = []    
        determinzations = [game.state.order.copy() for i in range(self.DETERMINZATIONS)]
        
        #[random.shuffle(d) for d in determinzations]
        
        ## goal: find the tile play that will get the best average continuation eval 
        best_avg_eval = math.inf
        best_avg_action = None

        mutable = game.startSim()
        self.backup = game.startSim()
        self.backupInner = game.startSim()

        depth = min(2, 71 - game.state.turn)

        for action in mutable.getActions(): ## if a.meeple and a.feature.featType is not FeatType.GRASS]:
            len_outer = len(mutable.getActions())
            avg_eval = 0.0
            examined = 0.0
            mutable.applyAction(action, quiet=True)
            self.backup.applyAction(action, quiet=True)
            self.backupInner.applyAction(action, quiet=True)

            self.action_stack.append(action)

            ## for this action, what the avg evaluation look like across sampled determinizations?
            for det in determinzations:

                if mutable.dispatchSpecific(det[0]):
                    ## two deep greedy search the continuation
                    curr_eval, ret = self.search2(mutable, game, det[1:len(det)], depth, 'zero')
                    ## accrue stats
                    avg_eval += curr_eval
                    examined += 1.0
                    
            ## find average after examining the determinzations and compare it to current best
            avg_eval = avg_eval / examined
            if avg_eval < best_avg_eval:
                best_avg_eval = avg_eval
                best_avg_action = action

            self.action_stack.pop() 
            game.refresh(mutable)
            game.refresh(self.backup)
            game.refresh(self.backupInner)

        ## finally, return the action that we found to be the best across the sampled determinzations
        return best_avg_action

    def search2(self, mutable:State, game:Game, order:List[int], depth:int, maximizing:string) -> tuple(int, Action):
        bestAction = None
        maxEval = -math.inf
        for action in mutable.getActions():
            len_inner_z = len(mutable.getActions())
            ## apply action and save it to stack
            mutable.applyAction(action, quiet=True)
            self.backupInner.applyAction(action, quiet=True)
            if mutable.dispatchSpecific(order[0]):
                self.action_stack.append(action)
                
                ## recurse in and get evaluation
                res = self.search1(mutable,game,order[1:len(order)],depth-1,'one')
                if res[0] > maxEval:
                    maxEval = res[0]
                    bestAction = action

                ## pop action, rollback mutable state for next action
                self.action_stack.pop()
            game.refreshSpecific(mutable, self.backup)
            game.refreshSpecific(self.backupInner, self.backup)
            #[mutable.applyAction(a, quiet=True) for a in self.action_stack]
            
        return maxEval, bestAction

    def search1(self, mutable:State, game:Game, order:List[int], depth:int, maximizing:string) -> tuple(int, Action):
        bestAction = None
                
        minEval = math.inf
        for action in mutable.getActions():
            len_inner_o = len(mutable.getActions())
            mutable.applyAction(action, quiet=True)

            res = self.search0(mutable,game,order[1:len(order)],depth-1,'zero')
            if res[0] < minEval:
                minEval = res[0]
                bestAction = action

            game.refreshSpecific(mutable, self.backupInner)
            #[mutable.applyAction(a, quiet=True) for a in self.action_stack]
            
        return minEval, bestAction

    def search0(self, mutable:State, game:Game, order:List[int], depth:int, maximizing:string):
        return mutable.scoreDelta(), None