import cv2
import math
import numpy
from src import MapTile


class Map:
    def __init__(self):
        self.listOfMapTiles = []
        img = cv2.imread('..\PNGs\gulfMapGimpBW.png')
        xSize = 1100
        ySize = 850
        a = 5
        self.xSizeMap = int((xSize - a * math.sqrt(3) / 2) / (a * math.sqrt(3)))
        self.ySizeMap = int(ySize / (3 * a)*2)
        for i in range(self.xSizeMap):
            lineMapTiles=[]
            for j in range(self.ySizeMap):
                mapTile=self.createTile(i, j, a, img)
                lineMapTiles.append(mapTile)
            self.listOfMapTiles.append(lineMapTiles)
        self.createNeighbourhood



    def getXSizeMap(self):
        return self.xSizeMap
    def getYSizeMap(self):
        return self.ySizeMap
    def getListOfMapTiles(self):
        return self.listOfMapTiles
    def getTile(self,i,j):
        return self.listOfMapTiles[i][j]

    def createTile(self,x,y,a,img):
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
        water=0
        land=0
        for k in coords:
            if k[1]>=850:
                continue
            if k[0]>=1100:
                continue
            if numpy.all([img[k[0]][k[1]],[255,255,255]]):
                water+=1
            else:
                land+=1
        if land<water:
            type=1
        else:
            type=0
        return MapTile.MapTile(x,y,type)

    def createNeighbourhood(self):
        for i in range(self.xSizeMap):
            for j in range(self.ySizeMap):
                self.setNeighbours(map[i][j])

        def setNeighbours(self, tile):
            x = tile.getX()
            y = tile.getY()
            neighbours = []
            if y % 2 == 0:
                if x > 0:
                    neighbours.append(self.getTile(x - 1, y))
                    if y > 0: neighbours.append(self.getTile(x - 1, y - 1))
                    if y < self.ySize_ - 1: neighbours.append(self.getTile(x - 1, y + 1))
                if x < self.xSize_ - 1: neighbours.append(self.getTile(x + 1, y))
                if y > 0: neighbours.append(self.getTile(x, y - 1))
                if y < self.ySize_ - 1: neighbours.append(self.getTile(x, y + 1))
            else:
                if x > 0: neighbours.append(self.getTile(x - 1, y))
                if y > 0: neighbours.append(self.getTile(x, y - 1))
                if y < self.ySize_ - 1: neighbours.append(self.getTile(x, y + 1))
                if x < self.xSize_ - 1:
                    neighbours.append(self.getTile(x + 1, y))
                    if y > 0: neighbours.append(self.getTile(x + 1, y - 1))
                    if y < self.ySize_ - 1: neighbours.append(self.getTile(x + 1, y + 1))
