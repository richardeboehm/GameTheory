from random import random


class Agent:

    def __init__(self, canvas, x, y, strategy=None):
        if (strategy and random() > .05):
            self.strategy = strategy
        else:
            self.strategy = random()
        self.x = x
        self.y = y
        self.life = 25
        self.canvas = canvas
        self.reference = None
        self.memory = {}

    def cooperate(self, opponent):
        strategy = self.strategy
        if opponent in self.memory:
            if self.memory[opponent]:
                strategy *= 1.5
            else:
                strategy /= 2
        return random() < strategy

    def play(self, opponent):
        selfStrat = self.cooperate(opponent)
        opponentStrat = opponent.cooperate(self)

        self.memory[opponent] = opponentStrat
        opponent.memory[self] = selfStrat

        if selfStrat and opponentStrat:
            self.life += 1
            opponent.life += 1

        elif selfStrat and not opponentStrat:
            self.life -= 15
            opponent.life += 10

        elif not selfStrat and opponentStrat:
            self.life += 10
            opponent.life -= 15

        else:
            self.life -= 1
            opponent.life -= 1

    def die(self):
        for agent in self.memory:
            agent.memory.pop(self)
