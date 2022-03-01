import tkinter
from math import floor
from agent import Agent

class View:

    def __init__(self, game, changeBinary, changeMemory):
        self.game = game
        self.numSq = 175;
        self.boardSize = 525
        self.maxAgents = 1500
        self.total = 0
        #set up the canvas
        self.window = tkinter.Tk()
        self.window.title("gameTheory.py")
        self.canvas = tkinter.Canvas(self.window, width=self.boardSize, height=self.boardSize, bg='#444444')
        self.canvas.pack()
        self.runaway = tkinter.BooleanVar()
        self.memory = tkinter.BooleanVar()
        tkinter.Checkbutton(self.window, text="Runaway", variable=self.runaway).pack()
        tkinter.Checkbutton(self.window, text="Binary", command=changeBinary).pack()
        tkinter.Checkbutton(self.window, text="Memory", variable=self.memory, command=changeMemory).pack()
        tkinter.Button(self.window, text="START", command=self.game.gameLoop).pack()

    def displayNewAgent(self, newAgent, colorval):
        return self.canvas.create_oval(newAgent.x * self.boardSize/self.numSq,
                                    newAgent.y * self.boardSize/self.numSq,
                                    newAgent.x * self.boardSize/self.numSq + self.boardSize/self.numSq,
                                    newAgent.y * self.boardSize/self.numSq + self.boardSize/self.numSq,
                                    fill=colorval)

    def removeAgent(self, agent):
        self.canvas.delete(agent.reference)

    def updateView(self, agents):
        # redraw all agents and update the canvas
        for agent in agents:
            self.canvas.coords(agent.reference,
                        agent.x * self.boardSize/self.numSq,
                        agent.y * self.boardSize/self.numSq,
                        agent.x * self.boardSize/self.numSq + self.boardSize/self.numSq,
                        agent.y * self.boardSize/self.numSq + self.boardSize/self.numSq)
        self.canvas.update()

