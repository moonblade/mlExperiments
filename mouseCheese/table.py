from game import Game, Direction
import pickle
import random

class Brain:
    def __init__(self, game, epoch=100000):
        self.alpha = 0.1
        self.epsilon = 0.01
        self.gamma = 0.9
        self.qtable = {}
        self.curEpoch = 0
        self.epoch = epoch
        self.game = game
        self.lastScore = game.score

    def play(self):
        for epoch in range(self.epoch):
            self.step()
        pickle.dump(self.qtable, open("temp", "w"))

    def step(self):
        move = self.findMove()
        state = self.game.getStateString()
        self.game.move(move)
        self.updateQval(state, move, self.game.score - self.lastScore)
        self.lastScore = self.game.score
        self.curEpoch += 1
        self.updateEpsilon()
        if self.game.end:
            print(self.game.score)
            self.game.reset()
    
    def updateEpsilon(self):
        if self.curEpoch%(self.epoch/100)==0:
            self.epsilon += 0.01
    def findMaxReward(self):
        if self.game.end:
            return self.game.score
        qvals = self.getQValues(self.game.getStateString())
        return max(qvals)

    def updateQval(self, state, move, delScore):
        if not state in self.qtable:
            self.qtable[state] = [0,0,0,0]
        self.qtable[state][move] =  self.qtable[state][move] + self.alpha*(delScore + self.gamma*(self.findMaxReward()) - self.qtable[state][move])

    def findMove(self):
        if (random.random() < self.epsilon):
            # good move
            state = self.game.getStateString()
            qvals = self.getQValues(state)
            # dirs = self.game.getValidMoves()
            # maxv = -float('inf')
            # maxd = dirs[0]
            # for dir in dirs:
            #     if qvals[int(dir)] > maxv:
            #         maxv = qvals[int(dir)]
            #         maxd = dir
            # return maxd
            return Direction(qvals.index(max(qvals)))
        else:
            # random move
            return random.choice(self.game.getValidMoves())

    def getQValues(self, state):
        if state not in self.qtable:
            self.qtable[state]=[0,0,0,0]
        return self.qtable[state]

    def qtableString(self):
        return ';'.join([str(state)+':' + ' '.join(map(str,self.qtable[state])) for state in self.qtable])

def main():
    game = Game(False)
    brain = Brain(game)
    brain.play()
    pass

if __name__ == "__main__":
    main()