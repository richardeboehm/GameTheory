import random


class Board:

    def __init__(self, size):
        #initialized with a 2-d array
        self.Positions = []
        for i in range(size):
            self.Positions.append([])
            for j in range(size):
                self.Positions[i].append(None)

    def add(self, agent):
        self.Positions[agent.x][agent.y] = agent

    def remove(self, agent):
        self.Positions[agent.x][agent.y] = None

    def findAdj(self, agent, agentRange):
        emptyAdj = []
        # loop through all adjecent squares and find empty ones
        for i in range(agent.x - agentRange, agent.x + agentRange + 1):
            if i >= 0 and i < len(self.Positions):
                for j in range(agent.y - agentRange, agent.y + agentRange + 1):
                    if j >= 0 and j < len(self.Positions[i]):
                        if self.Positions[i][j] is None:
                            emptyAdj.append((i, j))

        if not emptyAdj:
            emptyAdj = [(agent.x, agent.y)]
        return emptyAdj

    def move(self, agent):
        emptyAdj = self.findAdj(agent, 1)
        self.remove(agent)
        newPosition = random.sample(emptyAdj, 1)[0]
        agent.x = newPosition[0]
        agent.y = newPosition[1]
        self.add(agent)
