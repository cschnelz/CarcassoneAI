from Agents import Agent

class Player:
    def __init__(self, id:int, agent: Agent):
        self.id = id
        if id == 0:
            self.color = 'red'
        else:
            self.color = 'blue'

        self.meepleCount = 7
        self.score = 0

        self.agent = agent