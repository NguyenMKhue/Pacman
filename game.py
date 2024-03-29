from time import sleep
from pacman import *
import os
import copy
from heuristic import *
class GameManager:
    def __init__(self):
        self.gameMap = None
        self.curPos = None
    def extract_maze(self, maze_data: str):
        maze = []
        loc = None
        goals = []
        maze_mat = maze_data.split('\n')
        corners = {(1,1), (1, len(maze_mat)-2), (len(maze_mat[0])-2, 1), (len(maze_mat[0])-2, len(maze_mat)-2)}
        for line_idx, line in enumerate(maze_mat):
            row = []
            for col_idx, char in enumerate(line):
                if char == '#':
                    row.append(-1)
                elif char == ' ':
                    row.append(0)
                elif char == '.':
                    row.append(2)
                    goals.append((col_idx, line_idx))
                elif char == 'P':
                    row.append(1)
                    loc = (col_idx,line_idx)
                if (col_idx,line_idx) in corners and maze_mat[line_idx][col_idx] == ' ':
                    goals.append((col_idx, line_idx))
            maze.append(row)
        return maze, loc, goals
    
    def initialize(self):
        maze_name = input("Enter the maze file name: ")
        with open(f"input/{maze_name}.txt", 'r') as file:
            maze_data = file.read()
        
        maze, loc, goals = self.extract_maze(maze_data)
        problem = Problem(maze)
        self.gameMap = maze
        self.curPos = copy.deepcopy(loc)
        self.run(loc,goals,problem)
    
    def draw(self):
        for row in self.gameMap:
            for cell in row:
                if cell == -1:
                    print('#', end='')
                elif cell == 0:
                    print(' ', end='')
                elif cell == 1:
                    print('P', end='')
                elif cell == 2:
                    print('.', end='')
            print()
        pass
    def updateGameMap(self,action):
        x,y = self.curPos
        self.gameMap[y][x] = 0
        self.gameMap[y+action[1]][x+action[0]] = 1
        self.curPos = (x+action[0],y+action[1])
    def run(self,start,goals,problem):
        search_algo = input("Enter the search algorithm \n1. UCS\n2. A*\n")
        if (search_algo=='1'):
            pacman = UCSAgent()
        else:
            pacman = AStareAgent(convinientPathHeuristic)
        self.clear()
        self.draw()
        sleep(0.75)
        # actions, cost = self.pacman.getAction(self.state, self.state.goals)
        #actions = [UP,LEFT,DOWN,RIGHT,RIGHT,RIGHT,UP,UP] # test
        actions,cost,node_expanded = pacman.getActions(problem,start,goals)
        if actions is None:
            print("No path found!")
            print(f'\nNodes expanded: {node_expanded}')
            return
        while len(actions) > 0:
            self.clear()
            action = actions.pop(0)
            self.updateGameMap(action)
            self.draw()
            sleep(0.001)
        print('\n------------------------------\n')
        print(f'Path Found by Pacman Agent: "{pacman.__class__.__name__}"\n')
        print('Path cost: ',cost)
        print(f'\nNodes expanded: {node_expanded}')
        print('\n------------------------------\n')
    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:  
            os.system('clear')
        
game = GameManager()
game.initialize()
    
