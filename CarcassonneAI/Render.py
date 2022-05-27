from Board import Board, Node, meepleInfo
from Feature import *
from Tile import Tile, rotate
from Player import Player

import tkinter as tk
from PIL import Image, ImageTk


# *****************************

# RENDERER FOR CLI INFORMATION

# *****************************


def printFeature(tile: Tile, cardinal: int) -> str:
    if tile.edges[cardinal] == FeatType.CITY:
        return "C"
    elif tile.edges[cardinal] == FeatType.ROAD:
        return "R"
    
    if cardinal == 0 or cardinal == 2:
        return "-"
    return "|"


def renderTile(tile: Tile):
    print(" -  " + printFeature(tile, 0) + "  - ")   
    print("|       |")
    print(printFeature(tile,3) + "  T." + str(tile.id) + "  " + printFeature(tile,1))
    print("|       |")
    print(" -  " + printFeature(tile, 2) + "  - ")


def renderPlayOptions(tile: Tile):
    print("Tile Orientations: \n")

    orientations = [rotate(tile, i) for i in range(4)]

    # print north edges
    output = ""
    for t in orientations:
        output += " -  " + printFeature(t, 0) + "  -   "
    print(output)
    print("|       |  " * 4)
    
    # print west and east
    output = ""
    for t in orientations:
        output += printFeature(t,3) + "  T." + str(t.id) + "  " + printFeature(t,1) + "  "
    print(output)
    print("|       |  " * 4)

    # print south rows
    output = ""
    for t in orientations:
        output += " -  " + printFeature(t, 2) + "  -   "
    print(output)

# render a board with basic characters - goes row by row 
def render2(board: Board):
    # print the coordinate grid
    output = "   "
    for x in range(board.minX, board.maxX + 1):
        if x < 0:
            output += f"   {x}    "
        else:
            output += f"    {x}    "
    print(output + "\n")

    basicEdge = " - - - - "
    # print the top edge of the tile
    for y in range(board.minY, board.maxY+1):
        output = "   "
        for x in range(board.minX, board.maxX+1):
            node = board.board.get((x,y))
            if (x, y) in board.openLocations or node is None:
                output += basicEdge
            else:
                output += " -  " + printFeature(node.tile, 0) + "  - "
        print(output)

        # print some vertical edges
        print("   " + "|       |" * (board.maxX - board.minX + 1))

        # print the middle vert segment, with care for tile features
        if y < 0:
            output = f"{y} "
        else:
            output = f" {y} "
        for x in range(board.minX, board.maxX+1):
            node = board.board.get((x,y))
            if (x, y) in board.openLocations:
                output += "|  open |"
            elif node is None:
                output += "|       |"
            else:
                output += printFeature(node.tile,3) + "  T." + str(node.tile.id) + "  " + printFeature(node.tile,1)
        print(output)

        print("   " + "|       |" * (board.maxX - board.minX + 1))

        # print the bottom edge
        output = "   "
        for x in range(board.minX, board.maxX+1):
            node = board.board.get((x,y))
            if (x, y) in board.openLocations or node is None:
                output += basicEdge
            else:
                output += " -  " + printFeature(node.tile, 2) + "  - "
        print(output)





# *****************************

# RENDERER FOR TKINTER OUTPUT

# *****************************



