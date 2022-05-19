import tkinter
from Game import Game
from Agents import *
from PIL import Image, ImageTk

t = tkinter.Tk()
greeting = tkinter.Label(text="Carcassonne").pack()

c = tkinter.Canvas(t, width=2000,height=900,background='gray75')
c.pack()

tkinter.Button(t, command=t.destroy, text='Close').pack()





def rotateImage(img, orientation):
    if orientation == 0:
        return img
    if orientation == 1:
        return img.rotate(270)
    if orientation == 2:
        return img.rotate(180)
    if orientation == 3:
        return img.rotate(90)

def drawTile(x,y,tile):
    img = Image.open(rf'Images/tile-{tile.imgCode}.png').resize((50,50))
    imgR = rotateImage(img, tile.orientation)
    imgTk = ImageTk.PhotoImage(imgR, master=c)
    images.append(imgTk)
    c.create_image(cX + (50*x),cY + (50*y),image=imgTk)

def play0():
    response = random.choice(carcassonne.getActions())
    carcassonne.applyAction(response)
    drawTile(response.x,response.y,response.tile)


tkinter.Button(t, command=play0,text='random play').pack()


carcassonne = Game()
board = carcassonne.state.board

images = []
cX = 1000
cY = 450


drawTile(0,0,board.board[(0,0)].tile)


# for item, node in board.board.items():
#     img = Image.open(rf'Images/tile-{node.tile.imgCode}.png')
#     imgR = rotateImage(img, node.tile.orientation)
#     imgTk = ImageTk.PhotoImage(imgR, master=c)
#     images.append(imgTk)

#     c.create_image(cX,cY,image=imgTk)

tile = carcassonne.state.currentTile[0]
img = Image.open(rf'Images/tile-{tile.imgCode}.png')
imgTk = ImageTk.PhotoImage(img, master=c)
images.append(imgTk)
c.create_image(200,0,image=imgTk)




t.mainloop()