



class Player:
    def __init__(self, id):
        self.id = id
        if id == 0:
            self.color = 'red'
        else:
            self.color = 'blue'

        self.meepleCount = 7
        self.score = 0
    
    