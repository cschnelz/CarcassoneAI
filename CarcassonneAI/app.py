from doctest import master
from re import L
import tkinter
from turtle import back
from Game import Game
from Agents import *
from PIL import Image, ImageTk
from functools import partial
from Action import Action
from Feature import Feature
import threading






def rotateImage(img, orientation):
    if orientation == 0:
        return img
    if orientation == 1:
        return img.rotate(270)
    if orientation == 2:
        return img.rotate(180)
    if orientation == 3:
        return img.rotate(90)

class app:
    #WIDTH = 2000

    def __init__(self) -> None:
        self.t = tkinter.Tk()
        self.closeBtn = tkinter.Button(self.t, command=self.t.destroy, text='Close')
        self.closeBtn.pack()
        self.newGameBtn = tkinter.Button(self.t, command=self.newGameB, text='New Game')
        self.newGameBtn.pack()

        self.WIDTH = 2000
        self.HEIGHT = 900
        self.TILESIZE = 80
        self.HALFTILE = self.TILESIZE / 2

        self.cX = self.WIDTH / 2 - self.HALFTILE - 200
        self.cY = self.HEIGHT / 2 - self.HALFTILE + 50

        self.CANVASBG = 'gray75'

        self.MaxTurns = 30
       
        self.carcassonne = None
        self.board = None
        self.images = []
        self.stock = []
        self.orientation = 0
        self.currTileImg = None

        self.bestAgentRectangles = [None for i in range(3)]

        self.bestAgentTiles = []
        self.bestAgentMeeples = []
        # self.bestAgentLabels = [tkinter.Label(self.c, image=None, bg=colors[i], borderwidth=2) for i in range(3)]
        # for i in range(3):
        #     self.bestAgentLabels[i].place(x=1300, y=500 + (100 * i))


        self.meeples = {}
        self.meepleButtons = []
        self.meepleButtonImgs = []
        self.buttons = [] 

        self.stats = []
        self.statsIter = 0
        self.statsMax = 0
        self.currActions = None
        self.labelPtr = None

    def init(self):
        self.spawnGame()
        self.t.mainloop()

  

    def spawnGame(self):
        ## canvas
        self.c = tkinter.Canvas(self.t, width=self.WIDTH,height=self.HEIGHT,background=self.CANVASBG)
        self.c.pack(expand='YES', fill='both')

        # Carcassonne Logo
        self.logo = ImageTk.PhotoImage(Image.open(rf'Images/logo.png').resize((500,150)), master=self.c)
        self.c.create_image(260, 85, image=self.logo)

        # current tile things
        self.rotateButton = tkinter.Button(self.c, command=self.rotate,text='Rotate Tile')
        self.rotateButton.place(x=1325,y=180)
        tkinter.Label(self.c, text='Current Tile', font=("Arial", 25), background=self.CANVASBG).place(x=1290,y=25)

        ## Labels and border for scorboard
        self.scoreLabel = tkinter.Label(self.c, text=f'Score: Red 0 | Blue 0', font=("Arial", 25), bg=self.CANVASBG)
        self.scoreLabel.place(x=1525, y=35)
        self.toMoveLabel = tkinter.Label(self.c, text=f'Red to play', font=("Arial", 25),bg=self.CANVASBG)
        self.toMoveLabel.place(x=1525, y=85)
        self.turnsLabel = tkinter.Label(self.c, font=("Arial", 25),bg=self.CANVASBG, text=f'{self.MaxTurns} turns left')
        self.turnsLabel.place(x=1525, y=135)
        self.c.create_rectangle(1500, 25, 1900, 300, width=5)

        ## Labels and outline for MCTS info
        tkinter.Label(self.c, text="A Peek Into the Agent", font=("Arial", 20), bg=self.CANVASBG).place(x=1500, y=375)
        tkinter.Label(self.c, text="Current Best Estimate:", font=("Arial",15), bg=self.CANVASBG).place(x=1550, y=450)
        self.c.create_rectangle(1500, 425, 1900, 900, width=5)
      
        colors = ['orange', 'green', 'yellow']
        for ind in range(3):
            self.c.create_rectangle(1550, 500 + (120 * ind), 1650, 600 + (120 * ind), outline=colors[ind], width=5)

        self.bestAgentInfos = [tkinter.Label(self.c, text="Score: ", font=("Arial",15), bg=self.CANVASBG) for i in range(3)]
        for i in range(3):
            self.bestAgentInfos[i].place(x=1700, y=525 + (i * 125))

        ## Start a new game
        self.carcassonne = Game(players=[HumanAgent(), MCTS_Saver(info='Heuristic')])
        #self.carcassonne = Game(players=[HumanAgent(), HumanAgent()], order=[24,20,13,6,53,56,18])
        self.carcassonne.state.turn = 72 - self.MaxTurns

        self.board = self.carcassonne.state.board

        self.images = []

        self.drawTile(0,0,self.board.board[(0,0)].tile)
        self.orientation = 0
        self.drawCurrTile()
        self.drawLocations()
        self.scoreBoard()
        self.meepleStock()

        
        

    #################
    #
    #   HEADERS
    #
    ################
    def meepleStock(self):
        mRed = self.carcassonne.state.players[0].meepleCount
        mBlue = self.carcassonne.state.players[1].meepleCount

        self.stock = []
        tkinter.Label(text=f'{mRed}:', font=("Arial",25), background=self.CANVASBG).place(x=1525,y=250)
        tkinter.Label(text=f'{mBlue}:', font=("Arial",25), background=self.CANVASBG).place(x=1525,y=310)
        for i in range(mRed):
            meepleImage = ImageTk.PhotoImage(Image.open(rf'Images/red.png').resize((50,50)), master=self.c)
            self.stock.append(meepleImage)
            self.c.create_image(1585 + (i * 25),215, image=meepleImage)
        for i in range(mBlue):
            meepleImage = ImageTk.PhotoImage(Image.open(rf'Images/blue.png').resize((50,50)), master=self.c)
            self.stock.append(meepleImage)
            self.c.create_image(1585 + (i * 25),270, image=meepleImage)
    
    ## Draws curent score and who's turn it is
    def scoreBoard(self):
        score = self.carcassonne.getScore()
        self.scoreLabel.configure(text=f'Score: Red {score[0]} | Blue {score[1]}')

        toMove = 'Red' if self.carcassonne.state.currentPlayer == 0 else 'Blue'
        self.toMoveLabel.configure(text=f'{toMove} to play', fg=toMove)
        
        self.turnsLabel.configure(text=f'{72 - self.carcassonne.state.turn} turns left')

    def drawCurrTile(self):
        tile = self.carcassonne.state.currentTile[self.orientation]
        img = Image.open(rf'Images/tile-{tile.imgCode}.png').resize((100,100))
        imgR = rotateImage(img, tile.orientation)
        imgTk = ImageTk.PhotoImage(imgR, master=self.c)
        
        self.currTileImg = imgTk
        self.c.create_image(1375,125,image=imgTk)

    def endScreen(self):
        score = self.carcassonne.finalScore()
        self.finalScore = tkinter.Label(self.c, text=f"Game Over! Red {score[0]} | Blue {score[1]}", font=("Arial",25))
        self.finalScore.place(x=600, y=100)
        winText = 'Red Wins!' if score[0] > score[1] else 'Blue Wins!' if score[1] > score[0] else 'Tie!'
        self.winner = tkinter.Label(self.c, text=winText,font=("Arial",25))
        self.winner.place(x=600, y=300)

        self.newGameButton =tkinter.Button(self.c, text="New Game?", font=("Arial",25),command=self.newGame)
        self.newGameButton.place(x=600, y=500)

        self.rotateButton["state"] = "disabled"

    def newGameB(self):
        self.c.pack_forget()
        self.spawnGame()

    def newGame(self):
        self.finalScore.place_forget()
        self.winner.place_forget()
        self.newGameButton.place_forget()

        self.c.pack_forget()
      
        self.spawnGame()


    ################
    #
    #   BOARD DRAWS
    #
    ################
    def drawTile(self, x,y,tile):
        img = Image.open(rf'Images/tile-{tile.imgCode}.png').resize((self.TILESIZE,self.TILESIZE))
        imgR = rotateImage(img, tile.orientation)
        imgTk = ImageTk.PhotoImage(imgR, master=self.c)
        self.images.append(imgTk)
        self.c.create_image(self.cX + (self.TILESIZE*x),self.cY + (self.TILESIZE*y),image=imgTk)

    def drawMeeple(self, x,y,feature:Feature):
        if self.carcassonne.state.currentPlayer == 0:
            col = 'red'
        else:
            col = 'blue'
        meepleImage = ImageTk.PhotoImage(Image.open(rf'Images/{col}.png').resize((30,30)), master=self.c)
     
        self.meeples[(x,y)] = meepleImage
        mx = self.cX + (self.TILESIZE*x)
        my = self.cY + (self.TILESIZE*y)

        SHORT = 22
        LONG = 25
        if feature.featType == FeatType.CHAPEL:
            mx += 0
        elif feature.featType is not FeatType.GRASS:
            edge = feature.edges[0]
            if edge == 0:
                my -= LONG
            elif edge == 1:
                mx += LONG
            elif edge == 2:
                my += LONG
            else:
                mx -= LONG
        else:
            edge = feature.edges[0]
            if edge == 0:
                mx -= SHORT
                my -= LONG
            elif edge == 1:
                mx += SHORT
                my -= LONG
            elif edge == 2:
                mx += LONG
                my -= SHORT
            elif edge == 3:
                mx += LONG
                my += SHORT
            elif edge == 4:
                mx += SHORT
                my += LONG
            elif edge == 5:
                mx -= SHORT
                my += LONG
            elif edge == 6:
                mx -= LONG
                my += SHORT
            else:
                mx -= LONG
                my -= SHORT
        self.c.create_image(mx, my, image=meepleImage)

    
    def drawBestTile(self, tile, ind, act):
        img = Image.open(rf'Images/tile-{tile.imgCode}.png').resize((90,90))
        imgR = rotateImage(img, tile.orientation)
        imgTk = ImageTk.PhotoImage(imgR, master=self.c)
        self.bestAgentTiles.append(imgTk)
        self.c.create_image(1600, 550 + (120 * ind), image=imgTk)
        colors = ['orange', 'green', 'yellow']
        self.bestAgentRectangles[ind] = self.c.create_rectangle(
            self.cX + (act.x * self.TILESIZE) + (ind * 2) - (self.TILESIZE / 2), 
            self.cY + (act.y * self.TILESIZE) + (ind * 2) - (self.TILESIZE / 2), 
            self.cX + (act.x * self.TILESIZE) + self.TILESIZE - (ind * 2) - (self.TILESIZE / 2), 
            self.cY + (act.y * self.TILESIZE) + self.TILESIZE - (ind * 2) - (self.TILESIZE / 2), 
            outline=colors[ind], width=5)
    


    def drawBestMeeple(self, action, ind):
        col = self.carcassonne.currentPlayer().color
        img = Image.open(rf'Images/{col}.png').resize((30,30))
        imgTk = ImageTk.PhotoImage(img, master=self.c)
        self.bestAgentMeeples.append(imgTk)
        mx = 1600
        my = 550 + (120 * ind)
        long = 20
        short = 15
        if action.feature.featType == FeatType.CHAPEL:
            mx += 0
        elif action.feature.featType is not FeatType.GRASS:
            edge = action.feature.edges[0]
            if edge == 0:
                my -= long
            elif edge == 1:
                mx += long
            elif edge == 2:
                my += long
            else:
                mx -= long
        else:
            edge = action.feature.edges[0]
            if edge == 0:
                mx -= short
                my -= long
            elif edge == 1:
                mx += short
                my -= long
            elif edge == 2:
                mx += long
                my -= short
            elif edge == 3:
                mx += long
                my += short
            elif edge == 4:
                mx += short
                my += long
            elif edge == 5:
                mx -= short
                my += long
            elif edge == 6:
                mx -= long
                my += short
            else:
                mx -= long
                my -= short
        self.c.create_image(mx,my,image=imgTk)


    ####################
    #
    #   CORE LOGIC LOOP
    #
    ####################

    ### LOGIC LOOP:
        ## draw locations --->  play tile ---> meeple options ----> draw locations
        ##                |---> rotate current tile ---> draw locations


    ## Check for and report score change
    def checkScore(self, prevScore):
        currScore = self.carcassonne.getScore()
        if prevScore != currScore:
            if currScore[0] > prevScore[0] and currScore[1] > prevScore[1]:
                txt = f"Score! Red earned {currScore[0]-prevScore[0]} and Blue earned {currScore[1]-prevScore[1]} points!"
            elif currScore[0] > prevScore[0] and currScore[1] == prevScore[1]:
                txt = f'Score! Red earned {currScore[0]-prevScore[0]} points!'
            elif currScore[0] == prevScore[0] and currScore[1] > prevScore[1]:
                txt = f'Score! Blue earned {currScore[1]-prevScore[1]} points!'
            scoreLabel = tkinter.Label(self.c, text=txt, font=("Arial",25),bg=self.CANVASBG)
            scoreLabel.place(x=650,y=75)
            self.t.after(3000, scoreLabel.destroy)


    ## Rotate current tile and redraw open locatons
    ## Callback flow: DRAWLOCATION
    def rotate(self):
        currTiles = self.carcassonne.state.currentTile
        max = len(currTiles)
        self.orientation = (self.orientation + 1) % max
        self.drawCurrTile()
        self.drawLocations() 


    ## Carry out the meeple decision, destroy spawned buttons and score
    ## Callback flow: DRAWLOCATIONS
    def meepleOption(self, action:Action):
        self.confirmationButton.place_forget()
        self.cancelButton.place_forget()
        prevScore = self.carcassonne.getScore()
        completed = self.carcassonne.applyAction(action)
       
        self.orientation = 0

        ## if meeples were scored, we forget their image to undraw them
        for loc in completed:
            del self.meeples[loc]

        self.checkScore(prevScore)

        if self.carcassonne.gameOver():
            self.endScreen()

        else:  
            self.scoreBoard()
            self.drawCurrTile()
            self.meepleStock()

            if self.carcassonne.currentPlayer().agent.type != 'Human':
                threading.Thread(target=self.agentResponse).start()

            else:
                self.drawLocations()

    def agentResponse(self):
        self.rotateButton["state"] = "disabled"
        self.closeBtn["state"] = "disabled"
        self.newGameBtn["state"] = "disabled"

        self.stats = []
        self.bestAgentTiles = []
        self.currActions = self.carcassonne.getActions()
        response = self.carcassonne.currentPlayer().agent.getResponse(self.trackCalculation,self.carcassonne,self.carcassonne.currentPlayerId())
        
        prevScore = self.carcassonne.getScore()
        self.drawTile(response.x,response.y,response.tile)
        if response.meeple:
            self.drawMeeple(response.x,response.y,response.feature)
        completed = self.carcassonne.applyAction(response)
        self.checkScore(prevScore)
    

    
        for loc in completed:
            del self.meeples[loc]  

        self.orientation = 0
        if self.carcassonne.gameOver():
            self.endScreen()

        else:
            self.scoreBoard()
            self.drawCurrTile()
            self.drawLocations()
            self.meepleStock()

        self.rotateButton["state"] = "normal"
        self.closeBtn["state"] = "normal"
        self.newGameBtn["state"] = "normal"
        self.c.after(1500, lambda: [self.c.delete(self.bestAgentRectangles[i]) for i in range(3)])
            #self.c.delete(self.bestAgentRectangles[i])


    ## A callback to track the current mcts evluation
    def trackCalculation(self, info):
        self.stats.append(info)

        rank = []
        self.bestAgentMeeples = []
        for i in range(3):
            self.c.delete(self.bestAgentRectangles[i])
        
        for i in range(len(self.stats[0])):
            avg_ucb = 0.0
            ## and the inner loop ranges the number of determinzations
            for det in range(len(self.stats)):
                ## add the ucb of this determinzations ith action
                avg_ucb += self.stats[det][i]
                
            avg_ucb = avg_ucb / len(self.stats)
            rank.append(avg_ucb)
        
        for i in range(3):
            ind = rank.index(max(rank))
            act = self.currActions[ind]
            self.drawBestTile(act.tile, i, act)
            self.bestAgentInfos[i].configure(text="Score: {:0.2f}".format((rank[ind])))
            if act.meeple:
                self.drawBestMeeple(act, i)
            rank[ind] = -math.inf

    ## draw in the new tile and spawn buttons for meeple options
    ## callback flow: MEEPLE OPTION
    def playTile(self, l, o):
        action = next((act for act in self.carcassonne.getActions() if act.x == l[0] and act.y == l[1] and act.tile.orientation == o), None)
        self.drawTile(action.x,action.y,action.tile)
        

        for b in self.buttons:
            b.place_forget()
        self.buttons = []
        allActions = [act for act in self.carcassonne.getActions() if act.x == l[0] and act.y == l[1] and act.tile.orientation == o and act.feature is not None]
        for a in allActions:
            bx = self.cX + (self.TILESIZE*l[0]) - 15
            by = self.cY + (self.TILESIZE*l[1]) - 15
            LONG = 60
            SHORT = 40
            vertical = True
            bgCol = 'red' if self.carcassonne.state.currentPlayer == 0 else 'blue'
            imgPath = ''


            if a.feature.featType is FeatType.CHAPEL:
                bg = '#0ec5db'
                bx += 10
                by += 10
                imgPath = 'Images/chapel.png'
            elif a.feature.featType is not FeatType.GRASS:
                bg = '#daa412'
                edge = a.feature.edges[0]
                if edge == 0:
                    by -= (LONG + 10)
                elif edge == 1:
                    bx += LONG
                    vertical = False
                elif edge == 2:
                    by += LONG
                else:
                    bx -= (LONG + 10)
                    vertical = False

                if a.feature.featType is FeatType.CITY:
                    imgPath = 'Images/city.png' if vertical else 'Images/cityH.png'
                else:
                    imgPath = 'Images/road.png' if vertical else 'Images/roadH.png'
            else:
                bg = '#15990a'
                edge = a.feature.edges[0]
                if edge == 0:
                    by -= LONG
                    bx -= SHORT
                elif edge == 1:
                    by -= LONG
                    bx += SHORT
                elif edge == 2:
                    bx += LONG
                    by -= SHORT
                    vertical = False
                elif edge == 3:
                    bx += LONG
                    by += SHORT
                    vertical = False
                elif edge == 4:
                    by += LONG
                    bx += SHORT
                elif edge == 5:
                    by += LONG
                    bx -= SHORT
                elif edge == 6:
                    bx -= LONG
                    by += SHORT
                    vertical = False
                else:
                    bx -= LONG
                    by -= SHORT
                    vertical = False
                
                imgPath = 'Images/grass.png' if vertical else 'Images/grassH.png'

        
            img = tkinter.PhotoImage(file=imgPath)
            self.meepleButtonImgs.append(img)
            b = tkinter.Button(self.c, command=partial(self.confirmation,a),image=img,borderwidth=1, bg=bgCol)
            b.place(x=bx,y=by)
            self.meepleButtons.append(b)
        
        ## Don't place meeple option
        b = tkinter.Button(self.c,command=partial(self.confirmation,action), height=2, width=3, text='None',font=("Arial",10), background='#cebbd2')
        b.place(x=self.cX + (self.TILESIZE*l[0]) + 75, y = self.cY + (self.TILESIZE*l[1]) +75)
        self.meepleButtons.append(b)

        ## Cancel placement button
        b2 = tkinter.Button(self.c,command=self.cancelPlacement,height=2,width=3,text='Cancel',font=("Arial",10) ,background='#cebbd2')
        b2.place(x=self.cX + (self.TILESIZE*l[0]) - 125, y=self.cY + (self.TILESIZE*l[1]) + 75)
        self.meepleButtons.append(b2)

    
    def confirmation(self, action):
        for b in self.meepleButtons:
            b.place_forget()
        self.meepleButtons = []
        self.meepleButtonImgs = []

        ## draw meeple on tile if specified
        if action.meeple:
            self.drawMeeple(action.x,action.y,action.feature)

        self.confirmationButton = tkinter.Button(self.c, command=partial(self.meepleOption,action), text='Confirm', font=("Arial",10), height=2, width=3,background='#cebbd2')
        self.confirmationButton.place(x=self.cX + (self.TILESIZE*action.x) + 50,y=self.cY + (self.TILESIZE*action.y) + 50)

        self.cancelButton = tkinter.Button(self.c, command=partial(self.cancelMeeple,action), text='Cancel', font=("Arial",10), height=2, width=3,background='#cebbd2')
        self.cancelButton.place(x=self.cX + (self.TILESIZE*action.x) - 100,y=self.cY + (self.TILESIZE*action.y) + 50)
    
    def cancelMeeple(self, action):
        if (action.x,action.y) in self.meeples.keys():
            del self.meeples[(action.x,action.y)]
        self.images.pop()
        self.confirmationButton.place_forget()
        self.cancelButton.place_forget()
        self.drawLocations()

    def cancelPlacement(self):
        self.images.pop()
        for b in self.meepleButtons:
            b.place_forget()
        self.meepleButtons = []
        self.meepleButtonImgs = []

        self.drawLocations()

    ## draw valid locations for current tile
    ## callback flow: PLAYTILE
    def drawLocations(self):
        for b in self.buttons:
            b.place_forget()
        self.buttons = []

        validLocations = set()
        [validLocations.add((action.x, action.y)) for action in self.carcassonne.getActions() if (action.x,action.y) not in validLocations and action.tile.orientation == self.orientation]

        for loc in validLocations:
            b = tkinter.Button(self.c, command=partial(self.playTile,loc,self.orientation), height=2, width=3, text='', bg='#a1a28c',activebackground='#eef821')
            b.place(x=self.cX + (self.TILESIZE*loc[0]) - 25, y=self.cY + (self.TILESIZE*loc[1]) - 25)
            self.buttons.append(b)


    def play0(self):
        response = random.choice(self.carcassonne.getActions())
        completed = self.carcassonne.applyAction(response)
     
        self.drawTile(response.x,response.y,response.tile)
        if response.meeple:
            self.drawMeeple(response.x,response.y,response.feature)
       


        
        for loc in completed:
            del self.meeples[loc]  

        self.orientation = 0
        if self.carcassonne.gameOver():
            self.endScreen()

        else:
            self.scoreBoard()
            self.drawCurrTile()
            self.drawLocations()
            self.meepleStock()
        

if __name__=="__main__":
    demo = app()
    demo.init()




