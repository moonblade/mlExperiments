#!/usr/local/bin/python
import random

debug = True
class Grid:
    CAT = 1
    CHEESE = 2
    EMPTY = 0
    def __init__(self):
        self.grid = []
        with open("grid.txt") as f:
            for line in f:
                self.grid.append([int(x) for x in line.strip().split()])
    
    def get(self, position):
        return self.grid[position[0]][position[1]]

class Mouse:
    def __init__(self, grid):
        self.grid = grid
        self.directions = [0, 1, 2, 3]
        self.alive = True
        self.matrix = [[self.getMat2((y,x)) for x in range(len(grid.grid[0]))] for y in range(len(grid.grid))]
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])
        self.position = (0,0)
        self.prev = (0, 0)
        self.alpha = 0.5
        self.noOfMoves = 0
        self.score = 100
        self.decay = 0.9
    
    def setAlpha(self, num):
        self.alpha = num

    def getMat(self, pos):
        if self.grid.get(pos) == Grid.EMPTY:
            return 0
        if self.grid.get(pos) == Grid.CAT:
            return -1000
        if self.grid.get(pos) == Grid.CHEESE:
            return 1000
        
    def getNearby(self):
        p = []
        for x in [-1, 1]:
                p.append((self.position[0]+x, self.position[1], [-1, 1].index(x)))
        for y in [-1,1]:
                p.append((self.position[0], self.position[1]+y, [-1,1].index(y)+2))
        p = list(filter(lambda x: x[0]>=0 and x[0]<self.rows and x[1]>=0 and x[1]<self.columns, p))
        return p

    def pprint(self):
        if debug:
            # for p in self.grid.grid:
            #     print p
            # print

            for p in self.matrix:
                print p
            print

    def reset(self):
        self.score = 100
        self.noOfMoves = 0
        self.position = (0,0)
        self.alive = True

    def set(self, pos, reward):
        # data = self.matrix[pos[0]][pos[1]] * (1 - self.alpha) + self.alpha * ( self.decay * self.get(self.position) + reward)
        nextMax = self.getMax()
        data = self.matrix[pos[0]][pos[1]] * (1 - self.alpha) + self.alpha * (reward + self.decay * nextMax)
        print(self.matrix[pos[0]][pos[1]], self.alpha, self.decay, self.get(self.position), data)
        self.matrix[pos[0]][pos[1]] = data

    def get(self, position):
        return self.matrix[position[0]][position[1]]

    def getMax(self):
        p = self.getNearby()
        matrix = [self.get(x) for x in p]
        return max(matrix)

    def correctMove(self):
        p = self.getNearby()
        matrix = [self.get(x) for x in p]
        dir = p[matrix.index(max(matrix))][2]
        self.move(dir)

    def makeMove(self):
        if random.random() > self.alpha:
            self.moveRandom()
        else:
            self.correctMove()

    def bypass(self):
        # self.matrix = [[946, -569, 1691, -1036, 1552],[-1000, -1000, -439, -1000, -626],[0, -1000, 6583, -885, -1000],[1000, 8810, -1000, 2530, -1125],[9295, -262, 1336, -1000, 1846, -1000, 0, 1110, 20591]]
        # self.pprint()
        pass

    def path(self):
        self.bypass()
        y = 10
        self.position = (0,0)
        while y > 0 and self.grid.get(self.position)!=Grid.CHEESE: 
            p = self.getNearby()
            matrix = [self.get(x) for x in p]
            dir = p[matrix.index(max(matrix))]
            self.position = (dir[0], dir[1])
            print(self.position)
            y -= 1 
        

    def moveRandom(self):
        dir = [x for x in self.directions]
        if (self.position[0]==0):
            dir.remove(0)
        if (self.position[1]==0):
            dir.remove(2)
        if (self.position[0]==self.rows-1):
            dir.remove(1)
        if (self.position[1]==self.columns-1):
            dir.remove(3)
        self.move(random.choice(dir))

    # 0-3
    def move(self, direction):
        if not self.alive:
            return
        self.noOfMoves += 1
        dirx = 0
        diry = 0
        if (direction<2):
            dirx = -1 if direction==0 else 1
        if (direction>=2):
            diry = -1 if direction==2 else 1
        self.prev = self.position
        self.position = (self.position[0] + dirx, self.position[1] + diry)
        self.check()
        self.pprint()
    
    def check(self):
        reward = self.getMat(self.position)
        if (grid.get(self.position) == Grid.CAT):
            self.alive = False
            self.score -= 1000
        if (grid.get(self.position) == Grid.CHEESE):
            self.alive = False
            self.score += 1000
        self.set(self.prev, reward)
        


if __name__ == "__main__":
    grid = Grid()
    m = Mouse(grid)
    epoch = 100
    perEpoch = 1000
    for x in range(epoch):
        for y in range(perEpoch):
            m.makeMove()
            if (not m.alive):
                m.reset()
        m.setAlpha(min(1, m.alpha + 1.0/epoch))
    m.path()