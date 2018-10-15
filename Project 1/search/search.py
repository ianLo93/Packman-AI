# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    "*** YOUR CODE HERE ***"
    iniState = problem.getStartState()
    if problem.isGoalState(iniState):
        return ['Stop']
   
    fringe = util.Stack()
    paths = util.Stack()
    nextStates = problem.getSuccessors(iniState)
    for i in range(len(nextStates)):
        actions = [nextStates[-i-1][1]]
        fringe.push(nextStates[-i-1])
        paths.push(actions)
    visited = [iniState]
    while True:
        if fringe.isEmpty():
            break
        state = fringe.pop()
        moves = paths.pop()
        if state[0] in visited:
            continue
        visited.append(state[0]) 
        if problem.isGoalState(state[0]):
            break
        nextStates = problem.getSuccessors(state[0])
        for i in range(len(nextStates)):
            actions = moves + [nextStates[-i-1][1]]
            if nextStates[-i-1][0] not in visited:
                fringe.push(nextStates[-i-1])   
                paths.push(actions)
    
    return moves
        
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    iniState = problem.getStartState()
    if problem.isGoalState(iniState):
        return ['Stop']
    
    fringe = util.Queue()
    fringe.push(iniState)
    paths = util.Queue()
    visited = [iniState]
    head = fringe.pop()
    for successor in problem.getSuccessors(head):
        actions = [successor[1]]
        fringe.push(successor)
        paths.push(actions)
        visited.append(successor[0])
        
    while True:
        if fringe.isEmpty():
            print "No way to get there"
            return []
        head = fringe.pop()
        moves = paths.pop()
        if problem.isGoalState(head[0]):
            return moves
        for successor in problem.getSuccessors(head[0]):
            actions = moves + [successor[1]]
            if successor[0] in visited:
                continue
            fringe.push(successor)
            paths.push(actions)
            visited.append(successor[0])
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    iniState = problem.getStartState()
    if problem.isGoalState(iniState):
        return ['Stop']
    
    fringe = util.PriorityQueue()
    paths = util.PriorityQueue()
    visited = [iniState]
    for successor in problem.getSuccessors(iniState):
        actions = [successor[1]]
        fringe.push(successor, problem.getCostOfActions(actions))
        paths.push(actions, problem.getCostOfActions(actions))
        visited.append(successor[0])

    while True:
        state = fringe.pop()
        moves = paths.pop()
        if problem.isGoalState(state[0]):
            return moves
        for successor in problem.getSuccessors(state[0]):
            actions = moves + [successor[1]]            
            if successor[0] in visited:
                tmp_fringe = util.PriorityQueue()
                tmp_paths = util.PriorityQueue()
                while not fringe.isEmpty():
                    pos = fringe.pop()
                    act = paths.pop()
                    if pos[0] == successor[0] and successor[2] < pos[2]:
                        pos = successor
                        act = actions
                    tmp_fringe.push(pos, problem.getCostOfActions(act))
                    tmp_paths.push(act, problem.getCostOfActions(act))
                fringe = tmp_fringe
                paths = tmp_paths
                continue
            fringe.push(successor, problem.getCostOfActions(actions))
            paths.push(actions, problem.getCostOfActions(actions))
            visited.append(successor[0])
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    iniState = problem.getStartState()
    if problem.isGoalState(iniState):
        return ['Stop']
    
    fringe = util.PriorityQueue()
    paths = util.PriorityQueue()
    visited = [iniState]
    for successor in problem.getSuccessors(iniState):
        actions = [successor[1]]
        f = problem.getCostOfActions(actions) + heuristic(successor[0], problem)
        fringe.push(successor, f)
        paths.push(actions, f)
    
    while True:
        if fringe.isEmpty():
            print "No way to get there"
            return []
        state = fringe.pop()
        moves = paths.pop()
        if state[0] in visited:
            continue
        visited.append(state[0])
        if problem.isGoalState(state[0]):          
            return moves
        for successor in problem.getSuccessors(state[0]):
            actions = moves + [successor[1]]
            f = problem.getCostOfActions(actions) + heuristic(successor[0], problem)
            fringe.push(successor, f)
            paths.push(actions, f)
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
