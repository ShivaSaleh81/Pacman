import random
import math
import time
import copy 
import networkx as nx
import os
from collections import deque
from queue import Queue


def printGame(pac, gh1, gh2, m):
    print("******************************************************************")
    for i in range(0,rows) :
        for j in range(0, cols) :            
            if i == ghost1.x and j == ghost1.y :
                print (" g ",end="")
            elif i == ghost2.x and j == ghost2.y :
                print (" g ",end="")
            elif i == pacman.x and j == pacman.y :
                print (" p ",end="")
            else :
                if matrix[i][j] == 1 :
                    print (" . ",end="")
                elif matrix[i][j] == 0 :
                    print ( "   ",end="")
                elif matrix[i][j] == -1 :
                    print(" # ",end="")
        print()
    print("******************************************************************")


cols=18
rows=9
matrix=[[0]*cols for i in range(rows)]

matrix = [
     [1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1],
     [1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1],
     [1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1],
     [1, -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1],
     [1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1],
     [1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1],
     [1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1],
     [1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1],
     [1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1],
]

# def bestScore1(matrix ,pacman, ghost1, ghost2):
#     dis1 = math.sqrt((ghost1.x - pacman.x)**2 +( ghost1.y - pacman.y)**2)
#     dis2 = math.sqrt((ghost2.x - pacman.x)**2 +( ghost2.y - pacman.y)**2)
#     return min(dis1, dis2)

def bestScore2(matrix ,pacman, ghost1, ghost2):
    graph = nx.Graph()

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != -1:
                graph.add_node((i, j))
                if i > 0 and matrix[i - 1][j] != -1:
                    graph.add_edge((i, j), (i - 1, j))
                if i < len(matrix) - 1 and matrix[i + 1][j] != -1:
                    graph.add_edge((i, j), (i + 1, j))
                if j > 0 and matrix[i][j - 1] != -1:
                    graph.add_edge((i, j), (i, j - 1))
                if j < len(matrix[i]) - 1 and matrix[i][j + 1] != -1:
                    graph.add_edge((i, j), (i, j + 1))
 

    dis_score = float('inf')
    visited = set()

    def bfs(graph, start, end):
        queue = Queue()
        queue.put(start)
        visited.add(start)

        while not queue.empty():
            current_node = queue.get()

            if current_node == end:
                return True

            for neighbor in graph.neighbors(current_node):
                if neighbor not in visited:
                    queue.put(neighbor)
                    visited.add(neighbor)

        return False

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                has_path = bfs(graph, (pacman.x, pacman.y), (i, j))
                
                if has_path:
                    dis_food = nx.shortest_path_length(graph, (pacman.x, pacman.y), (i, j))
                    if dis_food < dis_score:
                        dis_score = dis_food

    score = ((20.1 - dis_score) / 20.1) * 9

    dis1 = nx.shortest_path_length(graph,(pacman.x, pacman.y), (ghost1.x, ghost1.y))
    dis2 = nx.shortest_path_length(graph,(pacman.x, pacman.y), (ghost2.x, ghost2.y))

    if min(dis1,dis2) < 5 :
        score *= -1

    return score


