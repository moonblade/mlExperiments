import pygame
from enum import Enum
import sys

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
        self.height = len(grid)
        self.width = len(grid[0])
        self.grid = [[Cell(x) for x in y] for y in grid]
    
    def getCell(self, posx, posy):
        return self.grid[posy][posx]               

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
        if graphic:
            pygame.init()
            self.screen = pygame.display.set_mode((self.grid.width*self.xScale, self.grid.height*self.yScale))
            self.images = {}
            for cell in Cell:
                if cell != Cell.empty:
                    self.images[cell] = self.transform(pygame.image.load('./images/'+cell.name+'.png'))

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
    
    def reset(self):
        self.end = False
        self.score = 0
        self.grid = Grid()
        self.mouse = Mouse(self.grid)

    def makeMove(self, direction):
        self.move(direction)
        if (self.end):
            print(self.score)
            self.reset()

    def move(self, direction):
        self.mouse.move(direction)
        self.test()
        return self.score


def main():
    game = Game()
    game.mainLoop()


if __name__ == "__main__":
    main()
    