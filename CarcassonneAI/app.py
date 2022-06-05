from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QSize, pyqtSignal, QObject
from Agents.Agent import Agent, HumanAgent
from Agents.MctsAgents import MCTS_Saver

from Game import Game
from Action import Action
from Feature import FeatType
import random

import sys
from functools import partial
import threading
import math



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.UIWIDTH, self.UIHEIGHT)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.menuWIDTH = 250
        self.menuPAD = 25
        self.menuX = self.UIWIDTH - self.menuWIDTH - self.menuPAD
        self.menuY = self.menuPAD

        subTitle = QFont("Times", 15)
        title = QFont("Times", 25)


        self.NewGameBtn = QtWidgets.QPushButton(self.centralwidget)
        self.NewGameBtn.setObjectName("NewGameBtn")
        self.NewGameBtn.setGeometry(self.menuX, self.menuY, self.menuWIDTH, 40)
        self.NewGameBtn.setText("Start New Game")
        self.NewGameBtn.clicked.connect(self.cleanup)

        self.rotateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.rotateBtn.setGeometry(QtCore.QRect(self.menuX - 175, 250, 100, 40))
        self.rotateBtn.setFont(QFont("Times",20))
        self.rotateBtn.setText("Rotate")

        currentTileTitle = QtWidgets.QLabel(self.centralwidget)
        currentTileTitle.setGeometry(self.menuX - 190, 25, 150, 80)
        currentTileTitle.setFont(QFont("Times",20))
        currentTileTitle.setText("Current Tile")


        self.randBtn = QtWidgets.QPushButton(self.centralwidget)
        self.randBtn.setGeometry(QtCore.QRect(self.menuX - 100, 210, 80, 23))
        self.randBtn.setObjectName("randBtn")
        self.randBtn.setText("Random")
        
        self.carcLogo = QtWidgets.QLabel(self.centralwidget)
        self.carcLogo.setGeometry(QtCore.QRect(15, 15, 300, 81))
        self.carcImg = QPixmap('Images/logo.png')
        self.carcLogo.setPixmap(self.carcImg)
        self.carcLogo.setScaledContents(True)

        self.scorePop = QtWidgets.QLabel(self.centralwidget)
        self.scorePop.setGeometry(350, 15, 800, 80)
        self.scorePop.setFont(title)
        self.scorePop.setText("")
        self.scorePop.setObjectName("ScoreBug")

        self.currTile = QtWidgets.QLabel(self.centralwidget)
        self.currTile.setGeometry(QtCore.QRect(self.menuX - 200, self.menuY + self.NewGameBtn.height() + self.menuPAD, 150, 150))
        self.currTile.setText("")
        self.currTile.setObjectName("currTile")
        self.currTile.setScaledContents(True)

        self.startTile = QtWidgets.QLabel(self.centralwidget)
        self.startTile.setGeometry(QtCore.QRect(260, 270, 71, 61))
        self.startTile.setText("")
        self.startTile.setObjectName("startTile")

        self.endScore = QtWidgets.QLabel(self.centralwidget)
        self.endScore.setGeometry(self.cX - 100, self.cY - 200, 600, 30)
        self.endScore.setFont(QFont("Times", 25))
        self.endScore.setStyleSheet("background-color: white")
        self.endScore.hide()

        self.endBtn = QtWidgets.QPushButton(self.centralwidget)
        self.endBtn.setFont(QFont("Time", 25))
        self.endBtn.setText("Play Again?")
        self.endBtn.setGeometry(self.cX - 50, self.cY - 100, 200, 50)
        self.endBtn.hide()
        self.endBtn.clicked.connect(self.cleanup)
   
        ####
        ####  RIGHT HAND MENUS
        ####

        nextFrameY =  self.menuY + self.NewGameBtn.height() + self.menuPAD
        #### SCOREBOARD
        self.ScoreFrame = QtWidgets.QFrame(self.centralwidget)
        self.ScoreFrame.setGeometry(QtCore.QRect(self.menuX, nextFrameY, self.menuWIDTH, 131))
        self.ScoreFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ScoreFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ScoreFrame.setObjectName("ScoreFrame")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.ScoreFrame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 201, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.ScoreBoard = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.ScoreBoard.setContentsMargins(0, 0, 0, 0)
        self.ScoreBoard.setObjectName("ScoreBoard")

        self.menu_Scoreboard = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.menu_Scoreboard.setText("Scoreboard")
        self.menu_Scoreboard.setFont(QFont("Times", 20))
        self.ScoreBoard.addWidget(self.menu_Scoreboard)
        self.ScoreLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ScoreLabel.setText("Score: Red 0 | Blue 0")
        self.ScoreLabel.setFont(subTitle)
        self.ScoreBoard.addWidget(self.ScoreLabel)
        self.TurnsLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.TurnsLabel.setText("Turns Remaining: 30")
        self.TurnsLabel.setFont(subTitle)
        self.ScoreBoard.addWidget(self.TurnsLabel)

        nextFrameY += self.ScoreFrame.height() + self.menuPAD
        ## MEEPLE STOCK
        self.MeeplesFrame = QtWidgets.QFrame(self.centralwidget)
        self.MeeplesFrame.setGeometry(QtCore.QRect(self.menuX, nextFrameY, self.menuWIDTH, 150))
        self.MeeplesFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MeeplesFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MeeplesFrame.setObjectName("MeeplesFrame")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.MeeplesFrame)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, self.menuWIDTH - 10, self.MeeplesFrame.height() - 10))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.ScoreBoard_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.ScoreBoard_4.setContentsMargins(0, 0, 0, 0)
        self.ScoreBoard_4.setObjectName("ScoreBoard_4")
        self.menu_Meeples_2 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.menu_Meeples_2.setText("Meeples Remaining")
        self.menu_Meeples_2.setFont(QFont("Times", 20))
        self.ScoreBoard_4.addWidget(self.menu_Meeples_2)
        self.redMeepLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.redMeepLabel.setText("7: ")
        self.redMeepLabel.setFont(QFont("Times", 15))
        self.ScoreBoard_4.addWidget(self.redMeepLabel)
        self.blueMeepLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.blueMeepLabel.setText("7: ")
        self.blueMeepLabel.setFont(QFont("Times", 15))
        self.ScoreBoard_4.addWidget(self.blueMeepLabel)

        nextFrameY += self.MeeplesFrame.height() + self.menuPAD
        ##### AGENT INFO
        self.AgentFrame = QtWidgets.QFrame(self.centralwidget)
        self.AgentFrame.setGeometry(QtCore.QRect(self.menuX, nextFrameY, self.menuWIDTH, 450))
        self.AgentFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.AgentFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.AgentFrame.setObjectName("AgentFrame")

        self.menu_Agent = QtWidgets.QLabel(self.AgentFrame)
        self.menu_Agent.setText("Peek into the Bot")
        self.menu_Agent.setFont(QFont("Times", 20))
        self.menu_Agent.setGeometry(10, 20, self.menuWIDTH - 10, 31)

        self.menu_Estimates = QtWidgets.QLabel(self.AgentFrame)
        self.menu_Estimates.setText("Current Best Estimates")
        self.menu_Estimates.setFont(subTitle)
        self.menu_Estimates.setGeometry(10, 60, self.menuWIDTH - 10, 20)


        self.firstBorder = QtWidgets.QLabel(self.AgentFrame)
        self.firstBorder.setGeometry(7, 87, 86, 86)
        self.firstBorder.setScaledContents(True)
        self.firstReal = QtWidgets.QLabel(self.centralwidget)
        self.firstReal.setScaledContents(True)
        self.firstReal.setPixmap(self.orange)
        self.firstReal.setGeometry(0,0,80,80)
        self.firstReal.hide()

        self.secondBorder = QtWidgets.QLabel(self.AgentFrame)
        self.secondBorder.setGeometry(7, 182, 86, 86)
        self.secondBorder.setScaledContents(True)
        self.secondReal = QtWidgets.QLabel(self.centralwidget)
        self.secondReal.setScaledContents(True)
        self.secondReal.setPixmap(self.purple)
        self.secondReal.setGeometry(0,0,80,80)
        self.secondReal.hide()

        self.thirdBorder = QtWidgets.QLabel(self.AgentFrame)
        self.thirdBorder.setGeometry(7, 272, 86, 86)
        self.thirdBorder.setScaledContents(True)
        self.thirdReal = QtWidgets.QLabel(self.centralwidget)
        self.thirdReal.setScaledContents(True)
        self.thirdReal.setPixmap(self.green)
        self.thirdReal.setGeometry(0,0,80,80)
        self.thirdReal.hide()

        self.First = QtWidgets.QLabel(self.AgentFrame)
        self.First.setText("First")
        self.First.setGeometry(10, 90, 80, 80)
        self.First.setScaledContents(True)
        self.FirstScore = QtWidgets.QLabel(self.AgentFrame)
        self.FirstScore.setGeometry(100, 130, 80, 20)

        self.Second = QtWidgets.QLabel(self.AgentFrame)
        self.Second.setText("Second")
        self.Second.setGeometry(10, 185, 80, 80)
        self.Second.setScaledContents(True)
        self.SecondScore = QtWidgets.QLabel(self.AgentFrame)
        self.SecondScore.setGeometry(100, 225, 80, 20)

        self.Third = QtWidgets.QLabel(self.AgentFrame)
        self.Third.setText("Third")
        self.Third.setGeometry(10, 275, 80, 80)
        self.Third.setScaledContents(True)
        self.thirdScore = QtWidgets.QLabel(self.AgentFrame)
        self.thirdScore.setGeometry(100, 315, 80, 20)

        self.estimateScores = [self.FirstScore, self.SecondScore, self.thirdScore]
        self.estimateLabels = [self.First, self.Second, self.Third]
        self.estimateMeeples = [QtWidgets.QLabel(self.AgentFrame) for x in range(3)]
        self.estimateLocs = [self.firstReal, self.secondReal, self.thirdReal]

        self.menu_progress = QtWidgets.QLabel(self.AgentFrame)
        self.menu_progress.setText("Evaluation Progress")
        self.menu_progress.setFont(subTitle)
        self.menu_progress.setGeometry(10, 360, self.menuWIDTH - 20, 25)

        self.progressBar = QtWidgets.QProgressBar(self.AgentFrame)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setGeometry(10, 400, self.menuWIDTH - 20, 23)

        progInfo = QtWidgets.QLabel(self.AgentFrame)
        progInfo.setText("10% Represents 1250 Iterations")
        progInfo.setGeometry(20, 425, self.menuWIDTH - 20, 20)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 810, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        


    def init(self):
        app = QApplication(sys.argv)
        app.setFont(QFont('Times'))
        win = QMainWindow()

        self.orange = QPixmap('Images/orange.png')
        self.purple = QPixmap('Images/purple.png')
        self.green = QPixmap('Images/green.png')

        self.UIWIDTH = 1900
        self.UIHEIGHT = 950
        self.cX = 750
        self.cY = 500

        self.setupUi(win)
        self.retranslateUi(win)

  
        self.tileSize = 80
        self.halfSize = int(self.tileSize / 2)
        self.meepleSize = 40
        self.halfMeeple = int(self.meepleSize / 2)

        self.randBtn.clicked.connect(self.randPlay)
        self.randBtn.hide()
        self.rotateBtn.clicked.connect(self.rotate)

        self.agent = Agent()
        self.agent.res.connect(self.agentPlay)
        self.agent.best.connect(self.trackProgress)

 

        self.newGame()

        win.show()
        sys.exit(app.exec_())

    def cleanup(self):
        for lb in self.tileLabels:
            lb.setParent(None)
            del lb
        self.tileLabels = []

        for loc, lb in self.meepleLabels.items():
            lb.hide()
        self.meepleLabels = {}

        for lb in self.tilePlaceBtns:
            lb.setParent(None)
            del lb
        self.tilePlaceBtns = []

        for lb in self.meeplePlaceBtns:
            lb.setParent(None)
            del lb
        self.meeplePlaceBtns = []

        for lb in self.redMeepStock:
            lb.setParent(None)
            del lb
        self.redMeepStock = []

        for lb in self.blueMeepStock:
            lb.setParent(None)
            del lb
        self.blueMeepStock = []

        self.newGame()


    def newGame(self):
        self.endScore.setText("")
        self.endScore.hide()
        self.endBtn.hide()
        self.rotateBtn.setEnabled(True)
        self.ScoreLabel.setText("Score: Red 0 | Blue 0")
        self.TurnsLabel.setText("Turns Remaining: 22")


        ### BOARD TILE REFS
        self.tileLabels = []
        self.meepleLabels = {}

        ## TILE PLACEMENT REFS
        self.tilePlaceBtns = []
        self.meeplePlaceBtns = []

        self.game = Game(players=[HumanAgent(), MCTS_Saver(info='Heuristic')])
        #self.game = Game(players=[HumanAgent(), HumanAgent()], order=[24,20,13,6,53,56,18])
        self.game.state.turn = 50
        self.currentOrientation = 0

        self.drawTile(0,0,self.game.state.board.board[(0,0)].tile)
        self.tileLocations()
        self.drawCurrTile()
        self.createMeepleStock()
        self.updateMeeples()

    def endGame(self):
        self.rotateBtn.setEnabled(False)
        fscore = self.game.finalScore()
        self.endScore.setText(f"Final Score:   Red  {fscore[0]}  |  Blue  {fscore[1]}")
        self.endScore.show()
        self.endScore.raise_()
        self.endBtn.show()
        self.endBtn.raise_()

    #### UI REMOVERS
    def popTile(self):
        lb = self.tileLabels.pop()
        lb.setParent(None)
        del lb

    def delPlaceTiles(self):
        for btn in self.tilePlaceBtns:
            btn.setParent(None)
        self.tilePlaceBtns = []

    def delPlaceMeeples(self):
        for btn in self.meeplePlaceBtns:
            btn.setParent(None)
        self.meeplePlaceBtns = []

    def randPlay(self):
        actions = self.game.getActions()
        action = random.choice(actions)
        ## add tile and meeple to board
        self.drawTile(action.x, action.y, action.tile)
        if action.meeple:
            self.drawMeeple(action.x, action.y, action.feature)
        
        ## apply action
        self.playTile(action)

    #### BOARD DRAWS
    def drawTile(self, x, y, tile):
        tileLabel = QtWidgets.QLabel(self.centralwidget)
        tileLabel.setGeometry(self.cX+(x*self.tileSize), self.cY+(y*self.tileSize), self.tileSize, self.tileSize)
        tileImage = QPixmap(rf'Images/tile-{tile.imgCode}.png').transformed(QtGui.QTransform().rotate(90 * tile.orientation))
        tileLabel.setPixmap(tileImage)
        tileLabel.setScaledContents(True)
        self.tileLabels.append(tileLabel)
        tileLabel.show()

    def drawMeeple(self, x, y, feature):
        print(feature)
        mx = self.cX + (self.tileSize*x) + self.halfSize - self.halfMeeple
        my = self.cY + (self.tileSize*y) + self.halfSize - self.halfMeeple

        col = 'red' if self.game.state.currentPlayer == 0 else 'blue'
        
        SHORT = 15
        LONG = 22
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
        
        
        meepleLabel = QtWidgets.QLabel(self.centralwidget)
        meepleLabel.setGeometry(mx,my,self.meepleSize, self.meepleSize)
        
        meepleImage = QPixmap(rf'Images/{col}.png')
        if feature.featType == FeatType.GRASS:
            meepleImage = meepleImage.transformed(QtGui.QTransform().rotate(90))
        meepleLabel.setPixmap(meepleImage)
        meepleLabel.setScaledContents(True)     
        self.meepleLabels[(x,y)] = meepleLabel
        meepleLabel.show()

    def removeMeeples(self, removed):
        for loc in removed:
            self.meepleLabels.get(loc).setHidden(True)

    #### MENU DRAWS
    def drawCurrTile(self):
        tile = self.game.state.currentTile[self.currentOrientation]
        tileImg = QPixmap(rf'Images/tile-{tile.imgCode}.png').transformed(QtGui.QTransform().rotate(90 * tile.orientation))
        self.currTile.setPixmap(tileImg)

    def rotate(self):
        self.currentOrientation = (self.currentOrientation + 1) % len(self.game.state.currentTile)
        self.drawCurrTile()
        self.delPlaceTiles()
        self.tileLocations()

    def checkScore(self, prev, curr):
        if curr != prev:
            if curr[0] > prev[0] and curr[1] > prev[1]:
                txt = f"Score! Red earned {curr[0]-prev[0]} and Blue earned {curr[1]-prev[1]} points!"        
            elif curr[0] > prev[0] and curr[1] == prev[1]:
                txt = f'Score! Red earned {curr[0]-prev[0]} points!'
            elif curr[0] == prev[0] and curr[1] > prev[1]:
                txt = f'Score! Blue earned {curr[1]-prev[1]} points!'
            
            self.scorePop.setText(txt)
            self.scorePop.setHidden(False)
            self.ScoreLabel.setText(f'Score: Red {curr[0]} | Blue {curr[1]}')
            QtCore.QTimer.singleShot(4000, lambda: self.scorePop.setHidden(True))

    def createMeepleStock(self):
        self.redMeepStock = []
        self.redMeep = QPixmap('Images/red.png')
        self.blueMeepStock = []
        self.blueMeep = QPixmap('Images/blue.png')

        mx = self.menuX + self.meepleSize
        my = self.MeeplesFrame.y() + 60

        for i in range(self.game.state.players[0].meepleCount):
            mStock = QtWidgets.QLabel(self.centralwidget)
            mStock.setGeometry(mx + (self.halfMeeple) * i, my, self.meepleSize, self.meepleSize)
            mStock.setPixmap(self.redMeep)
            mStock.setScaledContents(True)
            self.redMeepStock.append(mStock)
        
        my = self.MeeplesFrame.y() + 65 + self.meepleSize
        for i in range(self.game.state.players[1].meepleCount):
            mStock = QtWidgets.QLabel(self.centralwidget)
            mStock.setGeometry(mx + (self.halfMeeple) * i, my, self.meepleSize, self.meepleSize)
            mStock.setPixmap(self.blueMeep)
            mStock.setScaledContents(True)
            self.blueMeepStock.append(mStock)

    def updateMeeples(self):
        for i in range(7):
            self.redMeepStock[i].setHidden(True)
            self.blueMeepStock[i].setHidden(True)
        for i in range(self.game.state.players[0].meepleCount):
            self.redMeepStock[i].setHidden(False)
        for i in range(self.game.state.players[1].meepleCount):
            self.blueMeepStock[i].setHidden(False)
        
        self.redMeepLabel.setText(f"{self.game.state.players[0].meepleCount}: ")
        self.blueMeepLabel.setText(f"{self.game.state.players[1].meepleCount}: ")



        # self.carcLogo = QtWidgets.QLabel(self.centralwidget)
        # self.carcLogo.setGeometry(QtCore.QRect(15, 15, 300, 81))
        # self.carcImg = QPixmap('Images/logo.png')
        # self.carcLogo.setPixmap(self.carcImg)
        # self.carcLogo.setScaledContents(True)

    ### GAMEPLAY LOGIC LOOP
    def startTurn(self):
        self.delPlaceTiles()
        self.delPlaceMeeples()

        self.drawCurrTile()
        self.TurnsLabel.setText(f"Turns Remaining: {72 - self.game.state.turn}")
        self.updateMeeples()

        if self.game.currentPlayer().agent.type == 'Human':
            self.tileLocations()
        else:
            self.progressBar.setValue(0)
            self.rotateBtn.setEnabled(False)
            self.NewGameBtn.setEnabled(False)
            self.stats = []
            self.currentActions = self.game.getActions()
            threading.Thread(target=lambda: self.agent.agentResponse(self.game)).start()

    
    def tileLocations(self):
        self.rotateBtn.setEnabled(True)
        validActions = [action for action in self.game.getActions() if action.tile.orientation == self.currentOrientation and action.meeple is False]
    
        for action in validActions:
            placeBtn = QtWidgets.QPushButton(self.centralwidget)
            placeBtn.setGeometry(self.cX+(action.x*self.tileSize), self.cY+(action.y*self.tileSize), self.tileSize, self.tileSize)
            #placeBtn.setText(f"{action.x}, {action.y}")
            placeBtn.clicked.connect(partial(self.placeTile, action))
            self.tilePlaceBtns.append(placeBtn)
            placeBtn.show()

    def placeTile(self, action):
        self.drawTile(action.x, action.y, action.tile)
        self.delPlaceTiles()
        self.rotateBtn.setEnabled(False)

        meepleActions = [act for act in self.game.getActions() if act.tile.orientation == action.tile.orientation and act.x == action.x and act.y == action.y and act.meeple]
        for mAction in meepleActions:
            meepX = self.cX + (action.x*self.tileSize) + self.halfSize - self.halfMeeple
            meepY = self.cY + (action.y*self.tileSize) + self.halfSize - self.halfMeeple

            if mAction.feature.featType == FeatType.GRASS:
                edge = mAction.feature.edges[0]
                if edge == 7 or edge == 0:
                    meepX -= (self.halfSize - 10)
                    meepY -= (self.halfSize - 10)
                elif edge == 1 or edge == 2:
                    meepX += (self.halfSize - 10)
                    meepY -= (self.halfSize - 10)
                elif edge == 3 or edge == 4:
                    meepX += (self.halfSize - 10)
                    meepY += (self.halfSize - 10)
                else:
                    meepX -= (self.halfSize - 10)
                    meepY += (self.halfSize - 10)
            elif mAction.feature.featType == FeatType.CITY or mAction.feature.featType == FeatType.ROAD:
                edge = mAction.feature.edges[0]
                if edge == 0:
                    meepY -= self.halfSize
                elif edge == 1:
                    meepX += self.halfSize
                elif edge == 2:
                    meepY += self.halfSize
                else:
                    meepX -= self.halfSize


            placeMeeple = QtWidgets.QPushButton(self.centralwidget)
            placeMeeple.setGeometry(meepX, meepY, self.meepleSize, self.meepleSize)

            placeMeeple.setFlat(True)
            placeMeeple.setStyleSheet("QPushButton { background-color: transparent }")
            placeMeeple.setIcon(QtGui.QIcon('Images/place.png'))
            placeMeeple.setIconSize(QSize(self.meepleSize + 15, self.meepleSize + 15))

            placeMeeple.clicked.connect(partial(self.playTile, mAction))

            self.meeplePlaceBtns.append(placeMeeple)
            placeMeeple.show()

        placeMeeple = QtWidgets.QPushButton(self.centralwidget)
        placeMeeple.setGeometry(self.cX + (action.x*self.tileSize) + self.tileSize, self.cY + (action.y*self.tileSize) + self.tileSize, self.meepleSize, self.meepleSize)
        placeMeeple.setFlat(True)
        placeMeeple.setStyleSheet("QPushButton { background-color: transparent }")
        placeMeeple.setIcon(QtGui.QIcon('Images/noMeeple.png'))
        placeMeeple.setIconSize(QSize(self.meepleSize, self.meepleSize))

        placeMeeple.clicked.connect(partial(self.playTile, action))

        self.meeplePlaceBtns.append(placeMeeple)
        placeMeeple.show()

        cancelTile = QtWidgets.QPushButton(self.centralwidget)
        cancelTile.setGeometry(self.cX + (action.x*self.tileSize) - self.halfSize, self.cY + (action.y*self.tileSize) + self.tileSize, self.meepleSize, self.meepleSize)
        cancelTile.setFlat(True)
        cancelTile.setStyleSheet("QPushButton { background-color: transparent }")
        cancelTile.setIcon(QtGui.QIcon('Images/cancelTile.png'))
        cancelTile.setIconSize(QSize(self.meepleSize, self.meepleSize))

        cancelTile.clicked.connect(partial(self.cancelTile, cancelTile))

        self.meeplePlaceBtns.append(cancelTile)
        cancelTile.show()

    def cancelTile(self, cancelBtn):
        self.popTile()
        self.startTurn()


    def playTile(self, action):
        if action.meeple:
            self.drawMeeple(action.x, action.y, action.feature)

        prevScore = self.game.getScore()
        removed = self.game.applyAction(action)
        newScore = self.game.getScore()
        self.checkScore(prevScore, newScore)
        self.removeMeeples(removed)
        self.currentOrientation = 0

        if self.game.gameOver():
            self.endGame()
        else:
            self.startTurn()

    def agentPlay(self, action):
        self.rotateBtn.setEnabled(True)
        self.NewGameBtn.setEnabled(True)
        self.drawTile(action.x, action.y, action.tile)
        QtCore.QTimer.singleShot(3000, lambda: [estimateLoc.hide() for estimateLoc in self.estimateLocs])
        self.playTile(action)

    def trackProgress(self, info):
        self.stats.append(info)

        rank = []
        self.bestAgentMeeples = []

        self.progressBar.setValue(self.progressBar.value() + 20)
    
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
            act = self.currentActions[ind]
            self.drawBestTile(act, i)
            #self.bestAgentInfos[i].configure(text="Score: {:0.2f}".format((rank[ind])))
            self.estimateScores[i].setText("Score: {:0.2f}".format((rank[ind])))
            rank[ind] = -math.inf
        print(max(rank))

    def drawBestTile(self, action, polePos):
        self.firstBorder.setPixmap(self.orange)
        self.secondBorder.setPixmap(self.purple)
        self.thirdBorder.setPixmap(self.green)

        self.estimateLocs[polePos].setGeometry(self.cX + action.x * (self.tileSize) + (2 * polePos), self.cY + action.y * (self.tileSize) + (2 * polePos), self.tileSize - (4*polePos), self.tileSize - (4*polePos))
        self.estimateLocs[polePos].show()

        img = QPixmap(f'Images/tile-{action.tile.imgCode}.png').transformed(QtGui.QTransform().rotate(90 * action.tile.orientation))
        self.estimateLabels[polePos].setPixmap(img)
        meep = self.blueMeep

        if action.meeple is False:
            self.estimateMeeples[polePos].setHidden(True)
        else:
            mx = self.estimateLabels[polePos].x() + self.halfMeeple
            my = self.estimateLabels[polePos].y() + self.halfMeeple

            feature = action.feature
            SHORT = 15
            LONG = 22
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
                meep = meep.transformed(QtGui.QTransform().rotate(90))
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

            self.estimateMeeples[polePos].setScaledContents(True)
            self.estimateMeeples[polePos].setGeometry(mx, my, self.meepleSize, self.meepleSize)
            self.estimateMeeples[polePos].setPixmap(meep)
            self.estimateMeeples[polePos].setHidden(False)
            self.estimateMeeples[polePos].raise_()



class Agent(QObject):
    res = pyqtSignal(Action)
    best = pyqtSignal(list)
    #### AGENT TURN
    def agentResponse(self, game):

        # self.rotateBtn.setEnabled(False)
        # self.NewGameBtn.setEnabled(False)

        self.stats = []
        self.bestAgentTiles = []
        self.currentActions = game.getActions()


        
        ## The call to the agent
        response = game.currentPlayer().agent.getResponse(self.trackProgress,game,game.currentPlayerId())
        
        # self.rotateBtn.setEnabled(True)
        # self.NewGameBtn.setEnabled(True)
        self.res.emit(response)

    def trackProgress(self, info):
        self.best.emit(info)

    


main = Ui_MainWindow()
main.init()
