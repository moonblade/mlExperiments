from game import Game

class Table:
    def __init__(self):
        self.alpha = 0.1
        self.gamma = 0.9
        self.qtable = {}

    def getQValues(self, state):
        if state not in self.qtable:
            self.qtable[state]=[0,0,0,0]
        return self.qtable[state]
            
def main():
    table = {}
    game = Game()
    game.getStateString()
    pass

if __name__ == "__main__":
    main()