def minimax (currentDepth, targetDepth, matrix, pacman, ghost1, ghost2, isMaximizing):

    if currentDepth == targetDepth :
        return bestScore2(matrix,pacman, ghost1, ghost2)
    
    if isMaximizing == 0 :
        best_move = -1
        best_score = float('-inf')
        for i in range(1 , 5) :
            if isValid(matrix , pacman.x, pacman.y, i) != -1 :

                currentPacmanX = pacman.x
                currentPacmanY = pacman.y

                futurePacmanX , futurePacmanY = isValid(matrix , pacman.x, pacman.y, i)
                pacman.x , pacman.y = futurePacmanX, futurePacmanY

                food = matrix[pacman.x][pacman.y]

                score = minimax(currentDepth, targetDepth, matrix, pacman, ghost1, ghost2, 1) 
                pacman.x, pacman.y = currentPacmanX, currentPacmanY
                # matrix[pacman.x][pacman.y] = food
                if score > best_score :
                    best_score = score 
                    best_move = i

        if currentDepth == 0 :
            tempX, tempY =  isValid(matrix , pacman.x, pacman.y, best_move) 
            matrix[tempX][tempY] = 0
            pacman.x, pacman.y = tempX, tempY
            if matrix[tempX][tempY] == 1:
                matrix[tempX][tempY] = 0
                print(matrix[tempX][tempY])
                pacman.x, pacman.y = tempX, tempY
                print(matrix[tempX][tempY])
                
            return tempX, tempY
        else :
            return best_score

    elif isMaximizing == 1 :
        best_score = float('inf')
        for i in range(1 , 5) :
            if isValid(matrix , ghost1.x, ghost1.y, i) != -1 :

                currentGhost1X = ghost1.x
                currentGhost1Y = ghost1.y

                futureGhost1X , futureGhost1Y = isValid(matrix , ghost1.x, ghost1.y, i)

                ghost1.x , ghost1.y = futureGhost1X, futureGhost1Y

                score = minimax(currentDepth, targetDepth, matrix, pacman, ghost1, ghost2, 2) 

                ghost1.x, ghost1.y = currentGhost1X, currentGhost1Y

                if score < best_score :
                    best_score = score

        return best_score
    
    elif isMaximizing == 2 :
        best_score = float('inf')
        for i in range(1 , 5) :
            if isValid(matrix , ghost2.x, ghost2.y, i) != -1 :

                currentGhost2X = ghost2.x
                currentGhost2Y = ghost2.y

                futureGhost2X , futureGhost2Y = isValid(matrix , ghost2.x, ghost2.y, i)

                ghost2.x , ghost2.y = futureGhost2X, futureGhost2Y

                score = minimax(currentDepth + 1, targetDepth, matrix, pacman, ghost1, ghost2, 0) 

                ghost2.x, ghost2.y = currentGhost2X, currentGhost2Y

                if score < best_score :
                    best_score = score
        
        return best_score


    
def isValid (matrix, x , y, move) :
    if move == 1 and y + 1 < 18 and matrix[x][y+1] != -1:
        return x, y+1
    elif move == 2 and x + 1 < 9 and matrix[x+1][y] != -1 :
        return x+1, y
    elif move == 3 and y - 1 > -1 and matrix[x][y-1] != -1 :
        return x, y-1
    elif move == 4 and x - 1 > -1 and matrix[x-1][y] != -1 :
        return x-1, y
    else :
        return -1 


class Pacman:
    
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.score = 0


class Ghost:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def change_loc(self, move_command):

        if move_command == 1 and self.y + 1 < 18 and matrix[self.x][self.y+1] != -1:
            self.y += 1
        elif move_command == 2 and self.x + 1 < 9 and matrix[self.x+1][self.y] != -1:
            self.x += 1
        elif move_command == 3 and self.y - 1 > -1 and matrix[self.x][self.y-1] != -1:
            self.y -= 1
        elif move_command == 4 and self.x - 1 > -1 and matrix[self.x-1][self.y] != -1:
            self.x -= 1

        

pacman = Pacman(x=4, y=1) 
ghost1 = Ghost(x=0, y=0)
ghost2 = Ghost(x=8, y=17)

currentdepth = 0
i = 0
while True:
    printGame(pacman, ghost1, ghost2, matrix)
    # print(minimax(currentdepth, 1, matrix, pacman ,ghost1 , ghost2, 0))
    pacman.x , pacman.y = minimax(currentdepth, 1, matrix, pacman ,ghost1 , ghost2, 0)
    ghost1.change_loc(random.randint(1, 5))
    ghost2.change_loc(random.randint(1, 5))

    

    if (pacman.x == ghost1.x and pacman.y == ghost1.y ) or (pacman.x == ghost2.x and pacman.y == ghost2.y) :
        print(' pacman lose! ')
        break
    
    count = 0

    for i in range(9):
        for j in range(18) :
            if matrix[i][j] != 1 :
                count += 1

    if count == 9 * 18 :
        print(' pacman win! ')
        break

    t = 0.5
    time.sleep(t)
    i += 1
    # os.system("cls")