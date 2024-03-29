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
        walls = currentGameState.getWalls()
        if (walls[newPos[0]][newPos[1]]
        or currentGameState.getPacmanPosition() == successorGameState.getPacmanPosition()): return -1000
        score = 0
        for i, ghost in enumerate(newGhostStates):
            if(i<len(newScaredTimes) and newScaredTimes[i]>0):
                if(ghost.getPosition() == successorGameState.getPacmanPosition()):
                    score+=100
                if(newScaredTimes[i]>3 and ghost.getPosition()[0]+2 >= newPos[0] and ghost.getPosition()[0]-2 <= newPos[0] and ghost.getPosition()[1]+2 >= newPos[1] and ghost.getPosition()[1]-2 <= newPos[1]):
                    score+=10
            elif((ghost.getPosition()[0]+1 >= newPos[0] and ghost.getPosition()[0]-1 <= newPos[0] and ghost.getPosition()[1] == newPos[1])
                or (ghost.getPosition()[1]+1 >= newPos[1] and ghost.getPosition()[1]-1 <= newPos[1] and ghost.getPosition()[0]==newPos[0])):
                score-=100

        if newPos in currentGameState.getFood().asList():
            score += 10
        
        distances = []

        for food in currentGameState.getFood().asList():
            distances.append(manhattanDistance(food, newPos))
        score = score - min(distances)
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
        
        def ghostMoves(state, count, agentIndex):
            if state.isWin() or state.isLose(): return self.evaluationFunction(state)
            minValue = float('inf')
        
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents()-1:
                    minValue = min(minValue, pacmanMoves(state.generateSuccessor(agentIndex, action), count+1, 0))
                else:
                    minValue = min(minValue, ghostMoves(state.generateSuccessor(agentIndex, action), count, agentIndex+1))

            return minValue


        def pacmanMoves(state, count, agentIndex):
            if state.isWin() or state.isLose() or count==self.depth: return self.evaluationFunction(state)
            bestValue = float('-inf')
            for action in state.getLegalActions(agentIndex):
                value = ghostMoves(state.generateSuccessor(agentIndex, action), count, 1)
                bestValue = max(bestValue, value)
            return bestValue

        if gameState.isWin() or gameState.isLose(): return self.evaluationFunction(gameState)
        
        bestAction = ""
        bestValue = float('-inf')
        
        for action in gameState.getLegalActions(0):
            value = ghostMoves(gameState.generateSuccessor(0, action), 0, 1)
            if value >= bestValue:
                bestValue = value
                bestAction = action

        return bestAction

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
        
        def ghostMoves(state, count, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or count==self.depth: return self.evaluationFunction(state)
            minValue = float('inf')
        
            for action in state.getLegalActions(agentIndex):
                if minValue < alpha: return minValue
                if agentIndex == state.getNumAgents()-1:
                    minValue = min(minValue, pacmanMoves(state.generateSuccessor(agentIndex, action), count+1, 0, alpha, minValue))
                else:
                    minValue = min(minValue, ghostMoves(state.generateSuccessor(agentIndex, action), count, agentIndex+1, alpha, minValue))

            return minValue


        def pacmanMoves(state, count, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or count == self.depth: return self.evaluationFunction(state)
            bestValue = float('-inf')
            for action in state.getLegalActions(agentIndex):
                value = ghostMoves(state.generateSuccessor(agentIndex, action), count, 1, bestValue, beta)
                if value > beta: return value
                bestValue = max(bestValue, value)
            return bestValue

        if gameState.isWin() or gameState.isLose(): return self.evaluationFunction(gameState)
        
        bestAction = ""
        bestValue = float('-inf')
        
        for action in gameState.getLegalActions(0):
            value = ghostMoves(gameState.generateSuccessor(0, action), 0, 1, bestValue, 0)
            if value >= bestValue:
                bestValue = value
                bestAction = action
        
        return bestAction

        util.raiseNotDefined()

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
        
        def expMoves(state, count, agentIndex):
            if state.isWin() or state.isLose(): return self.evaluationFunction(state)
            value = 0
        
            p = 1/len(state.getLegalActions(agentIndex))
            
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents()-1:
                    value += p*pacmanMoves(state.generateSuccessor(agentIndex, action), count+1, 0)
                else:
                    value += p*expMoves(state.generateSuccessor(agentIndex, action), count, agentIndex+1)

            return value


        def pacmanMoves(state, count, agentIndex):
            if state.isWin() or state.isLose() or count==self.depth: return self.evaluationFunction(state)
            bestValue = float('-inf')
            for action in state.getLegalActions(agentIndex):
                bestValue = max(bestValue, expMoves(state.generateSuccessor(agentIndex, action), count, 1))
            return bestValue

        if gameState.isWin() or gameState.isLose(): return self.evaluationFunction(gameState)
        
        bestAction = ""
        bestValue = float('-inf')
        
        for action in gameState.getLegalActions(0):
            value = expMoves(gameState.generateSuccessor(0, action), 0, 1)
            if value >= bestValue:
                bestValue = value
                bestAction = action

        return bestAction
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <I used the scoreEvaluationFunction as a base score. Then added the distance of closest food and ghost in a way
    that makes pacman approach if pacman should approach, get away otherwise. Found the distance of closest object using bfs instead
    of manhattanDistance for better pathfinding>
    """
    "*** YOUR CODE HERE ***"
    
    currPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    walls = currentGameState.getWalls()
    ghostStates = currentGameState.getGhostStates()
    ghostPos = [ghost.getPosition() for ghost in ghostStates]
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    
    def bfs(currPos, dest, walls):
        actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        fringe = util.Queue()
        closed = set()
        fringe.push([currPos, 0])

        while(not fringe.isEmpty()):
            curr, dist = fringe.pop()
            if curr in dest:
                return [curr, dist]
            if curr not in closed:
                closed.add(curr)
                for action in actions:
                    if not walls[curr[0] + action[0]][curr[1] + action[1]] == True:
                        fringe.push([(curr[0]+action[0], curr[1]+action[1]), dist+1])
        return [dest[0], 0]
    
    score = scoreEvaluationFunction(currentGameState)
    
    ghostpos, ghostDist = bfs(currPos, ghostPos, walls)
    ghostInd = ghostPos.index(ghostpos)
    if ghostDist > 0 and scaredTimes[ghostInd]>0:
        score += 10/ghostDist
    elif ghostDist > 0:
        score -= 1/ghostDist

    if len(foods):
        pos, dist = bfs(currPos, foods, walls)
        if dist > 0:
            score += 1 / dist
    return score
    
    util.raiseNotDefined()
    

# Abbreviation
better = betterEvaluationFunction
