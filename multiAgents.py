# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        foodDistances = [ manhattanDistance(food,newPos) for food in newFood.asList()]
        if not foodDistances:
            return float('inf')
        foodCloset = min(foodDistances)
        
        for ghostState in newGhostStates:
            ghostPosition = ghostState.getPosition()
            if ghostState.scaredTimer == 0 and manhattanDistance(ghostPosition,newPos) < 2:
                return -float('inf')

        return successorGameState.getScore() + 1/foodCloset

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        maxValue = -float('inf')
        bestAction = None
        for action in gameState.getLegalActions(0):
            #lấy action có giá trị lớn nhất trong list next action of gost
            if self.minValueAction(gameState.generateSuccessor(0, action), 1, 0) > maxValue:
                maxValue = self.minValueAction(gameState.generateSuccessor(0, action), 1, 0)
                bestAction = action
        return bestAction

    def minValueAction(self, gameState, agentIndex, depth):
        #giá trị của action của ma sẽ là giá trị nhỏ nhất của các con ma phía sau
        minVal = float('inf')
        if len(gameState.getLegalActions(agentIndex)) == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex < gameState.getNumAgents() - 1:
            for action in gameState.getLegalActions(agentIndex):
                if minVal > self.minValueAction(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth):
                    minVal = self.minValueAction(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth)
            return minVal
        else: #đến con ma cuối thì sẽ chuyển sang depth sau và tìm min của pacman ở depth đó
            for action in gameState.getLegalActions(agentIndex):
                if minVal > self.maxValueAction(gameState.generateSuccessor(agentIndex, action), depth + 1):
                    minVal = self.maxValueAction(gameState.generateSuccessor(agentIndex, action), depth + 1)
            return minVal
    def maxValueAction(self, gameState, depth):
        #hàm lấy giá trị max cho action của pacman 
        maxVal = -float('inf')
        if len(gameState.getLegalActions(0)) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(0):
            if maxVal < self.minValueAction(gameState.generateSuccessor(0, action), 1, depth):
                maxVal = self.minValueAction(gameState.generateSuccessor(0, action), 1, depth)
        return maxVal
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, self.depth)[1]
        util.raiseNotDefined()
    
    def minimax(self, gameState, agentIndex, depth, alpha = -float('inf'), beta = float('inf')):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return ( self.evaluationFunction(gameState), "Stop")
        
        agentsNum = gameState.getNumAgents()
        agentIndex %=  agentsNum
        #khi den con ghost cuoi cung thi tru do sau 1
        if agentIndex == agentsNum - 1:
            depth -= 1

        # khi day la pacman, tinh gia tri max cho pacman
        if agentIndex == 0:
            actions = []
            for action in gameState.getLegalActions(agentIndex):
                v = self.minimax(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth, alpha, beta)[0]
                actions.append((v, action))
                if v > beta:
                    return (v, action)
                alpha = max(alpha, v)
            return max(actions)
        # khi day la ghost, tinh gia tri min cho ghost
        else:
            actions = []
            for action in gameState.getLegalActions(agentIndex):
                v = self.minimax(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth, alpha, beta)[0]
                actions.append((v, action))
                if v < alpha:
                    return (v, action)
                beta = min(beta, v)
            return min(actions)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
            def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # print gameState.getPacmanPosition()

        def expectimax(gameState, agentIndex, currentDepth):
            agents = gameState.getNumAgents()

            if currentDepth == self.depth * agents or gameState.isWin() or gameState.isLose():
                return float(self.evaluationFunction(gameState))

            if agentIndex == 0:
                val = -float('inf')
            else: 
                val = 0
                
            actions = len(gameState.getLegalActions(agentIndex))
            
            for action in gameState.getLegalActions(agentIndex):
                sucState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == 0:
                    val = max(val, expectimax(sucState, (agentIndex + 1) % agents, currentDepth + 1))
                else:
                    val += (1.0 / actions) * expectimax(sucState, (agentIndex + 1) % agents, currentDepth + 1)

            return val

        val = -float('inf')
        optimal = None
        for action in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0, action)
            temp = expectimax(successorState, 1, 1)

            if temp > val:
                val = temp
                optimal = action

        return optimal


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
