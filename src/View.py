from src import SpreadingLogic
from src import AllIsWaterMap
from tkinter import *
import math


class Tile:
    def __init__(self, mapTile, index):
        self.mapTile =mapTile
        self.index_ = index

class View(Tk):
    def __init__(self, tilesMap):
        Tk.__init__(self)
        self.oilHex_=[]
        self.hexagons = []
        self.biggestTileX = 1100
        self.biggestTileY = 850
        self.infoId = 0
        self.canvas = Canvas(width=1920, height=1080, bg="#AFEEEE")
        self.canvas.pack()
        self.a_ = 4
        self.tilesMap_ = tilesMap
        self.Sleep = 1
        self.Pause=False
        self.drawMap()
        self.setInitialTile(self.tilesMap_.getTile(125,75))

    def setInitialTile(self,mapTile):
        mapTile.setOilDensity(835)
        mapTile.setOilThickness(3000)
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
        self.doChanges()


    def fromRGB(self, R, G, B):
        return "#%02x%02x%02x" % (R, G, B)

    def drawTile(self, mapTile):
        if mapTile is None:
            return
        colors = [
            "#F3D804",
            "#0000FF"

        ]
        oilColors=[
            "#000000"
            "#1b1b20"
            "#2b2b3a"
            "#34344e"
            "#3b3b69"
            "#3a3a7e"
            "#3131ab"
            "#2c2cc2"
            "#1616e6"
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
            color = colors[1]
        else:
            color = oilColors[0]

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


    def getHexagon(self,mapTile):
        for hex in self.hexagons:
            if (hex.mapTile==mapTile):
                return hex

    def changeTileColor(self,mapTile):
        self.canvas.itemconfig(self.getHexagon(mapTile).index_, fill='red')



    def isInOilHex(self,tile):
        for t in self.oilHex_:
            if (t==tile):
                return True
        return False

    def doChanges(self):
        oilChanges = []
        for c in self.oilHex_:
            changedTiles = c.mapTile.doMove()
            if changedTiles is not None:
                for t in changedTiles:
                     oilChanges.append(t[0])
                     self.changeTileColor(t[0])
        self.canvas.update()
        if oilChanges is not None:
            self.oilHex_=[]
            for t in oilChanges:
                if not self.isInOilHex(self.getHexagon(t)):
                    self.oilHex_.append(self.getHexagon(t))
        if self.Pause is False:
            self.canvas.after(self.Sleep, self.doChanges)


map=AllIsWaterMap.AllIsWaterMap()
#map =Map.Map()
slogic = SpreadingLogic.SpreadingLogic(map)
view = View(map)
view.mainloop()
