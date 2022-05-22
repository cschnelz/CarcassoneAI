from asyncio import base_events
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
        self.greeting = tkinter.Label(text="Carcassonne").pack()
        tkinter.Button(self.t, command=self.t.destroy, text='Close').pack()
        self.randButton = tkinter.Button(self.t, command=self.play0,text='random play')
        self.randButton.pack()

        self.WIDTH = 1500
        self.HEIGHT = 600
        self.TILESIZE = 60
        self.HALFTILE = self.TILESIZE / 2

        self.cX = self.WIDTH / 2 - self.HALFTILE
        self.cY = self.HEIGHT / 2 - self.HALFTILE

        self.CANVASBG = 'gray75'
        self.c = tkinter.Canvas(self.t, width=self.WIDTH,height=self.HEIGHT,background=self.CANVASBG)
        self.c.pack(expand='YES', fill='both')

        
        
        self.carcassonne = None
        self.board = None
        self.images = []
        self.stock = []
        self.orientation = 0
        self.currTileImg = None

        self.scoreLabel = tkinter.Label(self.c, text=f'Score: Red 0 | Blue 0', font=("Arial", 25), bg=self.CANVASBG)
        self.scoreLabel.place(x=1500, y=10)
        self.toMoveLabel = tkinter.Label(self.c, text=f'Red to play', font=("Arial", 25),bg=self.CANVASBG)
        self.toMoveLabel.place(x=1500, y=60)
        self.turnsLabel = tkinter.Label(self.c, font=("Arial", 25),bg=self.CANVASBG, text=f'{70} turns left')
        self.turnsLabel.place(x=1500, y=110)

        self.meeples = {}
        self.meepleButtons = []
        self.meepleButtonImgs = []
        self.buttons = [] 

    def spawnGame(self):
        self.rotateButton = tkinter.Button(self.c, command=self.rotate,text='Rotate Tile')
        self.rotateButton.place(x=90,y=180)
        tkinter.Label(self.c, text='Current Tile', font=("Arial", 25), background=self.CANVASBG).place(x=50,y=10)

        ## Start a new game
        self.carcassonne = Game(order=[24,5,17,16,23])
        self.board = self.carcassonne.state.board

        self.images = []

        self.drawTile(0,0,self.board.board[(0,0)].tile)
        self.orientation = 0
        self.drawCurrTile()
        self.drawLocations()
        self.scoreBoard()
        self.meepleStock()

        self.t.mainloop()
        

    #################
    #
    #   HEADERS
    #
    ################
    def meepleStock(self):
        mRed = self.carcassonne.state.players[0].meepleCount
        mBlue = self.carcassonne.state.players[1].meepleCount

        self.stock = []
        tkinter.Label(text=f'{mRed}:', font=("Arial",25), background=self.CANVASBG).place(x=25,y=300)
        tkinter.Label(text=f'{mBlue}:', font=("Arial",25), background=self.CANVASBG).place(x=25,y=375)
        for i in range(mRed):
            meepleImage = ImageTk.PhotoImage(Image.open(rf'Images/red.png').resize((50,50)), master=self.c)
            self.stock.append(meepleImage)
            self.c.create_image(90 + (i * 25),300, image=meepleImage)
        for i in range(mBlue):
            meepleImage = ImageTk.PhotoImage(Image.open(rf'Images/blue.png').resize((50,50)), master=self.c)
            self.stock.append(meepleImage)
            self.c.create_image(90 + (i * 25),375, image=meepleImage)
    
    ## Draws curent score and who's turn it is
    def scoreBoard(self):
        score = self.carcassonne.getScore()
        self.scoreLabel.configure(text=f'Score: Red {score[0]} | Blue {score[1]}')

        toMove = 'Red' if self.carcassonne.state.currentPlayer == 0 else 'Blue'
        self.toMoveLabel.configure(text=f'{toMove} to play')
        
        self.turnsLabel.configure(text=f'{72 - self.carcassonne.state.turn} turns left')

    def drawCurrTile(self):
        tile = self.carcassonne.state.currentTile[self.orientation]
        img = Image.open(rf'Images/tile-{tile.imgCode}.png').resize((100,100))
        imgR = rotateImage(img, tile.orientation)
        imgTk = ImageTk.PhotoImage(imgR, master=self.c)
        
        self.currTileImg = imgTk
        self.c.create_image(140,125,image=imgTk)

    def endScreen(self):
        score = self.carcassonne.finalScore()
        self.finalScore = tkinter.Label(self.c, text=f"Game Over! Red {score[0]} | Blue {score[1]}", font=("Arial",25))
        self.finalScore.place(x=600, y=100)
        winText = 'Red Wins!' if score[0] > score[1] else 'Blue Wins!' if score[1] > score[0] else 'Tie!'
        self.winner = tkinter.Label(self.c, text=winText,font=("Arial",25))
        self.winner.place(x=600, y=300)

        self.newGameButton =tkinter.Button(self.c, text="New Game?", font=("Arial",25),command=self.newGame)
        self.newGameButton.place(x=600, y=500)

        self.randButton["state"] = "disabled"
        self.rotateButton["state"] = "disabled"

    def newGame(self):
        self.t.destroy()
        self.t = tkinter.Tk()
        self.greeting = tkinter.Label(text="Carcassonne").pack()
        tkinter.Button(self.t, command=self.t.destroy, text='Close').pack()
        self.randButton = tkinter.Button(self.t, command=self.play0,text='random play')
        self.randButton.pack()

        # self.finalScore.place_forget()
        # self.winner.place_forget()
        # self.newGameButton.place_forget()

        # self.c.pack_forget()
        self.c = tkinter.Canvas(self.t, width=self.WIDTH,height=self.HEIGHT,background=self.CANVASBG)
        self.c.pack(expand='YES', fill='both')

        self.scoreLabel = tkinter.Label(self.c, text=f'Score: Red 0 | Blue 0', font=("Arial", 25), bg=self.CANVASBG)
        self.scoreLabel.place(x=1500, y=10)
        self.toMoveLabel = tkinter.Label(self.c, text=f'Red to play', font=("Arial", 25),bg=self.CANVASBG)
        self.toMoveLabel.place(x=1500, y=60)
        self.turnsLabel = tkinter.Label(self.c, font=("Arial", 25),bg=self.CANVASBG, text=f'{70} turns left')
        self.turnsLabel.place(x=1500, y=110)


        self.carcassonne = Game()
        self.board = self.carcassonne.state.board

        self.images = []
        self.stock = []
        self.orientation = 0
        self.currTileImg = None
        self.toMoveLabel.configure(text='Red to Play')
        self.turnsLabel.configure(text=f'{72 - self.carcassonne.state.turn} turns left')
        self.scoreLabel.configure(text='Score: Red 0 | Blue 0')
        self.meeples = {}
        self.meepleButtons = []
        self.meepleButtonImgs = []
        for b in self.buttons:
            b.place_forget()
        self.buttons = []

        self.randButton["state"] = "normal"
        self.rotateButton["state"] = "normal"


        self.drawTile(0,0,self.board.board[(0,0)].tile)
        self.orientation = 0
        self.drawCurrTile()
        self.drawLocations()
        self.scoreBoard()
        self.meepleStock()


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
        if self.carcassonne.state.currentPlayer == 1:
            col = 'red'
        else:
            col = 'blue'
        meepleImage = ImageTk.PhotoImage(Image.open(rf'Images/{col}.png').resize((25,25)), master=self.c)
     
        self.meeples[(x,y)] = meepleImage
        mx = self.cX + (self.TILESIZE*x)
        my = self.cY + (self.TILESIZE*y)
        if feature.featType == FeatType.CHAPEL:
            mx += 0
        elif feature.featType is not FeatType.GRASS:
            edge = feature.edges[0]
            if edge == 0:
                my -= 15
            elif edge == 1:
                mx += 15
            elif edge == 2:
                my += 15
            else:
                mx -= 15
        else:
            edge = feature.edges[0]
            if edge == 0:
                mx -= 10
                my -= 15
            elif edge == 1:
                mx += 10
                my -= 15
            elif edge == 2:
                mx += 15
                my -= 10
            elif edge == 3:
                mx += 15
                my += 10
            elif edge == 4:
                mx += 10
                my += 15
            elif edge == 5:
                mx -= 10
                my += 15
            elif edge == 6:
                mx -= 15
                my += 10
            else:
                mx -= 15
                my -= 10
        self.c.create_image(mx, my, image=meepleImage)

    
    ####################
    #
    #   CORE LOGIC LOOP
    #
    ####################

    ### LOGIC LOOP:
        ## draw locations --->  play tile ---> meeple options ----> draw locations
        ##                |---> rotate current tile ---> draw locations


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
        prevScore = self.carcassonne.getScore()

        completed = self.carcassonne.applyAction(action)
       
        self.orientation = 0
        
        for b in self.meepleButtons:
            b.place_forget()
        self.meepleButtons = []
        self.meepleButtonImgs = []

        ## draw meeple on tile if specified
        if action.meeple:
            self.drawMeeple(action.x,action.y,action.feature)

        ## if meeples were scored, we forget their image to undraw them
        for loc in completed:
            del self.meeples[loc]

        currScore = self.carcassonne.getScore()
        if prevScore != currScore:
            if currScore[0] > prevScore[0] and currScore[1] > prevScore[1]:
                txt = f"Score! Red earned {currScore[0]-prevScore[0]} and Blue earned {currScore[1]-prevScore[1]} points!"
            elif currScore[0] > prevScore[0] and currScore[1] == prevScore[1]:
                txt = f'Score! Red earned {currScore[0]-prevScore[0]} points!'
            elif currScore[0] == prevScore[0] and currScore[1] > prevScore[1]:
                txt = f'Score! Blue earned {currScore[1]-prevScore[1]} points!'
            scoreLabel = tkinter.Label(self.c, text=txt, font=("Arial",25),bg=self.CANVASBG)
            scoreLabel.place(x=400,y=25)
            self.t.after(3000, scoreLabel.destroy)

        if self.carcassonne.gameOver():
            self.endScreen()

        else:
            self.scoreBoard()
            self.drawCurrTile()
            self.drawLocations()
            self.meepleStock()

     

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
                    by -= LONG
                elif edge == 1:
                    bx += LONG
                    vertical = False
                elif edge == 2:
                    by += LONG
                else:
                    bx -= LONG
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
            b = tkinter.Button(self.c, command=partial(self.meepleOption,a),image=img,borderwidth=1, bg=bgCol)
            b.place(x=bx,y=by)
            self.meepleButtons.append(b)
        
        ## Don't place meeple option
        b = tkinter.Button(self.c,command=partial(self.meepleOption,action), height=2, width=1, text='None', background='#cebbd2')
        b.place(x=self.cX + (self.TILESIZE*l[0]) + 75, y = self.cY + (self.TILESIZE*l[1]) +75)
        self.meepleButtons.append(b)


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
    demo.spawnGame()