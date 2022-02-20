import random
import tkinter
from math import floor
from agent import Agent
from model import Model
from view import View


class Game:

    def __init__(self):
        self.view = View(self)
        self.model = Model(self.view.numSq)
        self.view.window.mainloop()

    def createNewAgent(self, agent=None):
        if len(self.model.agents) >= self.view.maxAgents:
            return

        # create a new agent
        newPosition = (floor(random.random() * len(self.model.Positions)),
                        floor(random.random() * len(self.model.Positions[0])))
        newStrategy = None
        if agent:
            newPosition = random.sample(self.findAdj(agent, 1), 1)[0]
            newStrategy = agent.strategy
        newAgent = Agent(newPosition[0], newPosition[1], newStrategy)

        # find an empty position to place the agent
        while self.model.Positions[newAgent.x][newAgent.y]:
            newAgent.x = floor(random.random() * len(self.model.Positions))
            newAgent.y = floor(random.random() * len(self.model.Positions[0]))

        # determine color of agent and add it to the view
        colorval = '#%02x%02x%02x' % (floor(255 - (newAgent.strategy * 255)), floor(newAgent.strategy * 255), 0)
        newAgent.reference = self.view.displayNewAgent(newAgent, colorval)

        self.model.add(newAgent)

    def kill(self, agent):
        self.view.removeAgent(agent)
        self.model.remove(agent)

    def findAdj(self, agent, agentRange):
        emptyAdj = []
        # loop through all adjecent squares and find empty ones
        for i in range(agent.x - agentRange, agent.x + agentRange + 1):
            if i >= 0 and i < len(self.model.Positions):
                for j in range(agent.y - agentRange, agent.y + agentRange + 1):
                    if j >= 0 and j < len(self.model.Positions[i]):
                        if self.model.Positions[i][j] is None:
                            emptyAdj.append((i, j))

        # CASE: no empty adjacent squares -- try again with wider margin
        if len(emptyAdj) == 0:
            return self.findAdj(agent, agentRange + 1)

        return emptyAdj

    def gameLoop(self):
        while (1):
            while (len(self.model.agents) < 99):
                self.createNewAgent()

            # agents is copied because agents, a set, will change as members die
            for agent in self.model.agents.copy():
                # CASE: agent not in agents -- agent has died
                if agent not in self.model.agents:
                    continue

                # find all of the agent's neighbors
                neighbors = []
                for i in range(agent.x - 1, agent.x + 2):
                    if i >= 0 and i < len(self.model.Positions):
                        for j in range(agent.y - 1, agent.y + 2):
                            if j >= 0 and j < len(self.model.Positions[i]):
                                if self.model.Positions[i][j] and self.model.Positions[i][j] is not agent:
                                    neighbors.append(self.model.Positions[i][j])

                # if agent has no neighbors, move the agent, and continue
                if len(neighbors) < 1:
                    self.model.move(agent)
                    continue

                # choose a random neighbor as the opponent and play against it
                opponent = random.sample(neighbors, 1)[0]
                result = agent.play(opponent)

                if self.view.runaway.get() and not result:
                    self.model.move(agent)

                # determine if the agent or opponent die or multiply
                if agent.life <= 0:
                    self.kill(agent)
                elif agent.life >= 50:
                    self.createNewAgent(agent)
                    agent.life = 25
                if opponent.life <= 0:
                    self.kill(opponent)
                elif opponent.life >= 50:
                    self.createNewAgent(opponent)
                    opponent.life = 25

            # update the view
            self.view.updateView(self.model.agents)


if __name__ == "__main__":
    game = Game()