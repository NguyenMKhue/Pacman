import math
import sys
def maxManhattanFoodHeuristic(state):
    x,y = state.getPosition()
    if len(state.getGoals())>0 :
        return max([manhatthan(xi,yi,x,y) for (xi,yi) in state.getGoals()])
    else: return 0
def manhatthan(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)

def findNearestFruit(state):
    x,y = state.getPosition()
    nearest = sys.maxsize
    max_distance_goal = None
    for (xi, yi) in state.getGoals():
        distance = abs(xi - x) + abs(yi - y)
        if distance < nearest:
            nearest = distance
            max_distance_goal = (xi, yi)
    return max_distance_goal,nearest

def convinientPathHeuristic(state):
    if len(state.getGoals())>0 :
        (nearX,nearY),nearest = findNearestFruit(state)
        return nearest +  max([manhatthan(xi,yi,nearX,nearY) for (xi,yi) in state.getGoals()])
    else:
        return 0