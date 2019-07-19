import pygame
from enum import IntEnum
import sys
import os
import numpy as np
import time

class Cell(IntEnum):
    empty=0
    mouse=1
    cat=2
    cheese=3
    smallCheese=4

class Direction(IntEnum):
    up=0
    down=1
    left=2
    right=3

class Grid:
    def __init__(self):
        grid = [[0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 2, 0], [2, 0, 0, 3]]
        self.height = len(grid)
        self.width = len(grid[0])
        self.grid = [[Cell(x) for x in y] for y in grid]
    
    def updateCell(self, posx, posy, cell):
        self.grid[posx][posy] = cell

    def getCell(self, posx, posy):
        return self.grid[posy][posx]               

class Mouse:
    def __init__(self, grid):
        self.posx = 0
        self.posy = 0
        self.grid = grid
        self.alive = True
        self.hasCheese = False
        self.hasSmallCheese = False
    
    def updateState(self):
        cell = self.grid.getCell(self.posx, self.posy)
        if cell == Cell.cat:
            self.alive = False
        if cell == Cell.cheese:
            self.hasCheese = True
        if cell == Cell.smallCheese:
            self.hasSmallCheese = True
            self.grid.updateCell(self.posx, self.posy, Cell.empty)

    def whatIfMove(self, direction):
        self.saveClass = self.__dict__
        self.move(direction)
    
    def rollBack(self):
        self.__dict__.update(self.saveClass)
    
    def getValidMoves(self):
        moves = []
        if self.posx>0:
            moves.append(Direction.left)
        if self.posx<self.grid.width-1:
            moves.append(Direction.right)
        if self.posy>0:
            moves.append(Direction.up)
        if self.posy<self.grid.height-1:
            moves.append(Direction.down)
        return moves     

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
        
class Color:
    white=(255,255,255)
    black=(0,0,0)

class Game:
    def __init__(self, graphic=True):
        self.grid = Grid()
        self.mouse = Mouse(self.grid)
        self.score = 0
        self.end = False
        self.graphic = graphic
        self.xScale = 100
        self.yScale = 100
        self.curStep = 0
        if graphic:
            pygame.init()
            self.screen = pygame.display.set_mode((self.grid.width*self.xScale, self.grid.height*self.yScale))
            self.images = {}
            for cell in Cell:
                if cell != Cell.empty:
                    self.images[cell] = self.transform(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/'+cell.name+'.png'))

    def getValidMoves(self):
        return self.mouse.getValidMoves()

    def transform(self, surface):
        return pygame.transform.scale(surface, (self.xScale-5, self.yScale-5))

    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.makeMove(Direction.left)
                    if event.key == pygame.K_RIGHT:
                        self.makeMove(Direction.right)
                    if event.key == pygame.K_UP:
                        self.makeMove(Direction.up)
                    if event.key == pygame.K_DOWN:
                        self.makeMove(Direction.down)
                if event.type == pygame.QUIT: sys.exit()
            self.display()

    def display(self):
        if self.graphic:
            self.screen.fill(Color.white)
            state = self.getState()
            for x in range(self.grid.width):
                for y in range(self.grid.height):
                    pygame.draw.rect(self.screen, Color.black, (x*self.xScale,y*self.yScale,self.xScale,self.yScale), 1)
                    if (state[y][x] != Cell.empty):
                        self.screen.blit(self.images[state[y][x]],(x*self.xScale,y*self.yScale))
            pygame.display.update()
            time.sleep(0.1)

    def getStateString(self):
        # print(self.mouse.posx + self.mouse.posy * self.grid.height)
        # print("{0:b}".format(self.mouse.posx + self.mouse.posy * self.grid.height))
        # print(tuple("{0:b}".format(self.mouse.posx + self.mouse.posy * self.grid.height).zfill(4)))
        return np.array(list("{0:b}".format(self.mouse.posx + self.mouse.posy * self.grid.height).zfill(4))).astype(np.float)
        # return self.mouse.posx + self.mouse.posy * self.grid.height

    def getState(self):
        temp = [[x for x in y] for y in self.grid.grid]
        temp[self.mouse.posy][self.mouse.posx] = Cell.mouse
        return temp
    
    def test(self):
        if self.mouse.alive:
            self.score += 1
        else:
            self.score -= 1000
            self.end = True
        if self.mouse.hasCheese:
            self.score += 1000
            self.end = True    
        if self.mouse.hasSmallCheese:
            self.score += 100
            self.mouse.hasSmallCheese = False
        if self.curStep > 200:
            self.end = True
    
    def reset(self):
        self.end = False
        self.score = 0
        self.curStep = 0
        self.grid = Grid()
        self.mouse = Mouse(self.grid)
        return self.getStateString()

    def makeMove(self, direction):
        self.move(direction)
        if (self.end):
            self.reset()

    def whatIfMove(self, direction):
        # returns delscore
        self.mouse.whatIfMove(direction)
        score = 0
        if not self.mouse.alive:
            score -= 1000
        elif self.mouse.hasCheese:
            score += 1000
        else:
            score -= 1
        self.mouse.rollBack()
        return score

    def move(self, direction):
        self.curStep += 1
        self.mouse.move(direction)
        self.test()
        self.display()
        return self.score

    def render(self, mode):
        self.display()

    def step(self, action):
        self.move(action)
        return self.getStateString(), self.score, self.end, {}

def main():
    game = Game(False)
    # game.mainLoop()
    game.getStateString()


if __name__ == "__main__":
    main()
    