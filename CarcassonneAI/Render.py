from Board import Board, Node
from Feature import *
from Tile import Tile, rotate

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





top = tk.Tk()
top.geometry("800x800")
currTileFrame = tk.Frame(top)
gridFrame = tk.Frame(top)
gridFrameY = tk.Frame(top)
frame = tk.Frame(top)


def destroyFrames():
    for widgets in frame.winfo_children():
        widgets.destroy()
    frame.pack_forget()
    for widgets in gridFrameY.winfo_children():
        widgets.destroy()
    gridFrameY.pack_forget()
    for widgets in currTileFrame.winfo_children():
        widgets.destroy()
    currTileFrame.pack_forget()
    for widgets in gridFrame.winfo_children():
        widgets.destroy()
    gridFrame.pack_forget()


def drawCurrTile(root, currTile: Tile):
    img = Image.open(rf'Images/tile-{currTile.imgCode}.png')
    imgTk = ImageTk.PhotoImage(img)
    label = tk.Label(root, text="Current Tile:")
    label.grid(column=0, row=0, padx=10, sticky='w')

    # create the label for the current tile image
    labelImg = tk.Label(root, image=imgTk)
    labelImg.img = imgTk
    labelImg.grid(column=1, row=0)

def drawCoordsY(root, board: Board):
    for y in range(board.minY, board.maxY + 1):
        label = tk.Label(root, text=f'{y}')
        label.grid(column=0, row=y - board.minY, pady=40, sticky='w')

def drawCoords(root, board: Board):
    for x in range(board.minX, board.maxX+1):
        label = tk.Label(root, text=f'{x}')
        label.grid(row=0, column=x - board.minX, padx=40, sticky='n')

def rotateImage(img, orientation):
    if orientation == 0:
        return img
    if orientation == 1:
        return img.rotate(270)
    if orientation == 2:
        return img.rotate(180)
    if orientation == 3:
        return img.rotate(90)

def drawTile(root, board: Board, x, y, node: Node):
    img = Image.open(rf'Images/tile-{node.tile.imgCode}.png')
    imgR = rotateImage(img, node.tile.orientation)
    imgTk = ImageTk.PhotoImage(imgR)
    label = tk.Label(root, image = imgTk)
    label.img = imgTk

    label.grid(column= x - board.minX, row= y - board.minY)

def render3(board: Board, currTile:  Tile):
    destroyFrames()

    drawCurrTile(currTileFrame, currTile)
    drawCoords(gridFrame, board)
    drawCoordsY(gridFrameY, board)
    for item, node in board.board.items():
        drawTile(frame, board, item[0], item[1], node)
    
    currTileFrame.grid(row=0, column=0,pady=10)
    gridFrameY.grid(column=0, row=2,padx=10, rowspan=(board.maxY- board.minY))
    gridFrame.grid(column=2, row=1,pady=10, columnspan=(board.maxX - board.minX))
    frame.grid(column=2, row=2, rowspan=(board.maxY- board.minY), columnspan=(board.maxX - board.minX))
    top.update()