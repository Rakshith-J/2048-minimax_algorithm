#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
from sysconfig import sys
import time


#sys.setrecursionlimit(4000)

class PlayerAI(BaseAI):

    #variable that keeps track of the most optimal direction the PlayerAI can make
    def _init_(self):
        self.direction = -1

    #Input for heuristic: Gets the top four tiles and returns to eval function.
    def getMaxTiles(self, grid):
        maxTile = 0
        dist = 0
        maxTiles = [0, 0, 0, 0]
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                dist = dist+(x-y)*grid.map[x][y]*3.0
                maxTile = grid.map[x][y]
                if maxTile > maxTiles[0]:
                    maxTiles[0]=maxTile
                    maxTiles.sort(cmp=None, key=None, reverse=False)
        maxTiles.append(dist)
        return maxTiles
    
    def adjdif(self,grid):
                diff = 0
                c = 0
                for i in xrange(grid.size-1):
                        for j in xrange(grid.size):
                                c=c+1
                                diff=diff+grid.map[i][j]-grid.map[i+1][j]
                for j in xrange(grid.size-1):
                        for i in xrange(grid.size):
                                c=c+1
                                diff=diff+grid.map[i][j]-grid.map[i][j+1]
                return diff/c
                                
    #Heuristic: Calculates the utility at leaf node based on - number of empty cells available, top 4 maxTiles values
    #and weighted distance of tiles from bottom left corner.    
    def evalfn(self,grid):
        cell = grid.getAvailableCells()
        maxTiles = self.getMaxTiles(grid)
        maxSum = sum(maxTiles)-maxTiles[4]
        #diff= self.adjdif(grid)
        evalScore = len(cell)*5000+maxSum*0.8+maxTiles[4]*2#-diff*1000
        return(evalScore)
        
            
    #Allocates new tile as either number 2 (probability 0.9) or 4 (probability 0.1)
    def getNewTileValue(self):
        if randint(0,99) < 100 * 0.9: 
            return 2 
        else: 
            return 4    

    #Minimax algorithm implementation with alpha-beta pruning
    def alphabeta(self, grid, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            e = self.evalfn(grid)
            return [e,-1]
        if maximizingPlayer:
            moves = grid.getAvailableMoves()
            if moves == []:
                return [alpha, self.direction]
            for i in moves:
                newgrid = grid.clone()
                newgrid.move(i)
                r = self.alphabeta(newgrid, depth-1, alpha, beta, False)
                if alpha < r[0]:
                    self.direction = i
                if r[0] == -float('inf'):
                    self.direction = i  
                if beta <= alpha:
                    break
                alpha = max(alpha, r[0])
            result = [alpha, self.direction]
            return result
        else:
            moves = grid.getAvailableMoves()
            if moves == []:
                return [beta, self.direction]
            for i in moves:
                newgrid = grid.clone()
                newgrid.move(i)
                r = self.alphabeta(newgrid, depth-1, alpha, beta, True)
                if beta > r[0]:
                    self.direction = i
                if r[0] == float('inf'):
                    self.direction = i
                if beta <= alpha:
                    break
                beta = min(beta, r[0])   
            result = [beta, self.direction]
            return result
    
    #Returns the optimal move per the algorithm to the GameManager function.
    def getMove(self, grid):
                result = self.alphabeta(grid, 3, -float('inf'), float('inf'), True)
                return result[1]
    
        #return moves[randint(0, len(moves) - 1)] if moves else None                    
    
    
    
    
    
