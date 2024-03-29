from abc import ABC, abstractmethod
import heapq
import copy
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)
def printLoc(l):
    print("Explored:")
    for x in l:
        print(x.getPosition())

class Problem:
    def __init__(self,maze):
        self.P = dict()
        self.V = 0
        self.E = 0
        self.maze = maze
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x]==0 or self.maze[y][x]==1 or  self.maze[y][x]==2:
                    if (x,y) not in self.P: 
                        self.P[(x,y)] = []
                        self.V += 1
                    if x+1<len(self.maze[0]) and self.maze[y][x+1] != -1:
                        self.P[(x,y)].append(RIGHT)
                        self.E += 1
                    if x-1>0 and self.maze[y][x-1] != -1:
                        self.P[(x,y)].append(LEFT)
                        self.E += 1
                    if y-1>0 and self.maze[y-1][x] != -1:
                        self.P[(x,y)].append(UP)
                        self.E += 1
                    if y+1<len(self.maze) and self.maze[y+1][x] != -1:
                        self.P[(x,y)].append(DOWN)
                        self.E += 1
    def getMaze(self,curPos = None):
        if curPos:
            new_matrix = copy.deepcopy(self.maze)
            new_matrix[curPos[1]][curPos[0]] = 1
        else:
            new_matrix = copy.deepcopy(self.maze)
class State:
    def __init__(self,x,y,goals,cost=0,depth=0,action=None,par=None):
        self.action=action
        self.x = x
        self.y = y
        self.cost = cost
        self.depth = depth
        self.par=par
        self.goals = goals if ((x,y) not in goals) else [goal for goal in goals if goal != (x,y)]
    def getGoals(self):
        return self.goals
    def setCost(self,cost):
        self.cost = cost
    def getCost(self):
        return self.cost
    def getPathCost(self):
        return self.depth
    def isWin(self):
        return len(self.goals)==0
    def getNextState(self,action,cost=0):
        x_move,y_move = action
        return State(self.x+x_move,self.y+y_move,self.goals,cost,self.depth+1,action,self)
    def getPosition(self):
        return (self.x,self.y)
    def __lt__(self, nxt): 
        return (self.cost+self.depth) < (nxt.cost+nxt.depth)
    def __eq__(self,nxt):
        return self.x == nxt.x and self.y == nxt.y and self.goals == nxt.goals
    def __hash__(self):
        return hash((self.x,self.y,tuple(self.goals))) 
    def getAction(self):
        return self.action
class PacMan(ABC):
    def getState(self,action):
        return self.state.getNextState(action)
    @abstractmethod
    def getActions(self,state,goals):
        pass
class AStareAgent(PacMan):
    def __init__(self,heuristic):
        self.heuristic = heuristic
    def getActions(self,problem,startLocation,goals):
        start_loc = (startLocation[0],startLocation[1])
        if start_loc not in problem.P or problem.P[start_loc] == -1:
            print("Invalid input for problem!")
            return
        rtn = []
        start_state = State(start_loc[0],start_loc[1],goals)
        visited_states_set = set([])
        cost_of_states_dict = {start_state:0}
        frontier = [start_state]
        final_dest = start_state
        node_expanded = 0
        while len(frontier)>0 :
            head = heapq.heappop(frontier)
            if head in visited_states_set:
                continue
            else:
                node_expanded += 1
                visited_states_set.add(head)
                if head.isWin():
                    final_dest = head
                    break
                location = head.getPosition()
                if location in problem.P:
                    for action in problem.P[location]:
                        new_state = head.getNextState(action)
                        h_new_state = self.heuristic(new_state)
                        new_state.setCost(h_new_state)
                        if new_state in cost_of_states_dict:
                            if new_state.getPathCost() < cost_of_states_dict[new_state]:
                                cost_of_states_dict[new_state]=new_state.getPathCost()
                                heapq.heappush(frontier,new_state)
                        else:
                            cost_of_states_dict[new_state]=new_state.getPathCost()
                            heapq.heappush(frontier,new_state)
        if not final_dest.isWin():
            print("Goals unreachable!")
            return None, 0, node_expanded
        cost = final_dest.getPathCost()
        while final_dest!=start_state:
            rtn.append(final_dest.getAction())
            final_dest = final_dest.par
        return rtn[::-1],cost,node_expanded


class UCSAgent(PacMan):
   def getActions(self,problem,startLocation,goals):
        start_loc = (startLocation[0],startLocation[1])
        if start_loc not in problem.P or problem.P[start_loc] == -1:
            print("Invalid input for problem!")
            return
        rtn = []
        start_state = State(start_loc[0],start_loc[1],goals)
        visited_states_set = set([])
        cost_of_states_dict = {start_state:0}
        frontier = [start_state]
        final_dest = start_state
        node_expanded = 0
        while len(frontier)>0 :
            head = heapq.heappop(frontier)
            if head in visited_states_set:
                continue
            else:
                node_expanded += 1
                visited_states_set.add(head)
                if head.isWin():
                    final_dest = head
                    break
                location = head.getPosition()
                if location in problem.P:
                    for action in problem.P[location]:
                        new_state = head.getNextState(action,1+head.getCost())
                        if new_state in cost_of_states_dict:
                            if new_state.getPathCost() < cost_of_states_dict[new_state]:
                                cost_of_states_dict[new_state]=new_state.getPathCost()
                                heapq.heappush(frontier,new_state)
                        else:
                            cost_of_states_dict[new_state]=new_state.getPathCost()
                            heapq.heappush(frontier,new_state)
        cost = final_dest.getPathCost()
        while final_dest!=start_state:
            rtn.append(final_dest.getAction())
            final_dest = final_dest.par
        return rtn[::-1],cost,node_expanded