class Renderer():
    def __init__(self) -> None:
        self.top = tk.Tk()
        self.top.geometry("800x800")

        self.MEEPLE_SIZE = 35
        self.TILE_SIZE = 100

        self.images = []

        self.currTileFrame = tk.Frame(self.top)
        self.gridFrame = tk.Frame(self.top)
        self.gridFrameY = tk.Frame(self.top)
        self.canvas = tk.Canvas(self.top, width=1000, height=1000)


    def destroyFrames(self):
        for widgets in self.gridFrameY.winfo_children():
            widgets.destroy()
        self.gridFrameY.pack_forget()
        for widgets in self.currTileFrame.winfo_children():
            widgets.destroy()
        self.currTileFrame.pack_forget()
        for widgets in self.gridFrame.winfo_children():
            widgets.destroy()
        self.gridFrame.pack_forget()

    def rotateAndRedraw(self, board: Board, currTile: Tile, players: List[Player]):
        rTile = rotate(currTile, 1)
        self.render3(board, rTile, players)

    def drawCurrTileOrient(self, root, currTile, orient):
        img = Image.open(rf'Images/tile-{currTile[0].imgCode}.png')
        imgR = self.rotateImage(img, orient)
        imgTk = ImageTk.PhotoImage(imgR)
        label = tk.Label(root, text="Current Tile:")
        label.grid(column=orient,row=0)

        # create the label for the current tile image
        labelImg = tk.Label(root, image=imgTk)
        labelImg.img = imgTk
        labelImg.grid(column=orient,row=1)

        labelO = tk.Label(root, text=f"Orientation {orient}")
        labelO.grid(column=orient, row=2)

    def drawCurrTile(self, root, currTile: Tile, players: List[Player], board):
        for i in range(4):
            self.drawCurrTileOrient(root, currTile, i)

        labelScore = tk.Label(root, text="Current Score:")
        labelScore.grid(column=5,row=0, padx=20)
        labelScore2 = tk.Label(root, text=f"{players[0].color} {players[0].score} | {players[1].color} {players[1].score}")
        labelScore2.grid(column=5, row=1)

        root.grid(column=0,row=1, pady=10, columnspan=5)

    def drawCoordsY(self, root, board: Board):
        for y in range(board.minY, board.maxY + 1):
            label = tk.Label(root, text=f'{y}')
            label.grid(column=0, row=y - board.minY, pady=40, sticky='w')
        root.grid(column=0, row=3,padx=10, sticky="n")

    def drawCoords(self, root, board: Board):
        for x in range(board.minX, board.maxX+1):
            label = tk.Label(root, text=f'{x}')
            label.grid(row=0, column=x - board.minX, padx=40, sticky='n')
        root.grid(column=1, row=2,pady=10, sticky="w")


    def rotateImage(self, img, orientation):
        if orientation == 0:
            return img
        if orientation == 1:
            return img.rotate(270)
        if orientation == 2:
            return img.rotate(180)
        if orientation == 3:
            return img.rotate(90)

    def meepleOffset(self, board: Board, x: int, y: int, meeple: meepleInfo, t: Tile):
        xCoord = (x - board.minX) * self.TILE_SIZE
        yCoord = (y - board.minY)* self.TILE_SIZE

        if t.chapel:
            return xCoord, yCoord

        if meeple.feature:
            if meeple.edge == 0:
                yCoord -= self.MEEPLE_SIZE
            elif meeple.edge == 1:
                xCoord += self.MEEPLE_SIZE
            elif meeple.edge == 2:
                yCoord += self.MEEPLE_SIZE
            else:
                xCoord -= self.MEEPLE_SIZE
        else:
            if meeple.edge == 0:
                yCoord -= (self.MEEPLE_SIZE - 10)
                xCoord -= (self.MEEPLE_SIZE - 15)
            elif meeple.edge == 1:
                yCoord -= (self.MEEPLE_SIZE - 10)
                xCoord += (self.MEEPLE_SIZE - 15)
            elif meeple.edge == 2:
                yCoord -= (self.MEEPLE_SIZE - 15)
                xCoord += (self.MEEPLE_SIZE - 10)
            elif meeple.edge == 3:
                yCoord += (self.MEEPLE_SIZE - 15)
                xCoord += (self.MEEPLE_SIZE - 10)
            elif meeple.edge == 4:
                yCoord += (self.MEEPLE_SIZE - 10)
                xCoord += (self.MEEPLE_SIZE - 15)
            elif meeple.edge == 5:
                yCoord -= (self.MEEPLE_SIZE - 10)
                xCoord -= (self.MEEPLE_SIZE - 15)
            elif meeple.edge == 6:
                yCoord -= (self.MEEPLE_SIZE - 15)
                xCoord -= (self.MEEPLE_SIZE - 10)
            elif meeple.edge == 7:
                yCoord -= (self.MEEPLE_SIZE - 15)
                xCoord -= (self.MEEPLE_SIZE - 10)


        return xCoord, yCoord

    def drawMeeple(self, canvas: tk.Canvas, board: Board, x, y, node: Node):
        coords = (node.x, node.y)
        
        if coords in board.meepled.keys():
            meeple: meepleInfo = board.meepled.get(coords)
            meepleImage = ImageTk.PhotoImage(Image.open(rf'Images/{meeple.color}.png').resize((self.MEEPLE_SIZE,self.MEEPLE_SIZE)))
            self.images.append(meepleImage)

            xCoord, yCoord = self.meepleOffset(board, x, y, meeple, node.tile)
            canvas.create_image(xCoord,yCoord, image=meepleImage)

        # if t.occupied is not None and t.occupied.occupiedBy is not None:
        #     color = t.occupied.occupiedBy.color
            
        #     meeple = ImageTk.PhotoImage(Image.open(rf'Images/{color}.png').resize((MEEPLE_SIZE,MEEPLE_SIZE)))
        #     images.append(meeple)
            
        #     xCoord, yCoord = meepleOffset(board, x, y, t)
        #     canvas.create_image(xCoord,yCoord, image=meeple)

    def drawTile(self, canvas: tk.Canvas, board: Board, x, y, node: Node):
        img = Image.open(rf'Images/tile-{node.tile.imgCode}.png')
        imgR = self.rotateImage(img, node.tile.orientation)
        imgTk = ImageTk.PhotoImage(imgR)
        self.images.append(imgTk)

        canvas.create_image((x - board.minX) * self.TILE_SIZE, (y - board.minY)* self.TILE_SIZE,image=imgTk)

        self.drawMeeple(canvas, board, x, y, node)
        #label.grid(column= x - board.minX, row= y - board.minY)
        

        #canvas.grid(column= x - board.minX, row= y - board.minY)

    def render3(self, board: Board, currTile: Tile, players: List[Player]):
        self.destroyFrames()
        for widget in self.canvas.winfo_children():
            widget.destroy()
        self.canvas.pack_forget()
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.top, width=1000, height=1000)
     
        del self.images
        self.images = []

        self.drawCurrTile(self.currTileFrame, currTile, players, board)
        self.drawCoordsY(self.gridFrameY, board)
        self.drawCoords(self.gridFrame, board)
        #frame.grid(column=3, row=3, rowspan=(board.maxY- board.minY), columnspan=(board.maxX - board.minX))
        self.canvas.grid(column=1, row=3, padx=40, pady=50)
        for item, node in board.board.items():
            self.drawTile(self.canvas, board, item[0], item[1], node)

        #can.create_rectangle(50,50,1010,1010,fill="red")

        #frame.grid(column=2, row=2, rowspan=(board.maxY- board.minY), columnspan=(board.maxX - board.minX))
        self.top.update()