import math
import numpy
from src import MapTile


class AllIsWaterMap:
    def __init__(self):
        self.listOfMapTiles = []
        self.xSize = 260
        self.ySize = 140
        a = 1
        self.xSizeMap = int((self.xSize - a * math.sqrt(3) / 2) / (a * math.sqrt(3)))
        self.ySizeMap = int(self.ySize / (3 * a)*2)
        for i in range(self.xSizeMap):
            lineMapTiles=[]
            for j in range(self.ySizeMap):
                mapTile=self.createTile(i, j, a)
                lineMapTiles.append(mapTile)
            self.listOfMapTiles.append(lineMapTiles)
        self.createNeighbourhood()


    def getXSizeMap(self):
        return self.xSizeMap
    def getYSizeMap(self):
        return self.ySizeMap
    def getListOfMapTiles(self):
        return self.listOfMapTiles
    def getTile(self,i,j):
        return self.listOfMapTiles[i][j]
    def getNeighboursByCoords(self, x, y):
        return self.getTile(x, y).getNeighbours()

    def getNeighbours(self, tile):
        return tile.getNeighbours()

    def createTile(self,x,y,a):
        if y % 2 == 0:
            startX = 1.5 * a + a * math.sqrt(3) * x
        else:
            startX = 1.5 * a + a * math.sqrt(3) / 2 + a * math.sqrt(3) * x
        startY = 1.5 * a + 1 / 2 * a + 1.5 * y * a
        angle = 60
        coords = []
        for i in range(1, 7):
            coords.append([int(startX), int(startY)])
            endX = startX + a * math.sin(math.radians(angle * i))
            endY = startY + a * math.cos(math.radians(angle * i))
            startX = endX
            startY = endY
            type=0
        return MapTile.MapTile(x,y,0)


    def createNeighbourhood(self):
        for i in range(self.xSizeMap-1):
            for j in range(self.ySizeMap-1):
                self.setNeighbours(self.listOfMapTiles[i][j])

    def setNeighbours(self, tile):
        x = tile.getX()
        y = tile.getY()
        neighbours = []
        if y % 2 == 0:
            if x > 0:
                neighbours.append(self.getTile(x - 1, y))
                if y > 0: neighbours.append(self.getTile(x - 1, y - 1))
                if y < self.ySize - 1: neighbours.append(self.getTile(x - 1, y + 1))
            if x < self.xSize - 1: neighbours.append(self.getTile(x + 1, y))
            if y > 0: neighbours.append(self.getTile(x, y - 1))
            if y < self.ySize - 1: neighbours.append(self.getTile(x, y + 1))
        else:
            if x > 0: neighbours.append(self.getTile(x - 1, y))
            if y > 0: neighbours.append(self.getTile(x, y - 1))
            if y < self.ySize - 1: neighbours.append(self.getTile(x, y + 1))
            if x < self.xSize - 1:
                neighbours.append(self.getTile(x + 1, y))
                if y > 0: neighbours.append(self.getTile(x + 1, y - 1))
                if y < self.ySize - 1: neighbours.append(self.getTile(x + 1, y + 1))
        tile.setNeighbours(neighbours)


