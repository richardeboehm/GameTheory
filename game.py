import random
import tkinter
from math import floor
from agent import Agent
from board import Board

total = 0

def addAgent(agent):
    board.add(agent)
    agents.add(agent)
    global total
    total += agent.strategy


def kill(agent):
    agent.canvas.delete(agent.reference)
    board.remove(agent)
    agents.remove(agent)
    global total
    total -= agent.strategy
    agent.die()


def findAdj(agent, agentRange):
    emptyAdj = []
    # loop through all adjecent squares and find empty ones
    for i in range(agent.x - agentRange, agent.x + agentRange + 1):
        if i >= 0 and i < len(board.Positions):
            for j in range(agent.y - agentRange, agent.y + agentRange + 1):
                if j >= 0 and j < len(board.Positions[i]):
                    if board.Positions[i][j] is None:
                        emptyAdj.append((i, j))

    # CASE: no empty adjacent squares -- try again with wider margin
    if len(emptyAdj) == 0:
        return findAdj(agent, agentRange + 1)

    return emptyAdj


def multiply(agent):
    # CASE: maxAgents reached -- don't multiply
    if len(agents) >= maxAgents:
        agent.life = 25
        return

    # cut life in half and create new agent
    agent.life = 25
    emptyAdj = findAdj(agent, 1)
    newPosition = random.sample(emptyAdj, 1)[0]
    newAgent = Agent(agent.canvas, newPosition[0], newPosition[1])

    # five percent chance that new agent mutates to new strategy
    if random.random() > .01:
        newAgent.strategy = agent.strategy

    # determine color of agent and draw it on the canvas
    addAgent(newAgent)
    colorval = '#%02x%02x%02x' % (floor(255 - (newAgent.strategy * 255)), floor(newAgent.strategy * 255), 0)
    newAgent.reference = canvas.create_oval(newAgent.x * boardSize/numSq,
                                            newAgent.y * boardSize/numSq,
                                            newAgent.x * boardSize/numSq + boardSize/numSq,
                                            newAgent.y * boardSize/numSq + boardSize/numSq,
                                            fill=colorval)


def gameLoop(canvas):
    # CASE: less than 100 agents
    if len(agents) < 100:
        # create a new agent
        newAgent = Agent(canvas,
                         floor(random.random() * len(board.Positions)),
                         floor(random.random() * len(board.Positions[0])))

        # find an empty position to place the agent
        while board.Positions[newAgent.x][newAgent.y]:
            newAgent.x = floor(random.random() * len(board.Positions))
            newAgent.y = floor(random.random() * len(board.Positions[0]))
        addAgent(newAgent)

        # determine color of agent and draw it on the canvas
        colorval = '#%02x%02x%02x' % (floor(255 - (newAgent.strategy * 255)), floor(newAgent.strategy * 255), 0)
        newAgent.reference = canvas.create_oval(newAgent.x * boardSize/numSq,
                                            newAgent.y * boardSize/numSq,
                                            newAgent.x * boardSize/numSq + boardSize/numSq,
                                            newAgent.y * boardSize/numSq + boardSize/numSq,
                                            fill=colorval)

    # agents is copied because agents, a set, will change as members die
    for agent in agents.copy():
        # CASE: agent not in agents -- agent has died
        if agent not in agents:
            continue

        # find all of the agent's neighbors
        neighbors = []
        for i in range(agent.x - 1, agent.x + 2):
            if i >= 0 and i < len(board.Positions):
                for j in range(agent.y - 1, agent.y + 2):
                    if j >= 0 and j < len(board.Positions[i]):
                        if board.Positions[i][j] and board.Positions[i][j] is not agent:
                            neighbors.append(board.Positions[i][j])

        # if agent has no neighbors, move the agent, and continue
        if len(neighbors) < 1:
            board.move(agent)
            continue

        # choose a random neighbor as the opponent and play against it
        opponent = random.sample(neighbors, 1)[0]
        agent.play(opponent)

        if Runaway:
            if not agent.memory[opponent]:
                board.move(agent)
            if not opponent.memory[agent]:
                board.move(opponent)

        # determine if the agent or opponent die or multiply
        if agent.life <= 0:
            kill(agent)
        elif agent.life >= 50:
            multiply(agent)
        if opponent.life <= 0:
            kill(opponent)
        elif opponent.life >= 50:
            multiply(opponent)

    # redraw all agents and update the canvas
    for agent in agents:
        canvas.coords(agent.reference,
                      agent.x * boardSize/numSq,
                      agent.y * boardSize/numSq,
                      agent.x * boardSize/numSq + boardSize/numSq,
                      agent.y * boardSize/numSq + boardSize/numSq)
    canvas.update()

    print(total / len(agents))


if __name__ == "__main__":
    #determine the size of the board, maximum agents, and create the board
    numSq = 175;
    boardSize = 525
    maxAgents = 6000
    board = Board(numSq)
    agents = set()
    buttonVar = None
    global Runaway
    Runaway = False

    #set up the canvas
    window = tkinter.Tk()
    window.title("gameTheory.py")
    canvas = tkinter.Canvas(window, width=boardSize, height=boardSize, bg='gray')
    canvas.pack()
    buttonVar = tkinter.BooleanVar()
    def changeRunaway():
        global Runaway
        Runaway = buttonVar.get()
    tkinter.Checkbutton(window, text="Runaway", variable=buttonVar, command=changeRunaway).pack()

    # initiate the game's main loop
    while 1:
        gameLoop(canvas)

    window.mainloop()
