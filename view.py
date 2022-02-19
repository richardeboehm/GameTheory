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
        self.canvas = tkinter.Canvas(self.window, width=self.boardSize, height=self.boardSize, bg='#444444')
        self.canvas.pack()
        tkinter.Checkbutton(self.window, text="Runaway", command=self.game.changeRunaway).pack()
        tkinter.Button(self.window, text="START", command=self.game.gameLoop).pack()

    def displayNewAgent(self, newAgent, colorval):
        return self.canvas.create_oval(newAgent.x * self.boardSize/self.numSq,
                                    newAgent.y * self.boardSize/self.numSq,
                                    newAgent.x * self.boardSize/self.numSq + self.boardSize/self.numSq,
                                    newAgent.y * self.boardSize/self.numSq + self.boardSize/self.numSq,
                                    fill=colorval)

    def removeAgent(self, agent):
        self.canvas.delete(agent.reference)

    def updateBoard(self, agents):
        # redraw all agents and update the canvas
        for agent in agents:
            self.canvas.coords(agent.reference,
                        agent.x * self.boardSize/self.numSq,
                        agent.y * self.boardSize/self.numSq,
                        agent.x * self.boardSize/self.numSq + self.boardSize/self.numSq,
                        agent.y * self.boardSize/self.numSq + self.boardSize/self.numSq)
        self.canvas.update()

