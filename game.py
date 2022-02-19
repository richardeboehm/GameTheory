import random
import tkinter
from math import floor
from agent import Agent
from board import Board
from view import View


class Game:

    def __init__(self):
        self.view = View(self)
        self.board = Board(self.view.numSq)
        self.agents = set()
        self.view.window.mainloop()

    def createNewAgent(self, agent=None):
        if len(self.agents) >= self.view.maxAgents:
            return

        # create a new agent
        newPosition = (floor(random.random() * len(self.board.Positions)),
                        floor(random.random() * len(self.board.Positions[0])))
        newStrategy = None
        if agent:
            newPosition = random.sample(self.findAdj(agent, 1), 1)[0]
            newStrategy = agent.strategy
        newAgent = Agent(newPosition[0], newPosition[1], newStrategy)

        # find an empty position to place the agent
        while self.board.Positions[newAgent.x][newAgent.y]:
            newAgent.x = floor(random.random() * len(self.board.Positions))
            newAgent.y = floor(random.random() * len(self.board.Positions[0]))

        # determine color of agent and add it to the view
        colorval = '#%02x%02x%02x' % (floor(255 - (newAgent.strategy * 255)), floor(newAgent.strategy * 255), 0)
        newAgent.reference = self.view.displayNewAgent(newAgent, colorval)

        self.board.add(newAgent)
        self.agents.add(newAgent)

    def kill(self, agent):
        self.view.removeAgent(agent)
        self.board.remove(agent)
        self.agents.remove(agent)
        agent.die()

    def findAdj(self, agent, agentRange):
        emptyAdj = []
        # loop through all adjecent squares and find empty ones
        for i in range(agent.x - agentRange, agent.x + agentRange + 1):
            if i >= 0 and i < len(self.board.Positions):
                for j in range(agent.y - agentRange, agent.y + agentRange + 1):
                    if j >= 0 and j < len(self.board.Positions[i]):
                        if self.board.Positions[i][j] is None:
                            emptyAdj.append((i, j))

        # CASE: no empty adjacent squares -- try again with wider margin
        if len(emptyAdj) == 0:
            return self.findAdj(agent, agentRange + 1)

        return emptyAdj

    def gameLoop(self):
        while (1):
            while (len(self.agents) < 50):
                self.createNewAgent()

            # agents is copied because agents, a set, will change as members die
            for agent in self.agents.copy():
                # CASE: agent not in agents -- agent has died
                if agent not in self.agents:
                    continue

                # find all of the agent's neighbors
                neighbors = []
                for i in range(agent.x - 1, agent.x + 2):
                    if i >= 0 and i < len(self.board.Positions):
                        for j in range(agent.y - 1, agent.y + 2):
                            if j >= 0 and j < len(self.board.Positions[i]):
                                if self.board.Positions[i][j] and self.board.Positions[i][j] is not agent:
                                    neighbors.append(self.board.Positions[i][j])

                # if agent has no neighbors, move the agent, and continue
                if len(neighbors) < 1:
                    self.board.move(agent)
                    continue

                # choose a random neighbor as the opponent and play against it
                opponent = random.sample(neighbors, 1)[0]
                agent.play(opponent)

                if self.view.runaway.get():
                    if not agent.memory[opponent]:
                        self.board.move(agent)
                    if not opponent.memory[agent]:
                        self.board.move(opponent)

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
            self.view.updateBoard(self.agents)


if __name__ == "__main__":
    game = Game()