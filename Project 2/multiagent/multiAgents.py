# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        newGhostPos = successorGameState.getGhostPositions()
        nearestFood = 0
        numFood = len(newFood.asList()+successorGameState.getCapsules())
        if not len(newFood.asList()) == 0:
            nearestFood = min([manhattanDistance(food, newPos) for food in newFood.asList()\
                               +successorGameState.getCapsules()])
        cost = 0
        bonus = 0;
        ghosts = [manhattanDistance(newGhostPos[i], newPos) for i in range(len(newScaredTimes))\
                    if newScaredTimes[i] == 0]
                
        eatables = [manhattanDistance(newGhostPos[i], newPos) for i in range(len(newScaredTimes))\
                    if not newScaredTimes[i] == 0]
        
        if not len(ghosts) == 0:
            if min(ghosts) <= 1:
                cost = -99999
            else:
                cost = 0
                
        if not len(eatables) == 0:
            bonus = min(eatables)
            
        score = successorGameState.getScore()-0.5*nearestFood+cost-bonus-50*numFood
        
        return score
        
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
        
    def valueFunc(self, gameState, agentIndex, depth):
        numAgents = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose() or depth == self.depth*numAgents:
            return self.evaluationFunction(gameState), 'Stop'
        
        legalMoves = gameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            successors = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
            maxVal = -99999
            bestMove = 0
            for nextState in successors:
                score = self.valueFunc(nextState, (agentIndex+1)%numAgents, depth+1)[0]
                if score>maxVal:
                    maxVal = score
                    bestMove = legalMoves[successors.index(nextState)]
            return maxVal, bestMove
            
        else:
            successors = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
            minVal = 99999
            bestMove = 0
            for nextState in successors:
                score = self.valueFunc(nextState, (agentIndex+1)%numAgents, depth+1)[0]
                if score<minVal:
                    minVal = score
                    bestMove = legalMoves[successors.index(nextState)]
            return minVal, bestMove

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        score, action = self.valueFunc(gameState, 0, 0)
        return action
        
        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def valueFunc(self, gameState, agentIndex, depth, alpha, beta):
        numAgents = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose() or depth == self.depth*numAgents:
            return self.evaluationFunction(gameState), 'Stop'
        
        legalMoves = gameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            maxVal = -99999
            bestMove = 0
            for action in legalMoves:
                nextState = gameState.generateSuccessor(agentIndex, action)
                score = self.valueFunc(nextState, (agentIndex+1)%numAgents, depth+1, alpha, beta)[0]
                #print alpha, score
                alpha = max(alpha, score)
                
                if score>maxVal:
                    maxVal = score
                    bestMove = action
                
                if alpha > beta:
                    return alpha, bestMove                
                
            return maxVal, bestMove
            
        else:
            minVal = 99999
            bestMove = 0
            for action in legalMoves:
                nextState = gameState.generateSuccessor(agentIndex, action)
                score = self.valueFunc(nextState, (agentIndex+1)%numAgents, depth+1, alpha, beta)[0]
                beta = min(beta, score)                 
                
                if score<minVal:
                    minVal = score
                    bestMove = action
                
                if beta < alpha:
                    return beta, bestMove

                
            return minVal, bestMove

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        score, action = self.valueFunc(gameState, 0, 0, -99999, 99999)
        return action        
        
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    
    def valueFunc(self, gameState, agentIndex, depth):
        numAgents = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose() or depth == self.depth*numAgents:
            return self.evaluationFunction(gameState), 'Stop'
        
        legalMoves = gameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            maxVal = -99999
            bestMove = 'Stop'
            for action in legalMoves:
                nextState = gameState.generateSuccessor(agentIndex, action)
                score = self.valueFunc(nextState, (agentIndex+1)%numAgents, depth+1)[0]
                if score>maxVal:
                    maxVal = score
                    bestMove = action
                    
            return maxVal, bestMove
            
        else:
            sumVal = 0
            for action in legalMoves:
                nextState = gameState.generateSuccessor(agentIndex, action)
                sumVal += self.valueFunc(nextState, (agentIndex+1)%numAgents, depth+1)[0]
                
            expectiVal = sumVal/len(legalMoves)
            
            return expectiVal, 'Stop'   

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        score, action = self.valueFunc(gameState, 0, 0)
        return action
    
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 
      My Pacman state evaluation score consist of 6 parts. Get state score to
      avoid time penalty, this is an incentive to keep Pacman moving. The closer
      to the nearest food, the higher the score, however, the drawback is that
      when the Pacman get to the food, it may not eat the food since if the 
      nearest food gone, the new nearest food distance is taking down the score,
      so I add the number of food as another motivation for Pacman to eat the food.
      The food list is the concatenation of foods and capsules. 
      
      The cost is the distance to the nearest ghosts, if it touches the ghosts, the
      penalty is huge, so that it will avoid being killed. But if some of the ghosts
      is scared, getting closer to those ghosts will have bonus, the incresed score
      of eating them will give it the incentive to eat scared ghost. 
      
      If in this state, Pacman is winning, then the a winning bonus will be given to
      finish the game as soon as possible.
      
      Hence, my evaluation score is:
      Score = Current Score - 0.5*Food Distance - 50*number of foods + Ghosts Distance + Eatable Ghost Distance + Winning Bonus
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]    
    
    newGhostPos = currentGameState.getGhostPositions()
    nearestFood = 0
    numFood = len(newFood.asList()+currentGameState.getCapsules())
    if not len(newFood.asList()) == 0:
        nearestFood = min([manhattanDistance(food, newPos) for food in newFood.asList()\
                           +currentGameState.getCapsules()])
    cost = 0
    bonus = 0;
    ghosts = [manhattanDistance(newGhostPos[i], newPos) for i in range(len(newScaredTimes))\
                if newScaredTimes[i] == 0]
            
    eatables = [manhattanDistance(newGhostPos[i], newPos) for i in range(len(newScaredTimes))\
                if not newScaredTimes[i] == 0]
    
    if not len(ghosts) == 0:
        if min(ghosts) <= 1:
            cost = -99999
        else:
            cost = 0
            
    if not len(eatables) == 0:
        bonus = min(eatables)
    
    winPts = 0
    losePts = 0
    if currentGameState.isWin():
        winPts = 9999
        
    score = currentGameState.getScore()-0.5*nearestFood-50*numFood+cost-bonus+winPts
    
    return score    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

