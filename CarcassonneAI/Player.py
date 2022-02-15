



class Player:
    def __init__(self, id):
        self.id = id
        if id == 0:
            self.color = 'red'
        else:
            self.color = 'blue'

    meeples = 7
    score = 0
    
    