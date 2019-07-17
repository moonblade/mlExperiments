from game import Game

class Table:
    def __init__(self, epoch=1000):
        self.alpha = 0.1
        self.epsilon = 0.01
        self.gamma = 0.9
        self.qtable = {}

    def getQValues(self, state):
        if state not in self.qtable:
            self.qtable[state]=[0,0,0,0]
        return self.qtable[state]
            
def main():
    table = Table()
    game = Game(False)
    print(table.getQValues(game.getStateString()))
    print(game.whatIfMove(1))
    pass

if __name__ == "__main__":
    main()