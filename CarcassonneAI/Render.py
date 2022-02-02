from Board import Board

def render(board : Board):
    minX = maxX = minY = maxY = 0
    currX = currY = 0

    for key, value in board.board.items():
        # an artifact of frozen sets removing duplicates
        currX = key[0]
        currY = key[1]

        if minX > currX:
            minX = currX
        if maxX < currX:
            maxX = currX
        if minY > currY:
            minY = currY
        if maxY < currY:
            maxY = currY

    
    print(list(range(minX - 1, maxX + 2)))
    for y in range(minY -1, maxY + 2):
        output = ""
        for x in range(minX -1, maxX +2):
            printingCoord = (x, y)
            node = board.board.get(printingCoord)
            if node is None:
                output += " _ "
            else:
                output += " " + str(node.tile.id) + " "
        print(output)
            
        