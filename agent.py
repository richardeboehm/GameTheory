from random import random

class Agent:

    # Probability that a new agent mutates from its parent's strategy
    CHANCE_TO_MUTATE = .05

    def __init__(self, x, y, strategy=None):
        if (strategy and random() > self.CHANCE_TO_MUTATE):
            self.strategy = strategy
        else:
            self.strategy = random()
        self.x = x
        self.y = y
        self.life = 25
        self.reference = None

    def cooperate(self, opponent):
        return self.strategy > .5

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

        return opponentStrat

    def die(self):
        del self
