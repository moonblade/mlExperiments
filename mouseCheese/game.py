import pygame
from enum import Enum

class Cell(Enum):
    empty=0
    mouse=1
    cat=2
    cheese=3

class Direction(Enum):
    up=0
    down=1
    left=2
    right=3

class Grid:
    def __init__(self):
        grid = [[0, 0, 0, 0], [2, 0, 2, 0], [0, 0, 2, 2], [2, 0, 0, 3], [2,2,2,2]]
        height = len(grid)
        width = len(grid[0])
        self.grid = [[Cell(x) for x in y] for y in grid]
    
    def getCell(self, posx, posy):
        return self.grid[posx][posy]

class Mouse:
    def __init__(self, grid):
        self.posx = 0
        self.posy = 0
        self.grid = grid
        self.alive = True
        self.hasCheese = False
    
    def updateState(self):
        cell = self.grid.getCell(self.posx, self.posy)
        if cell == Cell.cat:
            self.alive = False
        if cell == Cell.cheese:
            self.hasCheese = True

    def move(self, direction):
        if direction == Direction.left and self.posx>0:
            self.posx-=1
        if direction == Direction.right and self.posx<self.grid.width-1:
            self.posx+=1
        if direction == Direction.up and self.posy>0:
            self.posy-=1
        if direction == Direction.down and self.posy<self.grid.height-1:
            self.posy+=1
        self.updateState()
        


class Game:
    def __init__(self):
        self.grid = Grid()
        self.mouse = Mouse(self.grid)
        self.score = 0
        self.end = False
    
    def getState(self):
        temp = self.grid.grid[:]
        temp[self.mouse.posx][self.mouse.posy] = Cell.mouse
    
    def test(self):
        if self.mouse.alive:
            self.score += 1
        else:
            self.end = True
        if self.mouse.hasCheese:
            self.score += 1000        
    
    def reset(self):
        self.end = False
        self.score = 0
        self.grid = Grid()
        self.mouse = Mouse(self.grid)

    def move(self, direction):
        self.mouse.move(direction)
        self.test()


def main():
    Game()

if __name__ == "__main__":
    main()
    