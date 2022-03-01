from random import random

class Agent:

    CHANCE_TO_MUTATE = .05
    BINARY = False

    def __init__(self, x, y, memory, strategy=None):
        if (strategy and random() > self.CHANCE_TO_MUTATE):
            self.strategy = strategy
        else:
            self.strategy = random()
        self.x = x
        self.y = y
        self.life = 25
        self.memory = None
        if memory:
            self.memory = dict()
        self.reference = None

    def cooperate(self, opponent):
        strategy = self.strategy
        if self.memory is not None and opponent in self.memory:
            if self.memory[opponent]:
                strategy *= 1.5
            else:
                strategy /= 2

        if self.BINARY:
            return strategy > .5
        else:
            return strategy > random()

    def play(self, opponent):
        selfStrat = self.cooperate(opponent)
        opponentStrat = opponent.cooperate(self)

        if selfStrat and opponentStrat:
            self.life += 1
            opponent.life += 1

        elif selfStrat and not opponentStrat:
            self.life -= 10
            opponent.life += 5

        elif not selfStrat and opponentStrat:
            self.life += 5
            opponent.life -= 10

        else:
            self.life -= 2
            opponent.life -= 2

        if self.memory is not None:
            self.memory[opponent] = opponentStrat
            opponent.memory[self] = selfStrat

        return opponentStrat

    def die(self):
        if self.memory is not None:
            for agent in self.memory:
                if agent.memory is not None and self in agent.memory:
                    agent.memory.pop(self)
