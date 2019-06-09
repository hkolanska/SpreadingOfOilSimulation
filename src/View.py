from src import SpreadingLogic
from src import AllIsWaterMap
from src import Map

from tkinter import *
import math


class Tile:
    def __init__(self, mapTile, index):
        self.mapTile = mapTile
        self.index_ = index


class View(Tk):
    def __init__(self, tilesMap):
        Tk.__init__(self)
        self.oilHex_ = []
        self.hexagons = []
        self.biggestTileX = 1900
        self.biggestTileY = 1000
        self.infoId = 0
        self.oilColors = [
            "black",
            "gray13",
            "gray26",
            "gray39",
            "gray50",
            "gray60",
            "gray66",
        ]
        self.canvas = Canvas(width=1920, height=1080, bg="#AFEEEE")
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.getTileByXY)
        self.a_ = 4.5
        self.tilesMap_ = tilesMap
        self.Sleep = 100
        self.initialTile = self.tilesMap_.getTile(125, 90)
        self.Pause = False
        self.theBiggestDistance = 0
        self.iterationNumber = 1
        self.drawMap()

        buttonBG4 = self.canvas.create_rectangle(1670, 680, 1730, 720, fill="grey40", outline="grey60")
        buttonTXT4 = self.canvas.create_text(1700, 700, text="Pause")
        self.canvas.tag_bind(buttonBG4, "<Button-1>", self.pause)
        self.canvas.tag_bind(buttonTXT4, "<Button-1>", self.pause)


    def setInitialTile(self, mapTile):
        mapTile.setOilDensity(835)
        mapTile.setOilThickness(5000)
        self.oilHex_.append(self.getHexagon(mapTile))

    def drawMap(self):
        map = self.tilesMap_
        xSize = map.getXSizeMap()
        ySize = map.getYSizeMap()
        if ySize % 2 == 0:
            yHeight = ySize * 1.5
        else:
            yHeight = math.ceil(ySize / 2) * 2 + ySize // 2
        xHeight = (2 * xSize + 1) * math.sqrt(3) / 2
        for i in range(xSize):
            for j in range(ySize):
                self.drawTile(map.getTile(i, j))
        self.setInitialTile(self.initialTile)
        self.drawTile(map.getTile(self.initialTile.getX(), self.initialTile.getY()))
        self.doChanges()

    def fromRGB(self, R, G, B):
        return "#%02x%02x%02x" % (R, G, B)

    def drawTile(self, mapTile):
        if mapTile is None:
            return
        colors = [
            "yellow",
            "blue",
            "red"

        ]

        tileCoords = mapTile.getCoords()
        if tileCoords[1] % 2 == 0:
            startX = 1.5 * self.a_ + self.a_ * math.sqrt(3) * tileCoords[0]
        else:
            startX = 1.5 * self.a_ + self.a_ * math.sqrt(3) / 2 + self.a_ * math.sqrt(3) * tileCoords[0]
        startY = 1.5 * self.a_ + 1 / 2 * self.a_ + 1.5 * tileCoords[1] * self.a_
        angle = 60
        coords = []
        for i in range(1, 7):
            coords.append([startX, startY])
            endX = startX + self.a_ * math.sin(math.radians(angle * i))
            endY = startY + self.a_ * math.cos(math.radians(angle * i))
            startX = endX
            startY = endY
        if mapTile.getOilThickness_() == 0:
            if mapTile.type_==0:
                color = colors[1]
            elif mapTile.type_==2:
                color = colors[2]
            else:
                color=colors[0]
        else:
            color = self.oilColors[0]

        index = self.canvas.create_polygon(coords[0][0],
                                           coords[0][1],
                                           coords[1][0],
                                           coords[1][1],
                                           coords[2][0],
                                           coords[2][1],
                                           coords[3][0],
                                           coords[3][1],
                                           coords[4][0],
                                           coords[4][1],
                                           coords[5][0],
                                           coords[5][1],
                                           fill=color,
                                           outline="gray"
                                           )
        for i in coords:
            if i[0] > self.biggestTileX:
                self.biggestTileX = i[0]
            if i[1] > self.biggestTileY:
                self.biggestTileY = i[1]



        hex = Tile(mapTile, index)
        self.hexagons.append(hex)

    def pause(self,event):
        if self.Pause is not True:
            self.Pause=True
        else:
            self.Pause=False
            self.doChanges()
    def getHexagon(self, mapTile):
        for hex in self.hexagons:
            if (hex.mapTile == mapTile):
                return hex

    def getHexagonByIndex(self, nearest):
        for i in self.hexagons:
            if i.index_ == nearest:
                return i
        return None
    def changeTileColor(self, mapTile):
        if mapTile.getOilThickness_!=0:
            self.canvas.itemconfig(self.getHexagon(mapTile).index_, fill=self.oilColors[3])

    def isInOilHex(self, tile):
        for t in self.oilHex_:
            if (t == tile):
                return True
        return False

    def doChanges(self):
        self.Sleep = 1000-self.iterationNumber
        if self.Sleep<2:
            self.Sleep=1
        oilChanges = []
        self.iterationNumber+=1
        for c in self.oilHex_:
            changedTiles = c.mapTile.doMove(self.iterationNumber/2, self.initialTile)
            if changedTiles is not None:
                for t in changedTiles:
                    if t[0].oilThickness_ > 0 and t[0].type_==0:
                        oilChanges.append(t[0])
                        self.changeTileColor(t[0])
            self.canvas.update()
        if oilChanges is not None:
            for t in oilChanges:
                if not self.isInOilHex(self.getHexagon(t)):
                    self.oilHex_.append(self.getHexagon(t))
        sumOfOil=0
        for c in self.oilHex_:
            sumOfOil+=c.mapTile.getOilThickness_()+c.mapTile.almostSpreaded
        print(sumOfOil)

        if self.Pause is False:
            self.canvas.after(self.Sleep, self.doChanges)

    def showTileDetails(self, tile):
        self.canvas.delete(self.infoId)
        onscreen = "Distance from \ninitial tile (65,40):\n(" + str(tile.mapTile.getX()) + "," + str(tile.mapTile.getY()) + ")\n"+ str(tile.mapTile.distance(self.initialTile))+" " + str(len(tile.mapTile.neighbours))+" \n"+str(tile.mapTile.getOilThickness_())
        self.infoId = self.canvas.create_text((1700, 20), anchor="nw", font=("helvetica", 12), text=onscreen)

    def getTileByXY(self, event):
         nearest = int(self.canvas.find_closest(event.x,event.y)[0])
         tile = self.getHexagonByIndex(nearest)
         if tile:
             self.showTileDetails(tile)

map =Map.Map()
view = View(map)
view.mainloop()