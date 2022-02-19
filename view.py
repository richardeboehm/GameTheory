import tkinter
from math import floor
from agent import Agent
from board import Board

class View:

    def __init__(self, game):
        self.game = game
        self.numSq = 175;
        self.boardSize = 525
        self.maxAgents = 6000
        self.total = 0
        #set up the canvas
        self.window = tkinter.Tk()
        self.window.title("gameTheory.py")
        self.canvas = tkinter.Canvas(self.window, width=self.game.boardSize, height=self.game.boardSize, bg='gray')
        self.canvas.pack()
        self.runawayButton = tkinter.BooleanVar()
        tkinter.Checkbutton(self.window, text="Runaway", command=self.game.changeRunaway).pack()
        tkinter.Button(self.window, text="START", command=lambda:self.game.gameLoop(self.canvas)).pack()

    def multiply(self, agent):
        # CASE: maxAgents reached -- don't multiply
        if len(self.agents) >= self.maxAgents:
            agent.life = 25
            return

        # cut life in half and create new agent
        agent.life = 25
        emptyAdj = self.findAdj(agent, 1)
        newPosition = random.sample(emptyAdj, 1)[0]
        newAgent = Agent(agent.canvas, newPosition[0], newPosition[1])

        # five percent chance that new agent mutates to new strategy
        if random.random() > .01:
            newAgent.strategy = agent.strategy

        # determine color of agent and draw it on the canvas
        self.addAgent(newAgent)
        colorval = '#%02x%02x%02x' % (floor(255 - (newAgent.strategy * 255)), floor(newAgent.strategy * 255), 0)
        newAgent.reference = canvas.create_oval(newAgent.x * self.boardSize/self.numSq,
                                                newAgent.y * self.boardSize/self.numSq,
                                                newAgent.x * self.boardSize/self.numSq + self.boardSize/self.numSq,
                                                newAgent.y * self.boardSize/self.numSq + self.boardSize/self.numSq,
                                                fill=colorval)

    def updateBoard(self, canvas, agents):
        # redraw all agents and update the canvas
        for agent in agents:
            canvas.coords(agent.reference,
                        agent.x * self.boardSize/self.numSq,
                        agent.y * self.boardSize/self.numSq,
                        agent.x * self.boardSize/self.numSq + self.boardSize/self.numSq,
                        agent.y * self.boardSize/self.numSq + self.boardSize/self.numSq)
        canvas.update()

